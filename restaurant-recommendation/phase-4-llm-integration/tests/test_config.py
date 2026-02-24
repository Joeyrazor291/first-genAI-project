"""Tests for configuration module."""

import pytest
import os
from src.config import LLMConfig


class TestLLMConfig:
    """Test cases for LLM configuration."""
    
    def test_config_creation_with_defaults(self):
        """Test creating config with default values."""
        config = LLMConfig(api_key="test_key")
        
        assert config.api_key == "test_key"
        assert config.model == "llama-3.3-70b-versatile"
        assert config.temperature == 0.7
        assert config.max_tokens == 1024
        assert config.max_retries == 3
        assert config.retry_delay == 1.0
    
    def test_config_creation_with_custom_values(self):
        """Test creating config with custom values."""
        config = LLMConfig(
            api_key="custom_key",
            model="custom-model",
            temperature=0.5,
            max_tokens=2048,
            max_retries=5,
            retry_delay=2.0
        )
        
        assert config.api_key == "custom_key"
        assert config.model == "custom-model"
        assert config.temperature == 0.5
        assert config.max_tokens == 2048
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
    
    def test_config_from_env(self, monkeypatch):
        """Test creating config from environment variables."""
        monkeypatch.setenv("GROQ_API_KEY", "env_key")
        monkeypatch.setenv("GROQ_MODEL", "env-model")
        monkeypatch.setenv("GROQ_TEMPERATURE", "0.8")
        monkeypatch.setenv("GROQ_MAX_TOKENS", "512")
        monkeypatch.setenv("MAX_RETRIES", "2")
        monkeypatch.setenv("RETRY_DELAY", "0.5")
        
        config = LLMConfig.from_env()
        
        assert config.api_key == "env_key"
        assert config.model == "env-model"
        assert config.temperature == 0.8
        assert config.max_tokens == 512
        assert config.max_retries == 2
        assert config.retry_delay == 0.5
    
    def test_config_from_env_missing_api_key(self, monkeypatch):
        """Test that missing API key raises error."""
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        
        with pytest.raises(ValueError) as exc_info:
            LLMConfig.from_env()
        
        assert "GROQ_API_KEY" in str(exc_info.value)
    
    def test_config_validation_empty_api_key(self):
        """Test validation fails for empty API key."""
        config = LLMConfig(api_key="")
        
        with pytest.raises(ValueError) as exc_info:
            config.validate()
        
        assert "API key cannot be empty" in str(exc_info.value)
    
    def test_config_validation_invalid_temperature_low(self):
        """Test validation fails for temperature < 0."""
        config = LLMConfig(api_key="test", temperature=-0.1)
        
        with pytest.raises(ValueError) as exc_info:
            config.validate()
        
        assert "Temperature must be between" in str(exc_info.value)
    
    def test_config_validation_invalid_temperature_high(self):
        """Test validation fails for temperature > 2."""
        config = LLMConfig(api_key="test", temperature=2.1)
        
        with pytest.raises(ValueError) as exc_info:
            config.validate()
        
        assert "Temperature must be between" in str(exc_info.value)
    
    def test_config_validation_invalid_max_tokens(self):
        """Test validation fails for max_tokens < 1."""
        config = LLMConfig(api_key="test", max_tokens=0)
        
        with pytest.raises(ValueError) as exc_info:
            config.validate()
        
        assert "Max tokens must be positive" in str(exc_info.value)
    
    def test_config_validation_invalid_max_retries(self):
        """Test validation fails for negative max_retries."""
        config = LLMConfig(api_key="test", max_retries=-1)
        
        with pytest.raises(ValueError) as exc_info:
            config.validate()
        
        assert "Max retries cannot be negative" in str(exc_info.value)
    
    def test_config_validation_invalid_retry_delay(self):
        """Test validation fails for negative retry_delay."""
        config = LLMConfig(api_key="test", retry_delay=-0.5)
        
        with pytest.raises(ValueError) as exc_info:
            config.validate()
        
        assert "Retry delay cannot be negative" in str(exc_info.value)
    
    def test_config_validation_success(self):
        """Test validation succeeds for valid config."""
        config = LLMConfig(api_key="test")
        
        # Should not raise any exception
        config.validate()
