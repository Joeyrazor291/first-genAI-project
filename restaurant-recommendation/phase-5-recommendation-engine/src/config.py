"""Configuration management for Phase 5 Recommendation Engine."""

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from Phase 5's .env file
phase5_env = Path(__file__).parent.parent / '.env'
load_dotenv(phase5_env)


@dataclass
class EngineConfig:
    """Configuration for recommendation engine."""
    
    # Database path
    phase1_db_path: str
    
    # Recommendation settings
    default_limit: int = 10
    max_limit: int = 100
    min_rating_threshold: float = 0.0
    
    # Groq API settings (for Phase 4)
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    groq_temperature: float = 0.7
    groq_max_tokens: int = 1024
    
    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0
    
    @classmethod
    def from_env(cls) -> "EngineConfig":
        """Create configuration from environment variables."""
        # Get database path
        db_path = os.getenv("PHASE1_DB_PATH", "../phase-1-data-pipeline/data/restaurant.db")
        
        # Convert to absolute path if relative
        if not os.path.isabs(db_path):
            # Resolve relative to this file's directory
            config_dir = Path(__file__).parent.parent
            db_path = str((config_dir / db_path).resolve())
        
        return cls(
            phase1_db_path=db_path,
            default_limit=int(os.getenv("DEFAULT_LIMIT", "10")),
            max_limit=int(os.getenv("MAX_LIMIT", "100")),
            min_rating_threshold=float(os.getenv("MIN_RATING_THRESHOLD", "0.0")),
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            groq_temperature=float(os.getenv("GROQ_TEMPERATURE", "0.7")),
            groq_max_tokens=int(os.getenv("GROQ_MAX_TOKENS", "1024")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("RETRY_DELAY", "1.0"))
        )
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not self.phase1_db_path:
            raise ValueError("Database path cannot be empty")
        
        if self.default_limit < 1:
            raise ValueError("Default limit must be positive")
        
        if self.max_limit < self.default_limit:
            raise ValueError("Max limit must be >= default limit")
        
        if self.min_rating_threshold < 0:
            raise ValueError("Min rating threshold cannot be negative")
