"""
AI-powered Root Cause Analyzer for Hybrid System
Adapts the existing rca_pipeline.py functionality for the hybrid architecture
"""
import os
import json
import sqlite3
import logging
import asyncio
import re
import hashlib
import time
import tiktoken
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from bs4 import BeautifulSoup

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logging.warning("LangChain not available, AI analysis will be limited")

try:
    from .models import AIAnalysisResult, HybridAnalysisRequest
    from .config import AI_MODEL_CONFIG, TIMEOUTS, logger
except ImportError:
    from models import AIAnalysisResult, HybridAnalysisRequest
    from config import AI_MODEL_CONFIG, TIMEOUTS, logger

# Token estimation function
def estimate_tokens(text: str, model: str) -> int:
    """Estimate tokens using tiktoken or fallback method"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        return len(text) // 4 + 1

@dataclass
class TaskResult:
    """Structure for webagent task results - adapted from rca_pipeline.py"""
    task_id: str
    timestamp: datetime
    task_type: str
    status: str
    verified_success: bool = False
    reasoning_files: Dict[str, str] = None
    html_files: List[Dict] = None
    script_files: List[Dict] = None
    db_data: Optional[Dict] = None
    other_files: List[Dict] = None
    folder_structure: Dict = None

    def __post_init__(self):
        if self.reasoning_files is None:
            self.reasoning_files = {}
        if self.html_files is None:
            self.html_files = []
        if self.script_files is None:
            self.script_files = []
        if self.other_files is None:
            self.other_files = []
        if self.folder_structure is None:
            self.folder_structure = {}
        if self.db_data is None:
            self.db_data = {}

class AIRootCauseAnalyzer:
    """
    AI-powered root cause analyzer using LLM analysis
    Adapted from the existing rca_pipeline.py
    """
    
    def __init__(self, model_config=None):
        self.model_config = model_config if model_config is not None else AI_MODEL_CONFIG
        self.timeout = TIMEOUTS.get('ai_analysis', 30.0)
        self._init_llm()
        
    def _init_llm(self):
        """Initialize the LLM client"""
        if not LANGCHAIN_AVAILABLE:
            self.llm = None
            logger.warning("LangChain not available, AI analysis disabled")
            return
            
        try:
            # Initialize LLM based on provider
            provider = self.model_config.get('provider', 'openai')
            api_key_env = self.model_config.get('api_key_env', 'OPENAI_API_KEY')
            api_key = os.getenv(api_key_env)
            
            if not api_key:
                logger.warning(f"API key not found in environment variable: {api_key_env}")
                self.llm = None
                return
            
            if provider == 'openai':
                # OpenAI GPT models
                self.llm = ChatOpenAI(
                    model=self.model_config['model'],
                    temperature=self.model_config['temperature'],
                    max_tokens=self.model_config['max_tokens'],
                    base_url=self.model_config.get('base_url', 'https://api.openai.com/v1'),
                    api_key=api_key
                )
            elif provider == 'groq':
                # Groq models (using OpenAI-compatible API)
                self.llm = ChatOpenAI(
                    model=self.model_config['model'],
                    temperature=self.model_config['temperature'],
                    max_tokens=self.model_config['max_tokens'],
                    base_url=self.model_config.get('base_url', 'https://api.groq.com/openai/v1'),
                    api_key=api_key
                )
            elif provider == 'google':
                # Google Gemini models
                try:
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    self.llm = ChatGoogleGenerativeAI(
                        model=self.model_config['model'],
                        temperature=self.model_config['temperature'],
                        max_tokens=self.model_config['max_tokens'],
                        google_api_key=api_key
                    )
                except ImportError:
                    logger.error("langchain_google_genai not installed. Install with: pip install langchain-google-genai")
                    # Fallback to OpenAI-compatible API if available
                    self.llm = ChatOpenAI(
                        model=self.model_config['model'],
                        temperature=self.model_config['temperature'],
                        max_tokens=self.model_config['max_tokens'],
                        base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
                        api_key=api_key
                    )
            else:
                logger.error(f"Unsupported provider: {provider}")
                self.llm = None
                return
            
            logger.info(f"AI analyzer initialized with {provider} provider, model: {self.model_config['model']}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self.llm = None

    async def analyze(self, request: HybridAnalysisRequest) -> AIAnalysisResult:
        """
        Perform AI-powered root cause analysis
        """
        start_time = time.time()
        
        try:
            if not self.llm:
                return AIAnalysisResult(
                    root_causes=["AI analysis unavailable - LLM not initialized"],
                    five_whys={},
                    contributing_factors=["LLM initialization failed"],
                    recommendations=["Check API keys and model configuration"],
                    analysis_summary="AI analysis could not be performed due to LLM initialization failure",
                    confidence_score=0.0,
                    analysis_time_ms=(time.time() - start_time) * 1000,
                    success=False,
                    framework_detected=request.framework,
                    additional_data={"error": "LLM not available"}
                )

            # Prepare context for analysis
            context = self._prepare_analysis_context(request)
            
            # Perform multi-stage analysis
            primary_analysis = await self._perform_primary_analysis(context)
            detailed_analysis = await self._perform_detailed_analysis(context, primary_analysis)
            
            # Extract structured results
            result = self._extract_analysis_result(
                primary_analysis, 
                detailed_analysis, 
                request,
                start_time
            )
            
            logger.info(f"AI analysis completed for task {request.task_id} in {result.analysis_time_ms:.2f}ms")
            return result
            
        except Exception as e:
            logger.error(f"AI analysis failed for task {request.task_id}: {e}")
            logger.error(traceback.format_exc())
            
            return AIAnalysisResult(
                root_causes=[f"AI analysis error: {str(e)}"],
                five_whys={},
                contributing_factors=["Analysis pipeline failure"],
                recommendations=["Review error logs and retry analysis"],
                analysis_summary=f"AI analysis failed due to: {str(e)}",
                confidence_score=0.0,
                analysis_time_ms=(time.time() - start_time) * 1000,
                success=False,
                framework_detected=request.framework,
                additional_data={"error": str(e), "traceback": traceback.format_exc()}
            )

    def _prepare_analysis_context(self, request: HybridAnalysisRequest) -> Dict[str, Any]:
        """Prepare context for AI analysis"""
        context = {
            "task_id": request.task_id,
            "framework": request.framework,
            "failure_log": request.failure_log[:5000],  # Limit size
            "dom_snapshot": self._process_dom_snapshot(request.dom_snapshot),
            "action_sequence": request.action_sequence[-10:],  # Last 10 actions
            "analysis_type": request.analysis_type.value,
            "timestamp": request.timestamp.isoformat()
        }
        
        # Add task result information if available
        if hasattr(request.task_result, 'reasoning_files'):
            context["reasoning_summary"] = self._summarize_reasoning_files(
                request.task_result.reasoning_files
            )
        
        if hasattr(request.task_result, 'db_data'):
            context["db_summary"] = self._summarize_db_data(
                request.task_result.db_data
            )
            
        return context

    def _process_dom_snapshot(self, dom_snapshot: str) -> str:
        """Process and clean DOM snapshot for analysis"""
        if not dom_snapshot:
            return "No DOM snapshot available"
            
        try:
            # Parse HTML and extract relevant information
            soup = BeautifulSoup(dom_snapshot, 'html.parser')
            
            # Remove script and style elements
            for element in soup(["script", "style"]):
                element.decompose()
            
            # Extract text content and structure
            text_content = soup.get_text()
            
            # Limit size and clean
            cleaned = re.sub(r'\s+', ' ', text_content)[:2000]
            
            # Extract form elements and interactive components
            forms = soup.find_all(['form', 'input', 'button', 'select', 'textarea'])
            form_info = []
            for form in forms[:10]:  # Limit to first 10
                form_info.append({
                    "tag": form.name,
                    "id": form.get('id', ''),
                    "class": ' '.join(form.get('class', [])),
                    "type": form.get('type', ''),
                    "name": form.get('name', '')
                })
            
            return {
                "text_content": cleaned,
                "interactive_elements": form_info,
                "total_elements": len(soup.find_all())
            }
            
        except Exception as e:
            logger.warning(f"DOM processing failed: {e}")
            return f"DOM processing error: {str(e)}"

    def _summarize_reasoning_files(self, reasoning_files: Dict[str, str]) -> str:
        """Summarize reasoning files content"""
        if not reasoning_files:
            return "No reasoning files available"
            
        summary_parts = []
        for filename, content in reasoning_files.items():
            # Extract key information from reasoning content
            lines = content.split('\n')
            key_lines = [line for line in lines[-50:] if any(keyword in line.lower() 
                        for keyword in ['error', 'fail', 'timeout', 'exception', 'unable'])]
            
            if key_lines:
                summary_parts.append(f"{filename}: {' | '.join(key_lines[:3])}")
                
        return ' | '.join(summary_parts) if summary_parts else "No error indicators found in reasoning"

    def _summarize_db_data(self, db_data: Dict) -> str:
        """Summarize database data for analysis"""
        if not db_data:
            return "No database data available"
            
        summary = []
        
        # Summarize actions taken
        if 'actions' in db_data:
            actions = db_data['actions']
            summary.append(f"Total actions: {len(actions)}")
            
            # Last few actions
            if actions:
                last_actions = actions[-3:]
                action_summary = []
                for action in last_actions:
                    action_type = action.get('event_type', 'unknown')
                    target = action.get('xpath', action.get('element_id', 'unknown'))
                    action_summary.append(f"{action_type}({target})")
                summary.append(f"Last actions: {' -> '.join(action_summary)}")
        
        # Check for common failure patterns
        failure_indicators = []
        if 'errors' in db_data:
            failure_indicators.append(f"Errors: {len(db_data['errors'])}")
        if 'timeouts' in db_data:
            failure_indicators.append(f"Timeouts: {len(db_data['timeouts'])}")
            
        if failure_indicators:
            summary.extend(failure_indicators)
            
        return ' | '.join(summary) if summary else "No significant database patterns found"

    async def _perform_primary_analysis(self, context: Dict[str, Any]) -> str:
        """Perform primary root cause analysis"""
        
        system_prompt = """You are an expert in web automation failure analysis. Analyze the provided context and identify the primary root cause of the task failure.

