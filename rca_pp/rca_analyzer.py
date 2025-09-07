"""
RCA Analysis with OpenAI API
"""
import re
import json
import asyncio
import hashlib
import tiktoken
import logging
from .models import TaskResult, RCAResult
from datetime import datetime
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS_PER_REQUEST, MIN_TOKENS_FOR_RESPONSE, MAX_CHUNK_SIZE

logger = logging.getLogger(__name__)

def estimate_tokens(text: str, model: str) -> int:
    """Estimate tokens using tiktoken or fallback method"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        return len(text) // 4 + 1

class OpenAIRCAAnalyzer:
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0.1,
            max_tokens=4096
        )
        self.model_name = model

    def _get_cache_path(self, task_id: str, file_name: str) -> Path:
        """Get cache path for processed reasoning files"""
        cache_dir = Path("cache/reasoning") / task_id
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / f"{hashlib.md5(file_name.encode()).hexdigest()}.json"

    def extract_critical_sections(self, content: str) -> list[str]:
        """Extract key sections to preserve verbatim"""
        critical = []
        
        # Preserve final outcome
        final_answer = re.search(r"Final Answer:.+", content, re.DOTALL)
        if final_answer:
            critical.append(final_answer.group(0)[:1000])
        
        # Preserve error messages
        errors = re.findall(r"Error:.+|Exception:.+|Failed:.+", content)
        critical.extend(errors[:3])
        
        # Preserve tool responses with failure
        tool_failures = re.findall(r"Tool:.+\nResult:.+(error|fail|invalid|denied)", content, re.IGNORECASE)
        critical.extend(tool_failures[:2])
        
        return critical

    def remove_boilerplate(self, content: str) -> str:
        """Remove unnecessary boilerplate from reasoning files"""
        cleaned = re.sub(r"# Input Format.*?---", "", content, flags=re.DOTALL)
        cleaned = re.sub(r"RESPONSE FORMAT.*?---", "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"SystemMessage.*?\)", "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"HumanMessage.*?\)", "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"AIMessage.*?\)", "", cleaned, flags=re.DOTALL)
        return cleaned.strip()

    async def summarize_to_token_limit(self, content: str, max_tokens: int) -> str:
        """Hierarchical summarization to fit token limits"""
        if estimate_tokens(content, self.model_name) <= max_tokens:
            return content
        
        # First-level summarization
        summary = await self._summarize_content(content)
        if estimate_tokens(summary, self.model_name) <= max_tokens:
            return summary
        
        # Second-level summarization
        return await self._summarize_content(summary, aggressive=True)

    async def _summarize_content(self, content: str, aggressive: bool = False) -> str:
        """Summarize content with adjustable aggressiveness"""
        if len(content) < 500:
            return content
        
        prompt = f"""
Summarize the following technical content while preserving:
- Error messages
- Key decisions
- Action sequences
- Status changes

{'Provide only the most critical points in 2-3 bullet points' if aggressive else 'Provide 3-5 key bullet points'}

