"""Main recommendation engine orchestrating all phases."""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add phase directories to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "phase-3-preference-processing" / "src"))
sys.path.insert(0, str(project_root / "phase-4-llm-integration" / "src"))

# Now we can import
try:
    from preference_processor import PreferenceProcessor, ValidationResult
    PHASE3_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Phase 3 not available: {e}")
    PHASE3_AVAILABLE = False
    PreferenceProcessor = None
    ValidationResult = None

try:
    from llm_service import LLMService, LLMServiceError
    from config import LLMConfig as Phase4Config
    PHASE4_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Phase 4 not available: {e}")
    PHASE4_AVAILABLE = False
    LLMService = None
    LLMServiceError = Exception
    Phase4Config = None

# Import Phase 5 config and database service using importlib to avoid conflicts
import sys
import importlib.util
from pathlib import Path

# Get the current file's directory
current_dir = Path(__file__).parent

# Load Phase 5 config module explicitly
config_path = current_dir / 'config.py'
spec = importlib.util.spec_from_file_location("phase5_config", config_path)
phase5_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase5_config)
EngineConfig = phase5_config.EngineConfig

# Load Phase 5 database_service module explicitly
db_path = current_dir / 'database_service.py'
spec = importlib.util.spec_from_file_location("phase5_database_service", db_path)
phase5_db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase5_db)
DatabaseService = phase5_db.DatabaseService


class RecommendationEngineError(Exception):
    """Base exception for recommendation engine errors."""
    pass


