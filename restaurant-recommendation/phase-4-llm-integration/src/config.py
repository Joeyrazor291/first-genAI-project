"""Configuration management for Phase 4 LLM Integration."""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# Load environment variables from multiple locations (if dotenv available)
try:
    from dotenv import load_dotenv
    
    # First try Phase 4 directory
    phase4_env = Path(__file__).parent.parent / ".env"
    if phase4_env.exists():
        load_dotenv(phase4_env)

    # Then try Phase 2 directory (for API server)
    phase2_env = Path(__file__).parent.parent.parent / "phase-2-recommendation-api" / ".env"
    if phase2_env.exists():
        load_dotenv(phase2_env)

    # Finally try Phase 5 directory
    phase5_env = Path(__file__).parent.parent.parent / "phase-5-recommendation-engine" / ".env"
    if phase5_env.exists():
        load_dotenv(phase5_env)

    # Also load from current working directory
    load_dotenv()
except ImportError:
    # dotenv not available (e.g., on Streamlit Cloud), skip .env loading
    pass


@dataclass
class LLMConfig:
    """Configuration for LLM integration."""
    
    # API settings
    api_key: str
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 1024
    api_provider: str = "groq"  # "groq" or "openrouter"
    
    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0
    
    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Create configuration from environment variables."""
        # Determine provider (default to groq for backward compatibility)
        provider = os.getenv("LLM_PROVIDER", "groq").lower()
        
        # Debug logging
        import sys
        print(f"DEBUG: LLM_PROVIDER env var = {provider}", file=sys.stderr)
        print(f"DEBUG: All env vars starting with LLM: {[(k, v[:20] if len(v) > 20 else v) for k, v in os.environ.items() if k.startswith('LLM') or k.startswith('OPENROUTER') or k.startswith('GROQ')]}", file=sys.stderr)
        
        if provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct")
            if not api_key:
                raise ValueError(
                    "OPENROUTER_API_KEY environment variable is required. "
                    "Please set it in your .env file."
                )
        else:  # groq (default)
            api_key = os.getenv("GROQ_API_KEY")
            model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
            if not api_key:
                raise ValueError(
                    "GROQ_API_KEY environment variable is required. "
                    "Please set it in your .env file."
                )
        
        return cls(
            api_key=api_key,
            model=model,
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1024")),
            api_provider=provider,
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("RETRY_DELAY", "1.0"))
        )
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not self.api_key:
            raise ValueError("API key cannot be empty")
        
        if self.api_provider not in ("groq", "openrouter"):
            raise ValueError("api_provider must be 'groq' or 'openrouter'")
        
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2")
        
        if self.max_tokens < 1:
            raise ValueError("Max tokens must be positive")
        
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
        
        if self.retry_delay < 0:
            raise ValueError("Retry delay cannot be negative")
