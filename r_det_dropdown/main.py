#!/usr/bin/env python3
"""
Main entry point for Deterministic Dropdown Root Cause Analysis
"""
import asyncio
import sys
from pathlib import Path

# Add the parent directory to sys.path to import the package
sys.path.append(str(Path(__file__).parent.parent))

from r_det_dropdown.pipeline import DropdownDetPipeline

def main():
    """Main function to run the deterministic dropdown analysis"""
    
    # Configuration - adjust these paths as needed
    parent_folder = "data/failed tasks/browseruse_gpt/dropdown/per"  # Path to failed tasks
    output_dir = "r_det_dropdown/results"  # Output directory for results
    
    print("🔍 Starting Deterministic Dropdown Root Cause Analysis")
    print(f"📂 Input folder: {parent_folder}")
    print(f"📊 Output folder: {output_dir}")
    print("=" * 60)
    
    # Initialize and run pipeline
    pipeline = DropdownDetPipeline(
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
