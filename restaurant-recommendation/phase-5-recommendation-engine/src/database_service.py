"""Database service for accessing Phase 1 restaurant data."""

import sqlite3
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for querying restaurant database from Phase 1."""
    
    def __init__(self, db_path: str):
        """
        Initialize database service.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._validate_database()
        logger.info(f"Database service initialized with path: {db_path}")
        logger.info("DATABASE SERVICE VERSION: 2.0 - PARTIAL MATCH ENABLED")
    
    def _validate_database(self) -> None:
        """Validate that database exists and is accessible."""
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Database not found at: {self.db_path}")
        
        # Test connection
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='restaurants'")
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                raise ValueError("Database does not contain 'restaurants' table")
                
        except sqlite3.Error as e:
            raise ValueError(f"Database validation failed: {e}")
    
    def filter_restaurants(
        self,
        cuisine: Optional[str] = None,
        location: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_price: Optional[float] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Filter restaurants based on preferences.
        
        Args:
            cuisine: Cuisine type filter
            location: Location filter
            min_rating: Minimum rating filter
            max_price: Maximum price filter
            limit: Maximum number of results
            
        Returns:
            List of restaurant dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM restaurants WHERE 1=1"
        params = []
        
        if cuisine:
            query += " AND LOWER(cuisine) LIKE LOWER(?)"
            params.append(f"%{cuisine}%")
            logger.info(f"Cuisine filter applied: LIKE '%{cuisine}%'")
        
        if location:
            query += " AND LOWER(location) LIKE LOWER(?)"
            params.append(f"%{location}%")
        
        if min_rating is not None:
            query += " AND rating >= ?"
            params.append(min_rating)
        
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        
        # Add ordering and limit
        query += " ORDER BY rating DESC, price ASC LIMIT ?"
        params.append(limit)
        
        logger.debug(f"Executing query: {query} with params: {params}")
        
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            restaurants = [dict(row) for row in rows]
            
            logger.info(f"Found {len(restaurants)} restaurants matching filters")
            return restaurants
            
        except sqlite3.Error as e:
            logger.error(f"Database query failed: {e}")
            raise
        finally:
            conn.close()
    
    def get_all_restaurants(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Get all restaurants from database.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of restaurant dictionaries
        """
        return self.filter_restaurants(limit=limit)
    
    def get_restaurant_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific restaurant by name.
        
        Args:
            name: Restaurant name
            
        Returns:
            Restaurant dictionary or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM restaurants WHERE LOWER(name) = LOWER(?)",
                (name,)
            )
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except sqlite3.Error as e:
            logger.error(f"Database query failed: {e}")
            raise
        finally:
            conn.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total count
            cursor.execute("SELECT COUNT(*) FROM restaurants")
            total_count = cursor.fetchone()[0]
            
            # Unique cuisines
            cursor.execute("SELECT COUNT(DISTINCT cuisine) FROM restaurants")
            unique_cuisines = cursor.fetchone()[0]
            
            # Unique locations
            cursor.execute("SELECT COUNT(DISTINCT location) FROM restaurants")
            unique_locations = cursor.fetchone()[0]
            
            # Average rating
            cursor.execute("SELECT AVG(rating) FROM restaurants")
            avg_rating = cursor.fetchone()[0]
            
            # Average price
            cursor.execute("SELECT AVG(price) FROM restaurants")
            avg_price = cursor.fetchone()[0]
            
            return {
                'total_restaurants': total_count,
                'unique_cuisines': unique_cuisines,
                'unique_locations': unique_locations,
                'average_rating': round(avg_rating, 2) if avg_rating else 0,
                'average_price': round(avg_price, 2) if avg_price else 0
            }
            
        except sqlite3.Error as e:
            logger.error(f"Failed to get stats: {e}")
            raise
        finally:
            conn.close()