class RecommendationEngine:
    """
    Main recommendation engine that orchestrates the complete pipeline.
    
    Pipeline:
    1. Validate preferences (Phase 3)
    2. Filter restaurants from database (Phase 1)
    3. Generate LLM recommendations (Phase 4)
    4. Format and return response
    """
    
    def __init__(self, config: Optional[EngineConfig] = None):
        """
        Initialize recommendation engine.
        
        Args:
            config: Engine configuration. If None, loads from environment.
        """
        self.config = config or EngineConfig.from_env()
        self.config.validate()
        
        # Initialize components
        self.preference_processor = PreferenceProcessor()
        self.database_service = DatabaseService(self.config.phase1_db_path)
        
        # Initialize LLM service if Phase 4 is available
        if PHASE4_AVAILABLE and Phase4Config:
            try:
                # Use from_env() to properly load OpenRouter or Groq configuration
                llm_config = Phase4Config.from_env()
                self.llm_service = LLMService(config=llm_config)
                logger.info(f"LLM service initialized with provider: {llm_config.api_provider}")
            except ValueError as e:
                logger.warning(f"LLM service not initialized: {e}")
                self.llm_service = None
        else:
            self.llm_service = None
            if not PHASE4_AVAILABLE:
                logger.warning("LLM service not initialized (Phase 4 not available)")
        
        logger.info("Recommendation engine initialized")
    
    def get_recommendations(
        self,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get restaurant recommendations based on user preferences.
        
        Args:
            preferences: User preferences dictionary
            
        Returns:
            Dictionary with recommendations and metadata
            
        Raises:
            RecommendationEngineError: If recommendation generation fails
        """
        try:
            # Step 1: Validate and normalize preferences
            logger.info("Step 1: Validating preferences")
            validation_result = self.preference_processor.validate_and_normalize(preferences)
            
            if not validation_result.is_valid:
                return {
                    'success': False,
                    'error': 'Invalid preferences',
                    'details': validation_result.errors,
                    'warnings': validation_result.warnings
                }
            
            normalized_prefs = validation_result.normalized_preferences
            logger.info(f"Preferences validated: {normalized_prefs}")
            
            # Step 2: Filter restaurants from database
            logger.info("Step 2: Filtering restaurants from database")
            filtered_restaurants = self._filter_restaurants(normalized_prefs)
            
            if not filtered_restaurants:
                return {
                    'success': True,
                    'recommendations': [],
                    'returned': 0,
                    'total_found': 0,
                    'message': 'No restaurants found matching your preferences',
                    'filters_applied': self.preference_processor.get_filter_summary(normalized_prefs),
                    'warnings': validation_result.warnings
                }
            
            logger.info(f"Found {len(filtered_restaurants)} matching restaurants")
            
            # Step 3: Generate LLM recommendations
            logger.info("Step 3: Generating LLM recommendations")
            limit = normalized_prefs.get('limit', self.config.default_limit)
            
            if self.llm_service:
                try:
                    recommendations = self.llm_service.generate_recommendations(
                        preferences=normalized_prefs,
                        restaurants=filtered_restaurants,
                        limit=limit
                    )
                except LLMServiceError as e:
                    logger.warning(f"LLM service failed, using fallback: {e}")
                    recommendations = self.llm_service.generate_fallback_recommendations(
                        restaurants=filtered_restaurants,
                        limit=limit
                    )
            else:
                # No LLM service, use fallback
                logger.info("Using fallback recommendations (no LLM service)")
                recommendations = self._generate_fallback_recommendations(
                    filtered_restaurants, limit
                )
            
            # Step 4: Enrich recommendations with full restaurant data
            logger.info("Step 4: Enriching recommendations")
            enriched_recommendations = self._enrich_recommendations(
                recommendations, filtered_restaurants
            )
            
            # Step 5: Format response
            response = {
                'success': True,
                'recommendations': enriched_recommendations,
                'total_found': len(filtered_restaurants),
                'returned': len(enriched_recommendations),
                'filters_applied': self.preference_processor.get_filter_summary(normalized_prefs),
                'warnings': validation_result.warnings
            }
            
            logger.info(f"Successfully generated {len(enriched_recommendations)} recommendations")
            return response
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            raise RecommendationEngineError(f"Failed to generate recommendations: {e}")
    
    def _filter_restaurants(self, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter restaurants based on preferences."""
        logger.info(f"Filtering restaurants with preferences: {preferences}")
        results = self.database_service.filter_restaurants(
            cuisine=preferences.get('cuisine'),
            location=preferences.get('location'),
            min_rating=preferences.get('min_rating'),
            max_price=preferences.get('max_price'),
            limit=self.config.max_limit  # Get more than needed for LLM to choose from
        )
        logger.info(f"Database returned {len(results)} restaurants")
        
        # Deduplicate by name + location before passing to LLM
        seen = set()
        deduplicated = []
        for restaurant in results:
            key = (restaurant.get('name', '').lower(), restaurant.get('location', '').lower())
            if key not in seen:
                seen.add(key)
                deduplicated.append(restaurant)
        
        if len(deduplicated) < len(results):
            logger.info(f"Deduplicated {len(results) - len(deduplicated)} duplicate restaurants")
        
        return deduplicated
    
    def _generate_fallback_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Generate fallback recommendations without LLM."""
        # Sort by rating (descending) and take top N
        sorted_restaurants = sorted(
            restaurants,
            key=lambda r: (r.get('rating', 0), -r.get('price', float('inf'))),
            reverse=True
        )
        
        recommendations = []
        for restaurant in sorted_restaurants[:limit]:
            recommendations.append({
                'name': restaurant.get('name', 'Unknown'),
                'explanation': f"Highly rated restaurant with {restaurant.get('rating', 'N/A')}/5.0 stars"
            })
        
        return recommendations
    
    def _enrich_recommendations(
        self,
        recommendations: List[Dict[str, Any]],
        restaurants: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Enrich recommendations with full restaurant data."""
        # Create lookup dictionary
        restaurant_lookup = {r['name'].lower(): r for r in restaurants}
        
        # Deduplicate recommendations by name + location
        seen = set()
        enriched = []
        
        for rec in recommendations:
            name = rec.get('name', '')
            
            # Check if we've already added this restaurant
            name_lower = name.lower()
            if name_lower in seen:
                logger.info(f"Skipping duplicate recommendation: {name}")
                continue
            
            restaurant_data = restaurant_lookup.get(name_lower)
            
            if restaurant_data:
                location = restaurant_data.get('location', '').lower()
                # Create unique key with name + location
                unique_key = (name_lower, location)
                
                # Check if this exact restaurant (name + location) was already added
                if unique_key not in seen:
                    seen.add(unique_key)
                    enriched.append({
                        'name': restaurant_data.get('name'),
                        'cuisine': restaurant_data.get('cuisine'),
                        'location': restaurant_data.get('location'),
                        'rating': restaurant_data.get('rating'),
                        'price': restaurant_data.get('price'),
                        'explanation': rec.get('explanation', '')
                    })
            else:
                # Restaurant not found in database, include basic info
                if name_lower not in seen:
                    seen.add(name_lower)
                    enriched.append({
                        'name': name,
                        'explanation': rec.get('explanation', ''),
                        'note': 'Full details not available'
                    })
        
        if len(enriched) < len(recommendations):
            logger.info(f"Removed {len(recommendations) - len(enriched)} duplicate recommendations")
        
        return enriched
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with database statistics
        """
        return self.database_service.get_stats()
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check health of all components.
        
        Returns:
            Dictionary with health status
        """
        health = {
            'engine': 'healthy',
            'database': 'unknown',
            'llm_service': 'unknown',
            'preference_processor': 'healthy'
        }
        
        # Check database
        try:
            stats = self.database_service.get_stats()
            if stats['total_restaurants'] > 0:
                health['database'] = 'healthy'
                health['database_stats'] = stats
            else:
                health['database'] = 'unhealthy'
                health['database_error'] = 'No restaurants in database'
        except Exception as e:
            health['database'] = 'unhealthy'
            health['database_error'] = str(e)
        
        # Check LLM service
        if self.llm_service:
            try:
                llm_health = self.llm_service.health_check()
                health['llm_service'] = llm_health['status']
            except Exception as e:
                health['llm_service'] = 'unhealthy'
                health['llm_error'] = str(e)
        else:
            health['llm_service'] = 'not_configured'
        
        # Overall status
        if health['database'] == 'healthy':
            health['status'] = 'healthy'
        else:
            health['status'] = 'degraded'
        
        return health
