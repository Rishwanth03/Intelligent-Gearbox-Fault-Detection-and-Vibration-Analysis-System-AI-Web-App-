#!/usr/bin/env python3
"""
Gearbox Dataset Preprocessing Tool
Simple CLI for batch processing vibration data files.
For advanced analysis and web interface, use webapp.py
"""

import os
import logging
from src import preprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Process all raw data files into a combined dataset."""
    
    RAW_DATA_DIR = "data/raw"
    PROCESSED_PATH = "data/processed/gearbox_dataset.csv"
    
    if not os.path.exists(RAW_DATA_DIR):
        logger.error(f"Raw data directory not found: {RAW_DATA_DIR}")
        return
    
    print("🔧 Gearbox Dataset Preprocessing")
    print("=" * 40)
    
    logger.info("Loading and preprocessing dataset...")
    df = preprocess.load_and_label_data(RAW_DATA_DIR)
    
    logger.info(f"Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
    print(f"\n📊 Combined Dataset: {df.shape[0]:,} samples from {len(df['source_file'].unique())} files")
    
    # Show sample
    print("\n📋 Sample Data:")
    print(df.head())
    
    logger.info("Saving processed dataset...")
    preprocess.save_processed_data(df, PROCESSED_PATH)
    
    print(f"\n✅ Complete! Saved to: {PROCESSED_PATH}")
    print(f"🌐 For advanced analysis, run: python webapp.py")

if __name__ == "__main__":
    main()
