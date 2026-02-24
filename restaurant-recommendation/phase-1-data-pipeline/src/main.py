"""Main entry point for Phase 1 data pipeline."""

import logging
from src.data.ingestion import load_restaurant_dataset
from src.data.preprocessing import clean_restaurant_data, get_cleaning_summary
from src.data.store import RestaurantStore
from src.config import LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run the complete Phase 1 data pipeline."""
    
    logger.info("=" * 80)
    logger.info("PHASE 1: DATA PIPELINE - AI RESTAURANT RECOMMENDATION SERVICE")
    logger.info("=" * 80)
    
    try:
        # Step 1: Ingest data from Hugging Face
        logger.info("\n[STEP 1] Loading dataset from Hugging Face...")
        raw_df = load_restaurant_dataset()
        original_count = len(raw_df)
        
        # Step 2: Clean and normalize data
        logger.info("\n[STEP 2] Cleaning and normalizing data...")
        cleaned_df = clean_restaurant_data(raw_df)
        cleaned_count = len(cleaned_df)
        
        # Step 3: Store in local database
        logger.info("\n[STEP 3] Storing data in SQLite database...")
        store = RestaurantStore()
        store.create_tables()
        store.store_restaurants(cleaned_df)
        
        # Step 4: Generate summary report
        logger.info("\n" + "=" * 80)
        logger.info("PIPELINE SUMMARY REPORT")
        logger.info("=" * 80)
        
        cleaning_summary = get_cleaning_summary(original_count, cleaned_count)
        logger.info(f"\nData Processing:")
        logger.info(f"  - Total records loaded: {cleaning_summary['original_count']}")
        logger.info(f"  - Records after cleaning: {cleaning_summary['cleaned_count']}")
        logger.info(f"  - Records removed: {cleaning_summary['removed_count']}")
        logger.info(f"  - Retention rate: {cleaning_summary['retention_rate']}")
        
        # Get database statistics
        stats = store.get_stats()
        logger.info(f"\nDatabase Statistics:")
        logger.info(f"  - Records stored in DB: {stats['total_restaurants']}")
        logger.info(f"  - Unique cuisines: {stats['unique_cuisines']}")
        logger.info(f"  - Unique locations: {stats['unique_locations']}")
        
        # Sample query: Top 5 Italian restaurants rated above 4.0
        logger.info(f"\nSample Query: Top 5 Italian restaurants rated above 4.0")
        sample_results = store.filter_restaurants(
            cuisine='italian',
            min_rating=4.0
        )[:5]
        
        if sample_results:
            logger.info(f"  Found {len(sample_results)} results:")
            for i, restaurant in enumerate(sample_results, 1):
                logger.info(f"    {i}. {restaurant['name']} - Rating: {restaurant['rating']}, "
                          f"Price: {restaurant['price']}, Location: {restaurant['location']}")
        else:
            logger.info("  No Italian restaurants found with rating above 4.0")
        
        # Alternative sample query if Italian doesn't exist
        if not sample_results:
            logger.info(f"\nAlternative Sample Query: Top 5 highest-rated restaurants")
            alt_results = store.filter_restaurants(min_rating=4.0)[:5]
            if alt_results:
                logger.info(f"  Found {len(alt_results)} results:")
                for i, restaurant in enumerate(alt_results, 1):
                    logger.info(f"    {i}. {restaurant['name']} - Rating: {restaurant['rating']}, "
                              f"Cuisine: {restaurant['cuisine']}, Location: {restaurant['location']}")
        
        logger.info("\n" + "=" * 80)
        logger.info("PHASE 1 PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
        store.close()
        
    except Exception as e:
        logger.error(f"\nPipeline failed with error: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