Content:
{content[:5000] if aggressive else content[:10000]}
"""
        messages = [
            SystemMessage(content="You are a technical summarizer focusing on key details"),
            HumanMessage(content=prompt)
        ]
        try:
            response = await self._analyze_with_retry(messages)
            return response.strip()
        except Exception as e:
            logger.error(f"Content summarization failed: {e}")
            return content[:1000] if aggressive else content[:2000]

    async def process_reasoning_file(self, task_id: str, file_name: str, content: str) -> str:
        """Process reasoning files with hierarchical summarization"""
        cache_path = self._get_cache_path(task_id, file_name)
        if cache_path.exists():
            return json.load(open(cache_path, 'r', encoding='utf-8'))
        
        logger.info(f"Processing reasoning file: {file_name}")
        
        # Clean and extract critical content
        cleaned_content = self.remove_boilerplate(content)
        critical_sections = self.extract_critical_sections(cleaned_content)
        
        # Process remaining content
        remaining_content = cleaned_content
        for section in critical_sections:
            remaining_content = remaining_content.replace(section, "")
        
        # Create combined content
        critical_str = "\n".join(critical_sections)
        combined = f"CRITICAL SECTIONS:\n{critical_str}\n\nOTHER CONTENT:\n{remaining_content}"
        
        # Summarize to fit token budget
        processed = await self.summarize_to_token_limit(combined, 1500)
        
        # Save to cache
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(processed, f)
        return processed

    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to a specific token count"""
        try:
            encoding = tiktoken.encoding_for_model(self.model_name)
            tokens = encoding.encode(text)
            if len(tokens) <= max_tokens:
                return text
            return encoding.decode(tokens[:max_tokens])
        except:
            return text[:max_tokens * 4]

    async def generate_compact_prompt(self, task_result: TaskResult) -> tuple[str, int]:
        """Generate RCA prompt with strict token budgeting"""
        # Get core task info
        primary_framework = "Unknown"
        element_counts = {}
        if task_result.html_files:
            for html_data in task_result.html_files:
                if html_data.get('primary_framework'):
                    primary_framework = html_data['primary_framework']
                if html_data.get('element_counts'):
                    element_counts = html_data['element_counts']
        
        # Build base prompt
        base_prompt = f"""
## TASK CONTEXT
- ID: {task_result.task_id}
- Status: {task_result.status} {'(Verified)' if task_result.verified_success else '(Unverified)'}
- Type: {task_result.task_type}

## UI FRAMEWORK ANALYSIS
- Primary Framework: {primary_framework}
- Element Distribution: {json.dumps(element_counts) or 'No elements detected'}

## REASONING ANALYSIS
"""
        token_count = estimate_tokens(base_prompt, self.model_name)
        reasoning_content = ""
        
        # Process reasoning files with token budget
        for file_path, content in task_result.reasoning_files.items():
            if token_count >= MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
                break
                
            processed = await self.process_reasoning_file(task_result.task_id, file_path, content)
            file_content = f"\n\n### {file_path}\n{processed}"
            file_tokens = estimate_tokens(file_content, self.model_name)
            
            if token_count + file_tokens > MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
                file_content = await self.summarize_to_token_limit(file_content, 500)
                file_tokens = estimate_tokens(file_content, self.model_name)
            
            if token_count + file_tokens <= MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
                reasoning_content += file_content
                token_count += file_tokens
        
        # Add database information
        db_content = "\n\n## DATABASE SUMMARY"
        if task_result.db_data:
            db_summary = []
            for db_path, db_info in task_result.db_data.items():
                db_summary.append(f"- {db_path}: {db_info.get('total_tables', 0)} tables")
                for table, details in db_info.get('tables', {}).items():
                    db_summary.append(f"  - {table}: {details.get('row_count', 0)} rows")
                    if len(db_summary) > 5:
                        break
            db_content += "\n" + "\n".join(db_summary[:5])
        else:
            db_content += "\nNo databases found"
        
        db_tokens = estimate_tokens(db_content, self.model_name)
        if token_count + db_tokens > MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
            db_content = "\n\n## DATABASE SUMMARY\n[Summary truncated]"
            db_tokens = estimate_tokens(db_content, self.model_name)
        token_count += db_tokens
        
        # Add analysis directives
        directives = f"""
        
## ROOT CAUSE ANALYSIS DIRECTIVES
1. Focus on critical sections from reasoning analysis
2. Analyze failures in relation to UI framework
3. Use 5 Whys methodology
4. Provide specific technical recommendations
5. Include database issues if applicable

## RESPONSE FORMAT
{{
  "root_causes": ["..."],
  "five_whys": {{"Cause": ["Why1", "Why2", ...]}},
  "contributing_factors": ["..."],
  "recommendations": ["..."],
  "analysis_summary": "...",
  "framework": "{primary_framework}",
  "element_types": {json.dumps(element_counts)},
  "db_issues": ["..."]
}}
"""
        # Combine all parts
        full_prompt = base_prompt + reasoning_content + db_content + directives
        token_count = estimate_tokens(full_prompt, self.model_name)
        
        # Final truncation if needed
        if token_count > MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
            full_prompt = self._truncate_to_tokens(
                full_prompt, 
                MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE
            )
            token_count = estimate_tokens(full_prompt, self.model_name)
        
        return full_prompt, token_count

    async def hierarchical_rca_analysis(self, task_result: TaskResult) -> RCAResult:
        """Perform RCA in stages to handle large inputs"""
        # Stage 1: Analyze reasoning files
        reasoning_analysis = await self.analyze_reasoning_files(task_result)
        
        # Stage 2: Analyze UI framework
        framework_analysis = await self.analyze_ui_framework(task_result)
        
        # Stage 3: Analyze database
        db_analysis = await self.analyze_database(task_result)
        
        # Stage 4: Final RCA synthesis
        return await self.synthesize_rca(
            task_result, 
            reasoning_analysis, 
            framework_analysis, 
            db_analysis
        )

    async def analyze_reasoning_files(self, task_result: TaskResult) -> str:
        """Analyze reasoning files in a focused way"""
        analysis = []
        for file_path, content in task_result.reasoning_files.items():
            processed = await self.process_reasoning_file(task_result.task_id, file_path, content)
            analysis.append(f"### {file_path}\n{processed}")
        
        prompt = f"""
Analyze the following reasoning files to identify critical failures and decision points:

{"".join(analysis)}

Respond with a concise summary of:
- Key errors
- Critical decision points
- Final outcomes
"""
        messages = [
            SystemMessage(content="You are an analyst identifying critical issues in task execution logs"),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = await self._analyze_with_retry(messages)
            return response.strip()
        except Exception as e:
            logger.error(f"Reasoning analysis failed: {e}")
            return "Reasoning analysis incomplete"

    async def analyze_ui_framework(self, task_result: TaskResult) -> str:
        """Analyze UI framework and elements"""
        if not task_result.html_files:
            return "No UI analysis performed"
        
        primary_framework = "Unknown"
        element_counts = {}
        for html_data in task_result.html_files:
            if html_data.get('primary_framework'):
                primary_framework = html_data['primary_framework']
            if html_data.get('element_counts'):
                element_counts = html_data['element_counts']
        
        prompt = f"""
Analyze the UI framework and element distribution for potential issues:

- Primary Framework: {primary_framework}
- Element Distribution: {json.dumps(element_counts)}

Consider common failure patterns for this framework and element types.
"""
        messages = [
            SystemMessage(content="You are a UI expert analyzing potential failure points"),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = await self._analyze_with_retry(messages)
            return response.strip()
        except Exception as e:
            logger.error(f"UI analysis failed: {e}")
            return "UI analysis incomplete"

    async def analyze_database(self, task_result: TaskResult) -> str:
        """Analyze database state for issues"""
        if not task_result.db_data:
            return "No database analysis performed"
        
        db_summary = []
        for db_path, db_info in task_result.db_data.items():
            db_summary.append(f"- {db_path}: {db_info.get('total_tables', 0)} tables")
            for table, details in db_info.get('tables', {}).items():
                db_summary.append(f"  - {table}: {details.get('row_count', 0)} rows")
                if len(db_summary) > 10:
                    break
        
        prompt = f"""
Review the database state for potential issues:

{"".join(db_summary)}

Identify any anomalies or inconsistencies.
"""
        messages = [
            SystemMessage(content="You are a database analyst identifying potential data issues"),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = await self._analyze_with_retry(messages)
            return response.strip()
        except Exception as e:
            logger.error(f"Database analysis failed: {e}")
            return "Database analysis incomplete"

    async def synthesize_rca(self, task_result: TaskResult, reasoning_analysis: str, 
                             framework_analysis: str, db_analysis: str) -> RCAResult:
        """Synthesize final RCA from component analyses"""
        # Get core task info
        primary_framework = "Unknown"
        element_counts = {}
        if task_result.html_files:
            for html_data in task_result.html_files:
                if html_data.get('primary_framework'):
                    primary_framework = html_data['primary_framework']
                if html_data.get('element_counts'):
                    element_counts = html_data['element_counts']
        
        prompt = f"""
## TASK CONTEXT
- ID: {task_result.task_id}
- Status: {task_result.status} {'(Verified)' if task_result.verified_success else '(Unverified)'}
- Type: {task_result.task_type}

## REASONING ANALYSIS SUMMARY
{reasoning_analysis}

## UI FRAMEWORK ANALYSIS SUMMARY
{framework_analysis}

## DATABASE ANALYSIS SUMMARY
{db_analysis}

## ROOT CAUSE ANALYSIS SYNTHESIS
Perform a comprehensive root cause analysis by integrating the above analyses.
Use the 5 Whys methodology to identify root causes and provide specific recommendations.

## RESPONSE FORMAT
{{
  "root_causes": ["..."],
  "five_whys": {{"Cause": ["Why1", "Why2", ...]}},
  "contributing_factors": ["..."],
  "recommendations": ["..."],
  "analysis_summary": "...",
  "framework": "{primary_framework}",
  "element_types": {json.dumps(element_counts)},
  "db_issues": ["..."]
}}
"""
        # Validate token count
        token_count = estimate_tokens(prompt, self.model_name)
        if token_count > MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
            logger.warning(f"RCA synthesis prompt too large ({token_count} tokens), truncating")
            prompt = self._truncate_to_tokens(prompt, MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE)
        
        messages = [
            SystemMessage(content="You are an RCA synthesis expert"),
            HumanMessage(content=prompt)
        ]
        
        response_content = await self._analyze_with_retry(messages)
        return self._parse_response(task_result.task_id, response_content)

    async def analyze_task(self, task_result: TaskResult) -> RCAResult:
        """Perform RCA with strict token management"""
        try:
            # First try compact analysis
            prompt, token_count = await self.generate_compact_prompt(task_result)
            if token_count <= MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
                logger.info(f"Using compact prompt ({token_count} tokens) for {task_result.task_id}")
                return await self._analyze_single_prompt(prompt, task_result.task_id)
            else:
                # Fall back to hierarchical analysis
                logger.warning(f"Compact prompt too large ({token_count} tokens), using hierarchical RCA")
                return await self.hierarchical_rca_analysis(task_result)
        except Exception as e:
            logger.exception(f"RCA analysis failed: {e}")
            return self._error_result(task_result.task_id, str(e))

    async def _analyze_single_prompt(self, prompt: str, task_id: str) -> RCAResult:
        """Process normal-sized prompt with validation"""
        token_count = estimate_tokens(prompt, self.model_name)
        if token_count > MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
            logger.warning(f"Prompt too large ({token_count} tokens), truncating")
            prompt = self._truncate_to_tokens(prompt, MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE)
        
        messages = [
            SystemMessage(content="You are an expert in root cause analysis for automated web agents."),
            HumanMessage(content=prompt)
        ]
        
        response_content = await self._analyze_with_retry(messages)
        return self._parse_response(task_id, response_content)

    async def _analyze_with_retry(self, messages: list, max_retries: int = 5) -> str:
        """Send request with exponential backoff - OPENAI VERSION"""
        # Validate message size
        content = "".join([msg.content for msg in messages if isinstance(msg, HumanMessage)])
        token_count = estimate_tokens(content, self.model_name)
        
        # Updated token limits for OpenAI
        if token_count > MAX_TOKENS_PER_REQUEST - MIN_TOKENS_FOR_RESPONSE:
            logger.error(f"Request too large ({token_count} tokens), cannot proceed")
            raise ValueError(f"Request exceeds maximum size ({MAX_TOKENS_PER_REQUEST} tokens)")
        
        for attempt in range(max_retries):
            try:
                return (await asyncio.to_thread(self.llm.invoke, messages)).content
            except Exception as e:
                if "context_length" in str(e):
                    # Handle context length errors specifically
                    logger.error(f"Context length exceeded: {e}")
                    raise
                elif "rate_limit" in str(e) or "429" in str(e):
                    wait_time = min(2 ** (attempt + 1) + 5, 60)
                    logger.warning(f"Rate limited (attempt {attempt+1}/{max_retries}), waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                else:
                    wait_time = min(2 ** (attempt + 1), 30)
                    logger.warning(f"API error (attempt {attempt+1}/{max_retries}): {e} - waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
        raise RuntimeError(f"Failed after {max_retries} retries")

    def _parse_response(self, task_id: str, response_content: str) -> RCAResult:
        """Parse response with enhanced validation and multiple JSON extraction methods"""
        # Try to find JSON in various formats
        json_match = None
        patterns = [
            r'```json\s*({.*?})\s*```',
            r'```\s*({.*?})\s*```',
            r'({.*})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response_content, re.DOTALL)
            if match:
                json_match = match.group(1)
                try:
                    data = json.loads(json_match)
                    break
                except json.JSONDecodeError:
                    continue
        
        # If no match found, try to parse the whole response
        if not json_match:
            try:
                data = json.loads(response_content)
            except json.JSONDecodeError:
                logger.error(f"Response parsing failed: No JSON found in response")
                logger.error(f"Response content (truncated): {response_content[:1000]}")
                return self._error_result(task_id, "No valid JSON found in response")
        
        # Set default values for required fields
        required_fields = ['root_causes', 'five_whys', 'recommendations', 'analysis_summary']
        defaults = {
            'root_causes': ["Root cause analysis incomplete: missing field"],
            'five_whys': {"Cause": ["Analysis incomplete"]},
            'recommendations': ["Review the model response for technical issues"],
            'analysis_summary': "Analysis summary missing due to model response format issues"
        }
        
        # Ensure required fields exist
        for field in required_fields:
            if field not in data:
                logger.warning(f"Response missing required field: {field}")
                data[field] = defaults[field]
        
        # Ensure framework has a default value
        framework = data.get('framework', 'Unknown')
        
        return RCAResult(
            task_id=task_id,
            analysis_timestamp=datetime.now(),
            root_causes=data.get('root_causes', []),
            five_whys=data.get('five_whys', {}),
            contributing_factors=data.get('contributing_factors', []),
            recommendations=data.get('recommendations', []),
            analysis_summary=data.get('analysis_summary', ''),
            framework=framework,
            element_types=data.get('element_types', {}),
            db_issues=data.get('db_issues', [])
        )
    
    def _error_result(self, task_id: str, error: str) -> RCAResult:
        """Create error result"""
        return RCAResult(
            task_id=task_id,
            analysis_timestamp=datetime.now(),
            root_causes=[f"Analysis error: {error}"],
            five_whys={"Cause": [f"Technical failure: {error}"]},
            contributing_factors=["Technical failure"],
            recommendations=["Check logs", "Verify configuration"],
            analysis_summary="RCA failed due to technical error",
            framework="Unknown"
        )

# GROQ VERSION (COMMENTED OUT)
# class GroqRCAAnalyzer:
#     def __init__(self, api_key: str = GROQ_API_KEY, model: str = GROQ_MODEL):
#         self.llm = ChatOpenAI(
#             base_url="https://api.groq.com/openai/v1",
#             api_key=api_key,
#             model=model,
#             temperature=0.1,
#             max_tokens=4096
#         )
#         self.model_name = model
#
#     # ... (All Groq methods would be here - identical to the OpenAIRCAAnalyzer methods above) ...
# 
#     async def _analyze_with_retry(self, messages: List, max_retries: int = 5) -> str:
#         """Send request with exponential backoff and rate limit handling"""
#         # First validate message size
#         content = "".join([msg.content for msg in messages if isinstance(msg, HumanMessage)])
#         token_count = estimate_tokens(content, self.model_name)
#         if token_count > 6000:  # Groq's hard limit for this model
#             logger.error(f"Request too large ({token_count} tokens), cannot proceed")
#             raise ValueError(f"Request exceeds maximum size (6000 tokens)")
#         
#         for attempt in range(max_retries):
#             try:
#                 return (await asyncio.to_thread(self.llm.invoke, messages)).content
#             except Exception as e:
#                 if "413" in str(e):
#                     # Request too large - we can't recover from this
#                     logger.error("Request too large, aborting")
#                     raise
#                 elif "429" in str(e):
#                     wait_time = min(2 ** (attempt + 1) + 5, 60)  # Exponential backoff with min 5s
#                     logger.warning(f"Rate limited (attempt {attempt+1}/{max_retries}), waiting {wait_time}s")
#                     await asyncio.sleep(wait_time)
#                 else:
#                     wait_time = min(2 ** (attempt + 1), 30)
#                     logger.warning(f"API error (attempt {attempt+1}/{max_retries}): {e} - waiting {wait_time}s")
#                     await asyncio.sleep(wait_time)
#         raise RuntimeError(f"Failed after {max_retries} retries")