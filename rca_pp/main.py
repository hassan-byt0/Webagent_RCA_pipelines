#!/usr/bin/env python3
"""
Root Cause Analysis Pipeline - Main Entry Point
"""
import asyncio
from .pipeline import RCAPipeline

if __name__ == "__main__":
    pipeline = RCAPipeline(
        parent_folder="data/db/browseruse/dropdown_BO",
        output_dir="rca_pp/rca_results"
    )
    asyncio.run(pipeline.run_pipeline())