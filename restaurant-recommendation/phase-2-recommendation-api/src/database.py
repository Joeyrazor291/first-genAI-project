"""Database integration module - connects to Phase 1 database."""

import sys
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine Phase 1 path
phase1_path = Path(__file__).parent.parent.parent / 'phase-1-data-pipeline'
phase1_path = phase1_path.resolve()

# Add Phase 1 to path if not already there
if str(phase1_path) not in sys.path:
    sys.path.insert(0, str(phase1_path))

# Import RestaurantStore from Phase 1
# This will work because we added phase1_path to sys.path
from src.data.store import RestaurantStore

# Load Phase 2 environment config
load_dotenv()
BASE_DIR = Path(__file__).parent.parent
PHASE1_DB_PATH = os.getenv('PHASE1_DB_PATH', '../phase-1-data-pipeline/data/restaurant.db')
PHASE1_DB_FULL_PATH = BASE_DIR / PHASE1_DB_PATH


class DatabaseService:
    """Service for interacting with Phase 1 database."""
    
    def __init__(self, db_path: Path = None):
        """
        Initialize database service.
        
        Args:
            db_path: Path to Phase 1 database. Defaults to config value.
        """
        self.db_path = db_path or PHASE1_DB_FULL_PATH
        self._store = None
        logger.info(f"Database service initialized with path: {self.db_path}")
    
    @property
    def store(self) -> RestaurantStore:
        """Get or create RestaurantStore instance."""
        if self._store is None:
            if not self.db_path.exists():
                raise FileNotFoundError(
                    f"Phase 1 database not found at {self.db_path}. "
                    "Please run Phase 1 pipeline first: cd ../phase-1-data-pipeline && py -m src.main"
                )
            self._store = RestaurantStore(db_path=self.db_path)
        return self._store
    
    def get_recommendations(
        self,
        cuisine: str = None,
        location: str = None,
        min_rating: float = None,
        max_price: float = None,
        limit: int = 10
    ) -> list:
        """
        Get restaurant recommendations based on filters.
        
        Args:
            cuisine: Filter by cuisine type.
            location: Filter by location.
            min_rating: Minimum rating threshold.
            max_price: Maximum price threshold.
            limit: Maximum number of results.
            
        Returns:
            List of restaurant dictionaries.
        """
        results = self.store.filter_restaurants(
            cuisine=cuisine,
            location=location,
            min_rating=min_rating,
            max_price=max_price
        )
        
        # Apply limit
        return results[:limit]
    
    def get_stats(self) -> dict:
        """
        Get database statistics.
        
        Returns:
            Dictionary with statistics.
        """
        return self.store.get_stats()
    
    def get_all_restaurants(self, limit: int = None) -> list:
        """
        Get all restaurants from database.
        
        Args:
            limit: Optional limit on number of results.
            
        Returns:
            List of restaurant dictionaries.
        """
        results = self.store.get_all()
        if limit:
            return results[:limit]
        return results
    
    def close(self):
        """Close database connection."""
        if self._store:
            self._store.close()
            self._store = None
            logger.info("Database connection closed")


# Global database service instance
db_service = DatabaseService()
