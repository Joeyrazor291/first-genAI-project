"""Phase 4: LLM Integration Module."""

__version__ = "1.0.0"

from .llm_service import LLMService, LLMServiceError
from .config import LLMConfig
from .prompt_builder import PromptBuilder

__all__ = ['LLMService', 'LLMServiceError', 'LLMConfig', 'PromptBuilder']
