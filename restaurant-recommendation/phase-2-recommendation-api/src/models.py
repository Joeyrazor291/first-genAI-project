"""Pydantic models for request/response validation."""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class UserPreferences(BaseModel):
    """User preference input model."""
    
    cuisine: Optional[str] = Field(None, description="Preferred cuisine type (e.g., 'italian', 'chinese')")
    location: Optional[str] = Field(None, description="Preferred location (e.g., 'downtown', 'uptown')")
    min_rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Minimum rating (0.0 to 5.0)")
    max_price: Optional[float] = Field(None, ge=0.0, description="Maximum price")
    limit: Optional[int] = Field(10, ge=1, le=100, description="Maximum number of results")
    
    @field_validator('cuisine', 'location')
    @classmethod
    def normalize_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """Normalize text fields to lowercase and strip whitespace."""
        if v is not None:
            return v.strip().lower()
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "cuisine": "italian",
                "location": "downtown",
                "min_rating": 4.0,
                "max_price": 30.0,
                "limit": 5
            }
        }


class Restaurant(BaseModel):
    """Restaurant model for API responses."""
    
    id: Optional[int] = Field(None, description="Restaurant ID")
    name: str = Field(..., description="Restaurant name")
    cuisine: str = Field(..., description="Cuisine type")
    location: str = Field(..., description="Location")
    rating: float = Field(..., ge=0.0, le=5.0, description="Rating (0.0 to 5.0)")
    price: float = Field(..., ge=0.0, description="Price")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Bella Italia",
                "cuisine": "italian",
                "location": "downtown",
                "rating": 4.5,
                "price": 25.50
            }
        }


class EnrichedRecommendation(BaseModel):
    """Enriched recommendation with explanation from LLM."""
    
    name: str = Field(..., description="Restaurant name")
    cuisine: Optional[str] = Field(None, description="Cuisine type")
    location: Optional[str] = Field(None, description="Location")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Rating (0.0 to 5.0)")
    price: Optional[float] = Field(None, ge=0.0, description="Price")
    explanation: str = Field(..., description="LLM-generated explanation for recommendation")
    note: Optional[str] = Field(None, description="Additional notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Bella Italia",
                "cuisine": "italian",
                "location": "downtown",
                "rating": 4.5,
                "price": 25.50,
                "explanation": "Highly rated Italian restaurant in downtown with excellent pasta dishes and great ambiance."
            }
        }


class RecommendationResponse(BaseModel):
    """Response model for recommendation requests."""
    
    success: bool = Field(..., description="Whether the request was successful")
    count: int = Field(..., description="Number of recommendations returned")
    recommendations: List[Restaurant] = Field(..., description="List of recommended restaurants")
    filters_applied: dict = Field(..., description="Filters that were applied")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "count": 2,
                "recommendations": [
                    {
                        "id": 1,
                        "name": "Bella Italia",
                        "cuisine": "italian",
                        "location": "downtown",
                        "rating": 4.5,
                        "price": 25.50
                    }
                ],
                "filters_applied": {
                    "cuisine": "italian",
                    "min_rating": 4.0
                }
            }
        }


class StatsResponse(BaseModel):
    """Response model for statistics endpoint."""
    
    total_restaurants: int = Field(..., description="Total number of restaurants in database")
    unique_cuisines: int = Field(..., description="Number of unique cuisine types")
    unique_locations: int = Field(..., description="Number of unique locations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_restaurants": 1000,
                "unique_cuisines": 25,
                "unique_locations": 15
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    success: bool = Field(False, description="Always False for errors")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Invalid input",
                "detail": "Rating must be between 0.0 and 5.0"
            }
        }
