"""Tests for LLM service module."""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.llm_service import LLMService, LLMServiceError
from src.config import LLMConfig


class TestLLMServiceInitialization:
    """Test cases for LLM service initialization."""
    
    def test_initialization_with_config(self):
        """Test initialization with provided config."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        assert service.config == config
        assert service.client is not None
        assert service.prompt_builder is not None
    
    def test_initialization_without_config(self, monkeypatch):
        """Test initialization without config (loads from env)."""
        monkeypatch.setenv("GROQ_API_KEY", "env_test_key")
        
        service = LLMService()
        
        assert service.config.api_key == "env_test_key"
        assert service.client is not None


class TestGenerateRecommendations:
    """Test cases for recommendation generation."""
    
    @patch('src.llm_service.Groq')
    def test_generate_recommendations_success(
        self, mock_groq_class, sample_preferences, sample_restaurants, mock_groq_response
    ):
        """Test successful recommendation generation."""
        # Setup mock
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_groq_response
        mock_groq_class.return_value = mock_client
        
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        # Generate recommendations
        recommendations = service.generate_recommendations(
            sample_preferences, sample_restaurants, limit=3
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all('name' in rec for rec in recommendations)
        assert all('explanation' in rec for rec in recommendations)
    
    @patch('src.llm_service.Groq')
    def test_generate_recommendations_empty_restaurants(
        self, mock_groq_class, sample_preferences, empty_restaurants
    ):
        """Test recommendation generation with empty restaurant list."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        recommendations = service.generate_recommendations(
            sample_preferences, empty_restaurants, limit=5
        )
        
        assert recommendations == []
    
    @patch('src.llm_service.Groq')
    def test_generate_recommendations_api_failure_with_retry(
        self, mock_groq_class, sample_preferences, sample_restaurants
    ):
        """Test recommendation generation with API failure and retry."""
        # Setup mock to fail then succeed
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [
            Exception("API Error"),
            Exception("API Error"),
            Mock(choices=[Mock(message=Mock(content='{"recommendations": []}'))])
        ]
        mock_groq_class.return_value = mock_client
        
        config = LLMConfig(api_key="test_key", max_retries=3, retry_delay=0.1)
        service = LLMService(config=config)
        
        # Should succeed after retries
        recommendations = service.generate_recommendations(
            sample_preferences, sample_restaurants, limit=5
        )
        
        assert isinstance(recommendations, list)
        assert mock_client.chat.completions.create.call_count == 3
    
    @patch('src.llm_service.Groq')
    def test_generate_recommendations_all_retries_fail(
        self, mock_groq_class, sample_preferences, sample_restaurants
    ):
        """Test recommendation generation when all retries fail."""
        # Setup mock to always fail
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_groq_class.return_value = mock_client
        
        config = LLMConfig(api_key="test_key", max_retries=2, retry_delay=0.1)
        service = LLMService(config=config)
        
        # Should raise LLMServiceError
        with pytest.raises(LLMServiceError) as exc_info:
            service.generate_recommendations(
                sample_preferences, sample_restaurants, limit=5
            )
        
        assert "Failed to generate recommendations" in str(exc_info.value)


