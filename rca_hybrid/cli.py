#!/usr/bin/env python3
"""
CLI Interface for Hybrid Root Cause Analysis System
"""
import argparse
import json
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
    from rca_hybrid.models import HybridAnalysisRequest
    from rca_hybrid.config import HybridAnalysisType, LearningMode
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed and the package is properly set up.")
    sys.exit(1)

class MockTaskResult:
    """Mock task result for testing"""
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.reasoning_files = {}
        self.db_data = {}

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Hybrid Root Cause Analysis System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "task_id", 
        help="Task ID to analyze"
    )
    
    parser.add_argument(
        "--analysis-type",
        choices=["dropdown", "arxiv_search", "auto_detect"],
        default="auto_detect",
        help="Type of analysis to perform (default: auto_detect)"
    )
    
    parser.add_argument(
        "--framework",
        default="unknown",
        help="Web automation framework used (default: unknown)"
    )
    
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.75,
        help="Confidence threshold for deterministic analysis (default: 0.75)"
    )
    
    parser.add_argument(
        "--learning-mode",
        choices=["passive", "active", "aggressive"],
        default="active",
        help="Learning mode for adaptive system (default: active)"
    )
    
    parser.add_argument(
        "--ai-provider",
        choices=["gpt", "groq", "gemini"],
        default="gpt",
        help="AI model provider to use (default: gpt)"
    )
    
    parser.add_argument(
        "--failure-log",
        default="",
        help="Failure log content or path to log file"
    )
    
    parser.add_argument(
        "--dom-snapshot",
        default="",
        help="DOM snapshot content or path to HTML file"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file for results (JSON format)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()

def load_content_from_file_or_string(content_or_path: str) -> str:
    """Load content from file if it's a path, otherwise return as-is"""
    if not content_or_path:
        return ""
        
    try:
        path = Path(content_or_path)
        if path.exists() and path.is_file():
            return path.read_text(encoding='utf-8')
    except Exception:
        pass
    
    return content_or_path

async def run_analysis(args):
    """Run hybrid root cause analysis"""
    
    # Map string arguments to enums
    analysis_type_map = {
        "dropdown": HybridAnalysisType.DROPDOWN,
        "arxiv_search": HybridAnalysisType.ARXIV_SEARCH,
        "auto_detect": HybridAnalysisType.AUTO_DETECT
    }
    
    learning_mode_map = {
        "passive": LearningMode.PASSIVE,
        "active": LearningMode.ACTIVE,
        "aggressive": LearningMode.AGGRESSIVE
    }
    
    # Load content from files if needed
    failure_log = load_content_from_file_or_string(args.failure_log)
    dom_snapshot = load_content_from_file_or_string(args.dom_snapshot)
    
    # Create analysis request
    request = HybridAnalysisRequest(
        task_id=args.task_id,
        analysis_type=analysis_type_map[args.analysis_type],
        task_result=MockTaskResult(args.task_id),
        failure_log=failure_log,
        dom_snapshot=dom_snapshot,
        action_sequence=[],
        framework=args.framework,
        confidence_threshold=args.confidence_threshold,
        learning_mode=learning_mode_map[args.learning_mode]
    )
    
    # Initialize analyzer
    analyzer = HybridRootCauseAnalyzer(
        confidence_threshold=args.confidence_threshold,
        learning_mode=learning_mode_map[args.learning_mode],
        ai_provider=args.ai_provider
    )
    
    if args.verbose:
        print(f"Starting hybrid analysis for task: {args.task_id}")
        print(f"Analysis type: {args.analysis_type}")
        print(f"Framework: {args.framework}")
        print(f"AI Provider: {args.ai_provider}")
        print(f"Learning mode: {args.learning_mode}")
        print(f"Confidence threshold: {args.confidence_threshold}")
        print("-" * 50)
    
    try:
        # Run analysis
        result = await analyzer.analyze(request)
        
        # Prepare output
        output_data = {
            "task_id": result.task_id,
            "analysis_type": result.analysis_type.value,
            "timestamp": result.timestamp.isoformat(),
            "primary_method": result.primary_method,
            "final_root_cause": result.final_root_cause,
            "final_confidence": result.final_confidence,
            "deterministic_success": result.deterministic_success,
            "ai_used": result.ai_used,
            "learning_applied": result.learning_applied,
            "new_pattern_discovered": result.new_pattern_discovered,
            "rule_updates_made": result.rule_updates_made,
            "total_analysis_time_ms": result.total_analysis_time_ms,
            "fallback_used": result.fallback_used,
            "framework": result.framework,
            "learning_mode": result.learning_mode.value
        }
        
        # Add detailed results if available
        if result.deterministic_result:
            output_data["deterministic_result"] = {
                "analyzer_type": result.deterministic_result.analyzer_type,
                "root_cause": result.deterministic_result.root_cause,
                "confidence_score": result.deterministic_result.confidence_score,
                "success": result.deterministic_result.success,
                "analysis_time_ms": result.deterministic_result.analysis_time_ms
            }
        
        if result.ai_result:
            output_data["ai_result"] = {
                "root_causes": result.ai_result.root_causes,
                "contributing_factors": result.ai_result.contributing_factors,
                "recommendations": result.ai_result.recommendations,
                "confidence_score": result.ai_result.confidence_score,
                "analysis_summary": result.ai_result.analysis_summary,
                "success": result.ai_result.success,
                "analysis_time_ms": result.ai_result.analysis_time_ms
            }
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"Results saved to: {args.output}")
        else:
            print(json.dumps(output_data, indent=2))
        
        if args.verbose:
            print(f"\nAnalysis completed in {result.total_analysis_time_ms:.2f}ms")
            print(f"Primary method used: {result.primary_method}")
            print(f"Final confidence: {result.final_confidence:.2f}")
            
    except Exception as e:
        error_output = {
            "error": str(e),
            "task_id": args.task_id,
            "timestamp": datetime.now().isoformat()
        }
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(error_output, f, indent=2)
        else:
            print(json.dumps(error_output, indent=2))
        
        if args.verbose:
            import traceback
            print(f"Error occurred: {e}")
            print(traceback.format_exc())
        
        return 1
    
    return 0

def main():
    """Main CLI entry point"""
    args = parse_arguments()
    
    try:
        exit_code = asyncio.run(run_analysis(args))
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
