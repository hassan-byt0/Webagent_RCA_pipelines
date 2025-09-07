#!/usr/bin/env python3
"""
Main entry point for Deterministic ArXiv Search Root Cause Analysis
"""
import asyncio
import sys
from pathlib import Path

# Add the parent directory to sys.path to import the package
sys.path.append(str(Path(__file__).parent.parent))

from rca_det_search.pipeline import ArxivDetPipeline

def main():
    """Main function to run the deterministic ArXiv search analysis"""
    
    # Configuration - adjust these paths as needed
    parent_folder = "data/failed tasks/browseruse_gpt/arxiv/per"  # Path to failed tasks
    output_dir = "rca_det_search/results"  # Output directory for results
    
    print("🔍 Starting Deterministic ArXiv Search Root Cause Analysis")
    print(f"📂 Input folder: {parent_folder}")
    print(f"📊 Output folder: {output_dir}")
    print("=" * 60)
    
    # Initialize and run pipeline
    pipeline = ArxivDetPipeline(
        parent_folder=parent_folder,
        output_dir=output_dir
    )
    
    try:
        # Run the async pipeline
        results = asyncio.run(pipeline.run_pipeline())
        
        # Print summary
        print("=" * 60)
        print("🎯 Analysis Complete!")
        print(f"📈 Total tasks analyzed: {results.get('task_statistics', {}).get('total_tasks', 0)}")
        print(f"✅ Successful analyses: {results.get('task_statistics', {}).get('successful_analyses', 0)}")
        print(f"⏱️  Duration: {results.get('pipeline_info', {}).get('duration_seconds', 0):.2f} seconds")
        
        # Print root cause distribution
        root_causes = results.get('root_cause_distribution', {})
        if root_causes:
            print("\n🔍 Root Cause Distribution:")
            for cause, count in root_causes.items():
                print(f"  • {cause}: {count}")
        
        # Print author failure distribution
        author_failures = results.get('author_failure_distribution', {})
        if author_failures:
            print("\n👤 Author Failure Types:")
            for failure_type, count in author_failures.items():
                print(f"  • {failure_type}: {count}")
        
        # Print date failure distribution
        date_failures = results.get('date_failure_distribution', {})
        if date_failures:
            print("\n📅 Date Failure Types:")
            for failure_type, count in date_failures.items():
                print(f"  • {failure_type}: {count}")
        
        # Print framework distribution  
        frameworks = results.get('framework_distribution', {})
        if frameworks:
            print("\n🛠️  Framework Distribution:")
            for framework, count in frameworks.items():
                print(f"  • {framework}: {count}")
        
        print(f"\n📁 Detailed results saved to: {output_dir}")
        
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