class TestCallLLM:
    """Test cases for LLM API calls."""
    
    @patch('src.llm_service.Groq')
    def test_call_llm_success(self, mock_groq_class, mock_groq_response):
        """Test successful LLM API call."""
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_groq_response
        mock_groq_class.return_value = mock_client
        
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        response = service._call_llm("test prompt")
        
        assert response == mock_groq_response
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('src.llm_service.Groq')
    def test_call_llm_with_correct_parameters(self, mock_groq_class):
        """Test that LLM is called with correct parameters."""
        mock_client = Mock()
        mock_groq_class.return_value = mock_client
        
        config = LLMConfig(
            api_key="test_key",
            model="test-model",
            temperature=0.5,
            max_tokens=512
        )
        service = LLMService(config=config)
        
        service._call_llm("test prompt")
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs['model'] == "test-model"
        assert call_args.kwargs['temperature'] == 0.5
        assert call_args.kwargs['max_tokens'] == 512
    
    @patch('src.llm_service.Groq')
    def test_call_llm_failure(self, mock_groq_class):
        """Test LLM API call failure."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_groq_class.return_value = mock_client
        
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        with pytest.raises(Exception) as exc_info:
            service._call_llm("test prompt")
        
        assert "API Error" in str(exc_info.value)


class TestParseResponse:
    """Test cases for response parsing."""
    
    @patch('src.llm_service.Groq')
    def test_parse_response_list_format(self, mock_groq_class):
        """Test parsing response in list format."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        # Create mock response with list format
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps([
            {'name': 'Restaurant 1', 'explanation': 'Great food'},
            {'name': 'Restaurant 2', 'explanation': 'Nice ambiance'}
        ])))]
        
        recommendations = service._parse_response(mock_response)
        
        assert len(recommendations) == 2
        assert recommendations[0]['name'] == 'Restaurant 1'
        assert recommendations[1]['name'] == 'Restaurant 2'
    
    @patch('src.llm_service.Groq')
    def test_parse_response_dict_format(self, mock_groq_class, mock_llm_response):
        """Test parsing response in dict format with 'recommendations' key."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        # Create mock response with dict format
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps(mock_llm_response)))]
        
        recommendations = service._parse_response(mock_response)
        
        assert len(recommendations) == 3
        assert all('name' in rec for rec in recommendations)
        assert all('explanation' in rec for rec in recommendations)
    
    @patch('src.llm_service.Groq')
    def test_parse_response_empty_content(self, mock_groq_class):
        """Test parsing response with empty content."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=''))]
        
        with pytest.raises(ValueError) as exc_info:
            service._parse_response(mock_response)
        
        assert "Empty response" in str(exc_info.value)
    
    @patch('src.llm_service.Groq')
    def test_parse_response_invalid_json(self, mock_groq_class):
        """Test parsing response with invalid JSON."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='not valid json'))]
        
        with pytest.raises(ValueError) as exc_info:
            service._parse_response(mock_response)
        
        assert "Invalid JSON" in str(exc_info.value)
    
    @patch('src.llm_service.Groq')
    def test_parse_response_malformed_recommendations(
        self, mock_groq_class, malformed_recommendations
    ):
        """Test parsing response with malformed recommendations."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps(malformed_recommendations)))]
        
        recommendations = service._parse_response(mock_response)
        
        # Should only include valid recommendations
        assert len(recommendations) == 1
        assert recommendations[0]['name'] == 'Restaurant 3'
    
    @patch('src.llm_service.Groq')
    def test_parse_response_unexpected_format(self, mock_groq_class):
        """Test parsing response with unexpected format."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"unexpected": "format"}'))]
        
        with pytest.raises(ValueError) as exc_info:
            service._parse_response(mock_response)
        
        assert "Unexpected response format" in str(exc_info.value)


class TestFallbackRecommendations:
    """Test cases for fallback recommendations."""
    
    @patch('src.llm_service.Groq')
    def test_generate_fallback_recommendations(
        self, mock_groq_class, sample_restaurants
    ):
        """Test generating fallback recommendations."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        recommendations = service.generate_fallback_recommendations(
            sample_restaurants, limit=3
        )
        
        assert len(recommendations) == 3
        assert all('name' in rec for rec in recommendations)
        assert all('explanation' in rec for rec in recommendations)
    
    @patch('src.llm_service.Groq')
    def test_fallback_recommendations_sorted_by_rating(
        self, mock_groq_class, sample_restaurants
    ):
        """Test that fallback recommendations are sorted by rating."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        recommendations = service.generate_fallback_recommendations(
            sample_restaurants, limit=5
        )
        
        # First recommendation should be highest rated
        assert recommendations[0]['name'] == 'Trattoria Roma'  # 4.7 rating
    
    @patch('src.llm_service.Groq')
    def test_fallback_recommendations_empty_list(
        self, mock_groq_class, empty_restaurants
    ):
        """Test fallback recommendations with empty restaurant list."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        recommendations = service.generate_fallback_recommendations(
            empty_restaurants, limit=5
        )
        
        assert recommendations == []
    
    @patch('src.llm_service.Groq')
    def test_fallback_recommendations_limit_respected(
        self, mock_groq_class, sample_restaurants
    ):
        """Test that fallback recommendations respect limit."""
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        recommendations = service.generate_fallback_recommendations(
            sample_restaurants, limit=2
        )
        
        assert len(recommendations) == 2


class TestHealthCheck:
    """Test cases for health check."""
    
    @patch('src.llm_service.Groq')
    def test_health_check_success(self, mock_groq_class):
        """Test successful health check."""
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = Mock()
        mock_groq_class.return_value = mock_client
        
        config = LLMConfig(api_key="test_key", model="test-model")
        service = LLMService(config=config)
        
        health = service.health_check()
        
        assert health['status'] == 'healthy'
        assert health['model'] == 'test-model'
        assert health['api_accessible'] is True
    
    @patch('src.llm_service.Groq')
    def test_health_check_failure(self, mock_groq_class):
        """Test health check failure."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Down")
        mock_groq_class.return_value = mock_client
        
        config = LLMConfig(api_key="test_key")
        service = LLMService(config=config)
        
        health = service.health_check()
        
        assert health['status'] == 'unhealthy'
        assert health['api_accessible'] is False
        assert 'error' in health
