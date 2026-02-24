"""FastAPI application for restaurant recommendations."""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
from pathlib import Path

# Add Phase 5 to path
phase5_path = Path(__file__).parent.parent.parent / 'phase-5-recommendation-engine' / 'src'
sys.path.insert(0, str(phase5_path))

from src.config import API_VERSION, API_TITLE, API_DESCRIPTION
from src.models import (
    UserPreferences,
    RecommendationResponse,
    StatsResponse,
    ErrorResponse,
    Restaurant,
    EnrichedRecommendation
)

# Import Phase 5 Recommendation Engine
try:
    from recommendation_engine import RecommendationEngine, RecommendationEngineError
    # Don't import EngineConfig here - let recommendation_engine handle it internally
    PHASE5_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Phase 5 not available: {e}")
    PHASE5_AVAILABLE = False
    RecommendationEngine = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url=f"/api/{API_VERSION}/docs",
    redoc_url=f"/api/{API_VERSION}/redoc",
    openapi_url=f"/api/{API_VERSION}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation engine
if PHASE5_AVAILABLE:
    try:
        engine = RecommendationEngine()
        logger.info("Recommendation engine initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize recommendation engine: {e}")
        engine = None
else:
    engine = None
    logger.warning("Running without Phase 5 recommendation engine")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information."""
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "status": "running",
        "endpoints": {
            "recommendations": f"/api/{API_VERSION}/recommendations",
            "restaurants": f"/api/{API_VERSION}/restaurants",
            "stats": f"/api/{API_VERSION}/stats",
            "docs": f"/api/{API_VERSION}/docs"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    try:
        if engine:
            health = engine.health_check()
            return {
                "status": health.get('status', 'unknown'),
                "engine": health.get('engine', 'unknown'),
                "database": health.get('database', 'unknown'),
                "llm_service": health.get('llm_service', 'unknown'),
                "database_stats": health.get('database_stats', {})
            }
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "unhealthy",
                    "error": "Recommendation engine not available"
                }
            )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@app.post(
    f"/api/{API_VERSION}/recommendations",
    tags=["Recommendations"],
    summary="Get restaurant recommendations",
    description="Get personalized restaurant recommendations based on user preferences"
)
async def get_recommendations(preferences: UserPreferences):
    """
    Get restaurant recommendations based on user preferences.
    
    - **cuisine**: Filter by cuisine type (optional)
    - **location**: Filter by location (optional)
    - **min_rating**: Minimum rating threshold (optional, 0.0-5.0)
    - **max_price**: Maximum price threshold (optional)
    - **limit**: Maximum number of results (default: 10, max: 100)
    """
    try:
        logger.info(f"API: Received recommendation request: {preferences}")
        
        if not engine:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Recommendation engine not available"
            )
        
        # Convert Pydantic model to dict
        prefs_dict = preferences.model_dump(exclude_none=True)
        logger.info(f"API: Preferences dict: {prefs_dict}")
        
        # Get recommendations from Phase 5 engine
        result = engine.get_recommendations(prefs_dict)
        logger.info(f"API: Engine returned {result.get('total_found', 0)} results")
        
        if not result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": result.get('error'),
                    "details": result.get('details', []),
                    "warnings": result.get('warnings', [])
                }
            )
        
        return {
            "success": True,
            "count": result['returned'],
            "total_found": result['total_found'],
            "recommendations": result['recommendations'],
            "filters_applied": result['filters_applied'],
            "warnings": result.get('warnings', [])
        }
        
    except HTTPException:
        raise
    except RecommendationEngineError as e:
        logger.error(f"Recommendation engine error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recommendation engine error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get(
    f"/api/{API_VERSION}/restaurants",
    tags=["Restaurants"],
    summary="List all restaurants",
    description="Get a list of all restaurants in the database"
)
async def list_restaurants(limit: int = 50):
    """
    List all restaurants in the database.
    
    - **limit**: Maximum number of results (default: 50, max: 100)
    """
    try:
        if limit > 100:
            limit = 100
        
        results = db_service.get_all_restaurants(limit=limit)
        restaurants = [Restaurant(**r) for r in results]
        
        return {
            "success": True,
            "count": len(restaurants),
            "restaurants": restaurants
        }
        
    except Exception as e:
        logger.error(f"Error listing restaurants: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get(
    f"/api/{API_VERSION}/stats",
    response_model=StatsResponse,
    tags=["Statistics"],
    summary="Get database statistics",
    description="Get statistics about the restaurant database"
)
async def get_stats():
    """
    Get database statistics.
    
    Returns information about:
    - Total number of restaurants
    - Number of unique cuisines
    - Number of unique locations
    """
    try:
        if not engine:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Recommendation engine not available"
            )
        
        stats = engine.get_database_stats()
        return StatsResponse(**stats)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down API...")
    if engine:
        logger.info("Recommendation engine cleanup complete")
