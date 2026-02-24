"""LLM service for restaurant recommendations using Groq or OpenRouter API."""

import json
import logging
import time
from typing import Dict, Any, List, Optional
from groq import Groq
from openai import OpenAI
from groq.types.chat import ChatCompletion

from config import LLMConfig
from prompt_builder import PromptBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Base exception for LLM service errors."""
    pass


class LLMService:
    """Service for generating restaurant recommendations using Groq or OpenRouter LLM."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize LLM service.
        
        Args:
            config: LLM configuration. If None, loads from environment.
        """
        self.config = config or LLMConfig.from_env()
        self.config.validate()
        
        # Initialize appropriate client based on provider
        if self.config.api_provider == "openrouter":
            self.client = OpenAI(
                api_key=self.config.api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://restaurant-recommendation.local",
                    "X-Title": "Restaurant Recommendation Engine"
                }
            )
            logger.info(f"LLM service initialized with OpenRouter: {self.config.model}")
        else:  # groq
            self.client = Groq(api_key=self.config.api_key)
            logger.info(f"LLM service initialized with Groq: {self.config.model}")
        
        self.prompt_builder = PromptBuilder()
        logger.info(f"Using provider: {self.config.api_provider}")
    
    def generate_recommendations(
        self,
        preferences: Dict[str, Any],
        restaurants: List[Dict[str, Any]],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate restaurant recommendations using LLM.
        
        Args:
            preferences: User preferences dictionary
            restaurants: List of candidate restaurants
            limit: Number of recommendations to generate
            
        Returns:
            List of recommendation dictionaries with 'name' and 'explanation'
            
        Raises:
            LLMServiceError: If recommendation generation fails after retries
        """
        if not restaurants:
            logger.warning("No restaurants provided for recommendations")
            return []
        
        # Build the prompt
        prompt = self.prompt_builder.build_recommendation_prompt(
            preferences, restaurants, limit
        )
        
        # Generate recommendations with retry logic
        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"Generating recommendations (attempt {attempt + 1}/{self.config.max_retries})")
                
                response = self._call_llm(prompt)
                recommendations = self._parse_response(response)
                
                logger.info(f"Successfully generated {len(recommendations)} recommendations")
                return recommendations
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < self.config.max_retries - 1:
                    # Exponential backoff
                    delay = self.config.retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("All retry attempts exhausted")
                    raise LLMServiceError(f"Failed to generate recommendations: {str(e)}")
        
        return []
    
    def _call_llm(self, prompt: str) -> ChatCompletion:
        """
        Call the Groq LLM API.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            ChatCompletion response from Groq
            
        Raises:
            Exception: If API call fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.prompt_builder.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                response_format={"type": "json_object"}
            )
            
            logger.debug(f"LLM API call successful")
            return response
            
        except Exception as e:
            logger.error(f"LLM API call failed: {str(e)}")
            raise
    
    def _parse_response(self, response: ChatCompletion) -> List[Dict[str, Any]]:
        """
        Parse LLM response into recommendation list.
        
        Args:
            response: ChatCompletion response from Groq
            
        Returns:
            List of recommendation dictionaries
            
        Raises:
            ValueError: If response cannot be parsed
        """
        try:
            # Extract content from response
            content = response.choices[0].message.content
            
            if not content:
                raise ValueError("Empty response from LLM")
            
            # Parse JSON response
            data = json.loads(content)
            
            # Handle different response formats
            if isinstance(data, list):
                recommendations = data
            elif isinstance(data, dict) and 'recommendations' in data:
                recommendations = data['recommendations']
            else:
                raise ValueError(f"Unexpected response format: {type(data)}")
            
            # Validate recommendation structure and deduplicate
            validated_recommendations = []
            seen = set()
            
            for rec in recommendations:
                if isinstance(rec, dict) and 'name' in rec and 'explanation' in rec:
                    name_lower = str(rec['name']).lower()
                    
                    # Skip if we've already seen this restaurant name
                    if name_lower in seen:
                        logger.info(f"Skipping duplicate from LLM response: {rec['name']}")
                        continue
                    
                    seen.add(name_lower)
                    validated_recommendations.append({
                        'name': str(rec['name']),
                        'explanation': str(rec['explanation'])
                    })
                else:
                    logger.warning(f"Skipping invalid recommendation: {rec}")
            
            return validated_recommendations
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise ValueError(f"Invalid JSON in LLM response: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to parse response: {str(e)}")
            raise ValueError(f"Failed to parse LLM response: {str(e)}")
    
    def generate_fallback_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate fallback recommendations without LLM (rule-based).
        
        Args:
            restaurants: List of candidate restaurants
            limit: Number of recommendations to generate
            
        Returns:
            List of recommendation dictionaries
        """
        logger.info("Generating fallback recommendations")
        
        if not restaurants:
            return []
        
        # Sort by rating (descending) and take top N
        sorted_restaurants = sorted(
            restaurants,
            key=lambda r: r.get('rating', 0),
            reverse=True
        )
        
        # Deduplicate by name + location
        seen = set()
        recommendations = []
        
        for restaurant in sorted_restaurants:
            name = restaurant.get('name', 'Unknown')
            location = restaurant.get('location', 'Unknown')
            key = (name.lower(), location.lower())
            
            if key not in seen:
                seen.add(key)
                recommendations.append({
                    'name': name,
                    'explanation': f"Highly rated restaurant with {restaurant.get('rating', 'N/A')}/5.0 stars"
                })
                
                if len(recommendations) >= limit:
                    break
        
        logger.info(f"Generated {len(recommendations)} fallback recommendations")
        return recommendations
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if LLM service is healthy.
        
        Returns:
            Dictionary with health status
        """
        try:
            # Try a simple API call
            test_response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=10
            )
            
            return {
                'status': 'healthy',
                'model': self.config.model,
                'api_accessible': True
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'model': self.config.model,
                'api_accessible': False,
                'error': str(e)
            }
