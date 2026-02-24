"""Local data store module using SQLite."""

import logging
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import DB_FULL_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class Restaurant(Base):
    """Restaurant table model."""
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cuisine = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False, index=True)
    rating = Column(Float, nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    address = Column(String, nullable=True)  # Optional address field
    
    # Add any additional columns that might be in the dataset
    # These will be dynamically handled


class RestaurantStore:
    """SQLite-based restaurant data store."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize the restaurant store.
        
        Args:
            db_path: Path to SQLite database file. Defaults to config value.
        """
        self.db_path = db_path or DB_FULL_PATH
        
        # Ensure data directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create database engine
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        self.Session = sessionmaker(bind=self.engine)
        
        logger.info(f"Database initialized at: {self.db_path}")
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        Base.metadata.create_all(self.engine)
        logger.info("Database tables created")
    
    def store_restaurants(self, df: pd.DataFrame, replace: bool = True):
        """
        Store restaurant data in the database.
        
        Args:
            df: DataFrame containing cleaned restaurant data.
            replace: If True, replace existing data. If False, append.
        """
        if df.empty:
            logger.warning("No data to store - DataFrame is empty")
            return
        
        # Ensure required columns exist
        required_cols = ['name', 'cuisine', 'location', 'rating', 'price']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Store data using pandas to_sql for simplicity
        if_exists = 'replace' if replace else 'append'
        
        df.to_sql(
            'restaurants',
            self.engine,
            if_exists=if_exists,
            index=False,
            method='multi'
        )
        
        logger.info(f"Stored {len(df)} records in database")
        
        # Create indexes for better query performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes on commonly queried columns."""
        with self.engine.connect() as conn:
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_cuisine ON restaurants(cuisine)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_location ON restaurants(location)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_rating ON restaurants(rating)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_price ON restaurants(price)"))
                conn.commit()
                logger.info("Database indexes created")
            except Exception as e:
                logger.warning(f"Index creation warning: {e}")
    
    def filter_restaurants(
        self,
        cuisine: Optional[str] = None,
        location: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Dict]:
        """
        Filter restaurants based on criteria.
        
        Args:
            cuisine: Filter by cuisine type (case-insensitive).
            location: Filter by location (case-insensitive).
            min_rating: Minimum rating threshold.
            max_price: Maximum price threshold.
            
        Returns:
            List of restaurant dictionaries matching the criteria.
        """
        query = "SELECT * FROM restaurants WHERE 1=1"
        params = {}
        
        if cuisine:
            query += " AND LOWER(cuisine) LIKE LOWER(:cuisine)"
            params['cuisine'] = f"%{cuisine}%"
        
        if location:
            query += " AND LOWER(location) LIKE LOWER(:location)"
            params['location'] = f"%{location}%"
        
        if min_rating is not None:
            query += " AND rating >= :min_rating"
            params['min_rating'] = min_rating
        
        if max_price is not None:
            query += " AND price <= :max_price"
            params['max_price'] = max_price
        
        query += " ORDER BY rating DESC, price ASC"
        
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            columns = result.keys()
            rows = result.fetchall()
            
            return [dict(zip(columns, row)) for row in rows]
    
    def get_all(self) -> List[Dict]:
        """
        Get all restaurants from the database.
        
        Returns:
            List of all restaurant dictionaries.
        """
        query = "SELECT * FROM restaurants"
        
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()
            
            return [dict(zip(columns, row)) for row in rows]
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the stored restaurant data.
        
        Returns:
            Dictionary with statistics (total count, unique cuisines, unique locations).
        """
        with self.engine.connect() as conn:
            # Total count
            total_result = conn.execute(text("SELECT COUNT(*) as count FROM restaurants"))
            total_count = total_result.fetchone()[0]
            
            # Unique cuisines
            cuisine_result = conn.execute(text("SELECT COUNT(DISTINCT cuisine) as count FROM restaurants"))
            unique_cuisines = cuisine_result.fetchone()[0]
            
            # Unique locations
            location_result = conn.execute(text("SELECT COUNT(DISTINCT location) as count FROM restaurants"))
            unique_locations = location_result.fetchone()[0]
            
            return {
                'total_restaurants': total_count,
                'unique_cuisines': unique_cuisines,
                'unique_locations': unique_locations
            }
    
    def close(self):
        """Close database connection."""
        self.engine.dispose()
        logger.info("Database connection closed")
