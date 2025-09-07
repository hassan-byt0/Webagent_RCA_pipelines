#!/usr/bin/env python3
"""
Root Cause Analysis Pipeline - Main Entry Point
"""
import asyncio
from .pipeline import RCAPipeline

if __name__ == "__main__":
    pipeline = RCAPipeline(
        parent_folder="data/failed tasks/broweruse_gpt/dropdown/per",
        web_folder="rca_pp_2/web_folder_2/drop-down-websites",  # Path to directory with reference HTML variations
        output_dir="rca_pp_2/rca_results_dropdown_g2.5pro3"
    )
    asyncio.run(pipeline.run_pipeline())