Focus on:
1. Element interaction failures (clicking, typing, selecting)
2. Navigation and timing issues  
3. DOM changes and dynamic content
4. Framework-specific patterns
5. Data validation problems

Provide a concise primary root cause analysis."""

        user_prompt = f"""
Task ID: {context['task_id']}
Framework: {context['framework']}
Analysis Type: {context['analysis_type']}

Failure Log:
{context['failure_log']}

DOM Summary: {json.dumps(context['dom_snapshot'], indent=2)}

Recent Actions: {json.dumps(context['action_sequence'], indent=2)}

Reasoning Summary: {context.get('reasoning_summary', 'Not available')}

DB Summary: {context.get('db_summary', 'Not available')}

Identify the primary root cause of this web automation failure.
"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = await asyncio.wait_for(
                self.llm.ainvoke(messages),
                timeout=self.timeout
            )
            
            return response.content
            
        except asyncio.TimeoutError:
            logger.warning(f"Primary analysis timeout for task {context['task_id']}")
            return "Analysis timeout - unable to complete primary analysis"
        except Exception as e:
            logger.error(f"Primary analysis error: {e}")
            return f"Primary analysis error: {str(e)}"

    async def _perform_detailed_analysis(self, context: Dict[str, Any], primary_analysis: str) -> str:
        """Perform detailed analysis including 5 Whys and recommendations"""
        
        system_prompt = """You are conducting a detailed root cause analysis. Based on the primary analysis, perform a comprehensive investigation using the 5 Whys technique and provide actionable recommendations.

Structure your response as:
1. 5 Whys Analysis
2. Contributing Factors  
3. Recommendations
4. Prevention Strategies"""

        user_prompt = f"""
Primary Analysis: {primary_analysis}

Context:
- Task: {context['task_id']}
- Framework: {context['framework']}
- Failure: {context['failure_log'][:1000]}

Perform detailed analysis with 5 Whys technique and provide specific recommendations for:
1. Immediate fixes
2. Prevention strategies
3. Code improvements
4. Testing enhancements
"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = await asyncio.wait_for(
                self.llm.ainvoke(messages),
                timeout=self.timeout
            )
            
            return response.content
            
        except asyncio.TimeoutError:
            logger.warning(f"Detailed analysis timeout for task {context['task_id']}")
            return "Detailed analysis timeout"
        except Exception as e:
            logger.error(f"Detailed analysis error: {e}")
            return f"Detailed analysis error: {str(e)}"

    def _extract_analysis_result(self, primary_analysis: str, detailed_analysis: str, 
                                request: HybridAnalysisRequest, start_time: float) -> AIAnalysisResult:
        """Extract structured results from analysis text"""
        
        # Extract root causes from primary analysis
        root_causes = self._extract_root_causes(primary_analysis)
        
        # Extract 5 whys from detailed analysis
        five_whys = self._extract_five_whys(detailed_analysis)
        
        # Extract contributing factors
        contributing_factors = self._extract_contributing_factors(detailed_analysis)
        
        # Extract recommendations
        recommendations = self._extract_recommendations(detailed_analysis)
        
        # Calculate confidence based on analysis quality
        confidence_score = self._calculate_confidence(primary_analysis, detailed_analysis)
        
        # Create summary
        analysis_summary = f"Primary cause: {root_causes[0] if root_causes else 'Unknown'}. " + \
                          f"Analysis completed with {len(contributing_factors)} contributing factors " + \
                          f"and {len(recommendations)} recommendations."
        
        return AIAnalysisResult(
            root_causes=root_causes,
            five_whys=five_whys,
            contributing_factors=contributing_factors,
            recommendations=recommendations,
            analysis_summary=analysis_summary,
            confidence_score=confidence_score,
            analysis_time_ms=(time.time() - start_time) * 1000,
            success=True,
            framework_detected=request.framework,
            additional_data={
                "primary_analysis": primary_analysis[:500],
                "detailed_analysis": detailed_analysis[:500]
            }
        )

    def _extract_root_causes(self, analysis: str) -> List[str]:
        """Extract root causes from analysis text"""
        root_causes = []
        
        # Look for explicit root cause statements
        patterns = [
            r"root cause[:\s]+(.*?)(?:\.|$)",
            r"primary cause[:\s]+(.*?)(?:\.|$)", 
            r"main issue[:\s]+(.*?)(?:\.|$)",
            r"core problem[:\s]+(.*?)(?:\.|$)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, analysis, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                cause = match.strip()
                if cause and len(cause) > 10:  # Filter out very short matches
                    root_causes.append(cause)
        
        # If no explicit root causes found, extract from first meaningful sentence
        if not root_causes:
            sentences = analysis.split('.')
            for sentence in sentences[:3]:  # Check first 3 sentences
                if len(sentence.strip()) > 20:
                    root_causes.append(sentence.strip())
                    break
        
        return root_causes[:3] if root_causes else ["Unable to determine root cause from analysis"]

    def _extract_five_whys(self, analysis: str) -> Dict[str, List[str]]:
        """Extract 5 whys structure from detailed analysis"""
        five_whys = {}
        
        # Look for numbered why questions
        why_pattern = r"why\s*(\d+)[:\s]+(.*?)(?:\n|$)"
        matches = re.findall(why_pattern, analysis, re.IGNORECASE | re.MULTILINE)
        
        for number, why_text in matches:
            key = f"Why {number}"
            five_whys[key] = [why_text.strip()]
        
        # If no structured whys found, create basic structure
        if not five_whys:
            lines = analysis.split('\n')
            why_lines = [line for line in lines if 'why' in line.lower()]
            for i, line in enumerate(why_lines[:5]):
                five_whys[f"Why {i+1}"] = [line.strip()]
        
        return five_whys

    def _extract_contributing_factors(self, analysis: str) -> List[str]:
        """Extract contributing factors from analysis"""
        factors = []
        
        # Look for factor sections
        factor_patterns = [
            r"contributing factors?[:\s]+(.*?)(?:\n\n|$)",
            r"factors?[:\s]+(.*?)(?:\n\n|$)",
            r"causes?[:\s]+(.*?)(?:\n\n|$)"
        ]
        
        for pattern in factor_patterns:
            matches = re.findall(pattern, analysis, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Split by common delimiters
                for delimiter in ['\n', ';', ',']:
                    if delimiter in match:
                        parts = match.split(delimiter)
                        for part in parts:
                            clean_part = part.strip(' -•*')
                            if clean_part and len(clean_part) > 5:
                                factors.append(clean_part)
                        break
                else:
                    # No delimiter found, add whole match
                    clean_match = match.strip()
                    if clean_match:
                        factors.append(clean_match)
        
        return factors[:5] if factors else ["Analysis did not identify specific contributing factors"]

    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract recommendations from analysis"""
        recommendations = []
        
        # Look for recommendation sections
        rec_patterns = [
            r"recommendations?[:\s]+(.*?)(?:\n\n|$)",
            r"solutions?[:\s]+(.*?)(?:\n\n|$)",
            r"fixes?[:\s]+(.*?)(?:\n\n|$)",
            r"improvements?[:\s]+(.*?)(?:\n\n|$)"
        ]
        
        for pattern in rec_patterns:
            matches = re.findall(pattern, analysis, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Split by common delimiters
                for delimiter in ['\n', ';']:
                    if delimiter in match:
                        parts = match.split(delimiter)
                        for part in parts:
                            clean_part = part.strip(' -•*1234567890.')
                            if clean_part and len(clean_part) > 10:
                                recommendations.append(clean_part)
                        break
                else:
                    # No delimiter found, add whole match
                    clean_match = match.strip()
                    if clean_match:
                        recommendations.append(clean_match)
        
        return recommendations[:5] if recommendations else ["No specific recommendations provided in analysis"]

    def _calculate_confidence(self, primary_analysis: str, detailed_analysis: str) -> float:
        """Calculate confidence score based on analysis quality"""
        
        confidence_factors = []
        
        # Length of analysis
        total_length = len(primary_analysis) + len(detailed_analysis)
        if total_length > 1000:
            confidence_factors.append(0.3)
        elif total_length > 500:
            confidence_factors.append(0.2)
        else:
            confidence_factors.append(0.1)
        
        # Presence of specific terms
        quality_terms = [
            'root cause', 'element', 'click', 'timeout', 'error', 
            'DOM', 'selector', 'navigation', 'framework'
        ]
        
        combined_text = (primary_analysis + ' ' + detailed_analysis).lower()
        term_count = sum(1 for term in quality_terms if term in combined_text)
        confidence_factors.append(min(term_count / len(quality_terms), 0.4))
        
        # Structure indicators  
        structure_indicators = ['why', 'recommendation', 'factor', 'cause']
        structure_count = sum(1 for indicator in structure_indicators if indicator in combined_text)
        confidence_factors.append(min(structure_count / len(structure_indicators), 0.3))
        
        return min(sum(confidence_factors), 1.0)

    def get_capabilities(self) -> Dict[str, Any]:
        """Return analyzer capabilities"""
        return {
            "name": "AI Root Cause Analyzer",
            "version": "1.0.0",
            "supported_frameworks": ["all"],
            "analysis_types": ["comprehensive", "primary", "detailed"],
            "features": [
                "LLM-powered analysis",
                "5 Whys technique", 
                "Contributing factors identification",
                "Actionable recommendations",
                "Multi-stage analysis"
            ],
            "llm_available": self.llm is not None,
            "model": self.model_config['model'] if self.llm else "unavailable"
        }
