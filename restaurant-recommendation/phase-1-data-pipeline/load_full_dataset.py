#!/usr/bin/env python3
"""
Batch loading script for full Hugging Face dataset.
Loads data in batches to avoid SQL parameter limits.
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data.ingestion import load_restaurant_dataset
from src.data.preprocessing import clean_restaurant_data
from src.data.store import RestaurantStore
from src.config import DB_FULL_PATH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_full_dataset_in_batches(batch_size=1000):
    """
    Load full Hugging Face dataset in batches.
    
    Args:
        batch_size: Number of records to insert per batch
    """
    logger.info("=" * 80)
    logger.info("LOADING FULL HUGGING FACE DATASET")
    logger.info("=" * 80)
    
    try:
        # Step 1: Fetch data from Hugging Face
        logger.info("\n[1/4] Fetching data from Hugging Face...")
        df_raw = load_restaurant_dataset()
        original_count = len(df_raw)
        logger.info(f"✅ Fetched {original_count:,} records")
        
        # Step 2: Clean and preprocess data
        logger.info("\n[2/4] Cleaning and preprocessing data...")
        df_clean = clean_restaurant_data(df_raw)
        cleaned_count = len(df_clean)
        removed_count = original_count - cleaned_count
        retention_rate = (cleaned_count / original_count * 100) if original_count > 0 else 0
        
        logger.info(f"✅ Cleaned to {cleaned_count:,} valid records")
        logger.info(f"   - Removed: {removed_count:,} records")
        logger.info(f"   - Retention rate: {retention_rate:.1f}%")
        
        # Step 3: Remove old database
        logger.info("\n[3/4] Preparing database...")
        if DB_FULL_PATH.exists():
            DB_FULL_PATH.unlink()
            logger.info(f"✅ Removed old database: {DB_FULL_PATH}")
        
        # Step 4: Store data in batches
        logger.info(f"\n[4/4] Storing {cleaned_count:,} records in batches of {batch_size}...")
        
        store = RestaurantStore()
        store.create_tables()
        
        total_batches = (cleaned_count + batch_size - 1) // batch_size
        
        for i in range(0, cleaned_count, batch_size):
            batch_num = (i // batch_size) + 1
            batch = df_clean.iloc[i:i+batch_size]
            
            # First batch replaces, subsequent batches append
            replace = (i == 0)
            store.store_restaurants(batch, replace=replace)
            
            progress = min(i + batch_size, cleaned_count)
            percentage = (progress / cleaned_count * 100)
            logger.info(f"   Batch {batch_num}/{total_batches}: {progress:,}/{cleaned_count:,} ({percentage:.1f}%)")
        
        logger.info(f"✅ Successfully stored {cleaned_count:,} restaurants")
        
        # Step 5: Verify and get statistics
        logger.info("\n" + "=" * 80)
        logger.info("DATABASE STATISTICS")
        logger.info("=" * 80)
        
        stats = store.get_stats()
        logger.info(f"Total Restaurants: {stats['total_restaurants']:,}")
        logger.info(f"Unique Cuisines: {stats['unique_cuisines']}")
        logger.info(f"Unique Locations: {stats['unique_locations']}")
        
        # Sample query
        logger.info("\n" + "=" * 80)
        logger.info("SAMPLE QUERY: Top 5 restaurants in Koramangala")
        logger.info("=" * 80)
        
        sample = store.filter_restaurants(location='koramangala', min_rating=4.0)[:5]
        if sample:
            for idx, restaurant in enumerate(sample, 1):
                logger.info(f"{idx}. {restaurant['name']}")
                logger.info(f"   Cuisine: {restaurant['cuisine']}, Rating: {restaurant['rating']}, Price: ₹{restaurant['price']}")
        else:
            logger.info("No restaurants found in Koramangala")
        
        store.close()
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ FULL DATASET LOADED SUCCESSFULLY!")
        logger.info("=" * 80)
        logger.info(f"\nDatabase location: {DB_FULL_PATH}")
        logger.info(f"Total records: {cleaned_count:,}")
        logger.info("\nNext steps:")
        logger.info("1. Update .env files to use 'restaurant.db'")
        logger.info("2. Restart API server")
        logger.info("3. Test with real Bangalore locations!")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Error loading dataset: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    success = load_full_dataset_in_batches(batch_size=1000)
    sys.exit(0 if success else 1)
