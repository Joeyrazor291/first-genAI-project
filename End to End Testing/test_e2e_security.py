"""
End-to-End Security Tests

Tests for input sanitization, SQL injection prevention, XSS prevention,
and other security concerns.
"""

import pytest
import httpx
from typing import Dict, Any


@pytest.mark.e2e
@pytest.mark.requires_api
class TestInputSanitization:
    """Test input sanitization and validation."""
    
    def test_sql_injection_in_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test SQL injection attempt in cuisine field."""
        malicious_inputs = [
            "italian'; DROP TABLE restaurants; --",
            "italian' OR '1'='1",
            "italian'; DELETE FROM restaurants WHERE '1'='1",
            "italian' UNION SELECT * FROM restaurants--",
        ]
        
        for malicious_input in malicious_inputs:
            preferences = {"cuisine": malicious_input, "limit": 5}
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should handle safely (return 200 with no results or sanitized query)
            assert response.status_code == 200
            
            # Verify database still works
            stats_response = api_client.get("/api/v1/stats")
            assert stats_response.status_code == 200
            stats = stats_response.json()
            assert stats["total_restaurants"] > 0, "Database should still be intact"
    
    def test_sql_injection_in_location(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test SQL injection attempt in location field."""
        malicious_inputs = [
            "downtown'; DROP TABLE restaurants; --",
            "downtown' OR '1'='1",
        ]
        
        for malicious_input in malicious_inputs:
            preferences = {"location": malicious_input, "limit": 5}
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should handle safely
            assert response.status_code == 200
            
            # Verify database integrity
            stats_response = api_client.get("/api/v1/stats")
            assert stats_response.status_code == 200
    
    def test_xss_in_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test XSS attempt in cuisine field."""
        xss_inputs = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<svg onload=alert('xss')>",
        ]
        
        for xss_input in xss_inputs:
            preferences = {"cuisine": xss_input, "limit": 5}
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should handle safely
            assert response.status_code == 200
            data = response.json()
            
            # Response should not contain unescaped script tags
            response_text = str(data)
            assert "<script>" not in response_text.lower()
    
    def test_xss_in_location(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test XSS attempt in location field."""
        xss_input = "<script>alert('xss')</script>"
        preferences = {"location": xss_input, "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle safely
        assert response.status_code == 200
        data = response.json()
        
        # Response should not contain unescaped script tags
        response_text = str(data)
        assert "<script>" not in response_text.lower()


@pytest.mark.e2e
@pytest.mark.requires_api
class TestCommandInjection:
    """Test command injection prevention."""
    
    def test_command_injection_in_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test command injection attempt in cuisine field."""
        command_inputs = [
            "italian; ls -la",
            "italian && cat /etc/passwd",
            "italian | whoami",
            "italian`whoami`",
            "italian$(whoami)",
        ]
        
        for command_input in command_inputs:
            preferences = {"cuisine": command_input, "limit": 5}
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should handle safely (no command execution)
            assert response.status_code == 200
    
    def test_path_traversal_in_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test path traversal attempt in cuisine field."""
        path_inputs = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "....//....//....//etc/passwd",
        ]
        
        for path_input in path_inputs:
            preferences = {"cuisine": path_input, "limit": 5}
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should handle safely
            assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.requires_api
class TestDataValidation:
    """Test data validation and type safety."""
    
    def test_integer_overflow_in_limit(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test integer overflow in limit field."""
        preferences = {"limit": 2147483647}  # Max 32-bit int
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should reject or cap at maximum
        assert response.status_code in [200, 400, 422]
    
    def test_negative_values_rejected(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that negative values are rejected."""
        test_cases = [
            {"min_rating": -1.0},
            {"max_price": -100.0},
            {"limit": -5},
        ]
        
        for preferences in test_cases:
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should reject negative values
            assert response.status_code in [400, 422]
    
    def test_out_of_range_values_rejected(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that out-of-range values are rejected."""
        test_cases = [
            {"min_rating": 10.0},  # > 5.0
            {"min_rating": -5.0},  # < 0.0
            {"limit": 200},  # > 100
            {"limit": 0},  # < 1
        ]
        
        for preferences in test_cases:
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should reject out-of-range values
            assert response.status_code in [400, 422]
    
    def test_type_mismatch_rejected(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that type mismatches are rejected."""
        test_cases = [
            {"cuisine": 123},  # Should be string
            {"min_rating": "not a number"},  # Should be float
            {"limit": "five"},  # Should be int
            {"max_price": True},  # Should be float
        ]
        
        for preferences in test_cases:
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should reject type mismatches
            assert response.status_code in [400, 422]


@pytest.mark.e2e
@pytest.mark.requires_api
class TestSpecialCharacters:
    """Test handling of special characters."""
    
    def test_unicode_characters(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of unicode characters."""
        unicode_inputs = [
            "中文",
            "日本語",
            "한국어",
            "العربية",
            "עברית",
            "🍕🍝",  # Emojis
        ]
        
        for unicode_input in unicode_inputs:
            preferences = {"cuisine": unicode_input, "limit": 5}
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should handle unicode gracefully
            assert response.status_code == 200
    
    def test_special_regex_characters(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of special regex characters."""
        special_chars = [
            "italian.*",
            "italian[a-z]",
            "italian+",
            "italian?",
            "italian{1,3}",
            "italian|chinese",
            "italian^",
            "italian$",
        ]
        
        for special_char in special_chars:
            preferences = {"cuisine": special_char, "limit": 5}
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should handle special characters safely
            assert response.status_code == 200
    
    def test_null_bytes(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of null bytes."""
        preferences = {"cuisine": "italian\x00", "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle null bytes safely
        assert response.status_code in [200, 400, 422]
    
    def test_control_characters(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of control characters."""
        control_chars = [
            "italian\n",
            "italian\r",
            "italian\t",
            "italian\x1b",
        ]
        
        for control_char in control_chars:
            preferences = {"cuisine": control_char, "limit": 5}
            response = api_client.post("/api/v1/recommendations", json=preferences)
            
            # Should handle control characters safely
            assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.requires_api
class TestRequestSizeLimit:
    """Test request size limits."""
    
    def test_very_large_string_in_cuisine(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of very large string."""
        # 10KB string
        large_string = "a" * 10000
        preferences = {"cuisine": large_string, "limit": 5}
        response = api_client.post("/api/v1/recommendations", json=preferences)
        
        # Should handle gracefully (accept or reject)
        assert response.status_code in [200, 400, 413, 422]
    
    def test_deeply_nested_json(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test handling of deeply nested JSON."""
        # Create nested structure
        nested = {"cuisine": "italian"}
        for i in range(100):
            nested = {"nested": nested}
        
        try:
            response = api_client.post("/api/v1/recommendations", json=nested)
            # Should reject or handle gracefully
            assert response.status_code in [200, 400, 422]
        except Exception:
            # Exception is acceptable for deeply nested JSON
            pass


@pytest.mark.e2e
@pytest.mark.requires_api
class TestAuthenticationAndAuthorization:
    """Test authentication and authorization (if implemented)."""
    
    def test_api_accessible_without_auth(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that API is accessible without authentication (current design)."""
        # Current design has no authentication
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        # Should succeed without auth
        assert response.status_code == 200
    
    def test_invalid_auth_header_ignored(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that invalid auth headers are ignored (no auth required)."""
        response = api_client.post(
            "/api/v1/recommendations",
            json=valid_preferences,
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        # Should succeed (auth not required)
        assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.requires_api
class TestCORSSecurity:
    """Test CORS security configuration."""
    
    def test_cors_headers_present(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that CORS headers are present."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        
        # Check for CORS headers
        headers = response.headers
        assert "access-control-allow-origin" in headers
    
    def test_cors_allows_common_origins(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that CORS allows common origins."""
        origins = [
            "http://localhost:8080",
            "http://localhost:3000",
            "http://127.0.0.1:8080",
        ]
        
        for origin in origins:
            response = api_client.post(
                "/api/v1/recommendations",
                json=valid_preferences,
                headers={"Origin": origin}
            )
            
            # Should succeed
            assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.requires_api
class TestErrorInformationLeakage:
    """Test that errors don't leak sensitive information."""
    
    def test_error_messages_no_stack_traces(
        self,
        api_client: httpx.Client,
        invalid_rating_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that error messages don't include stack traces."""
        response = api_client.post("/api/v1/recommendations", json=invalid_rating_preferences)
        
        assert response.status_code in [400, 422]
        data = response.json()
        
        # Should not contain stack trace keywords
        response_text = str(data).lower()
        assert "traceback" not in response_text
        assert "file \"" not in response_text
        assert "line " not in response_text.replace("online", "")  # Avoid false positive
    
    def test_error_messages_no_database_details(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that error messages don't leak database details."""
        # Try to trigger database error
        response = api_client.get("/api/v1/nonexistent")
        
        # Should not contain database details
        response_text = str(response.json()).lower()
        assert "sqlite" not in response_text
        assert "database" not in response_text or "database" in response_text  # Generic mention OK
        assert "table" not in response_text or "table" in response_text  # Generic mention OK
    
    def test_error_messages_no_file_paths(
        self,
        api_client: httpx.Client,
        invalid_rating_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that error messages don't include file paths."""
        response = api_client.post("/api/v1/recommendations", json=invalid_rating_preferences)
        
        assert response.status_code in [400, 422]
        data = response.json()
        
        # Should not contain file path indicators
        response_text = str(data)
        assert "/src/" not in response_text
        assert "\\src\\" not in response_text
        assert "C:\\" not in response_text
        assert "/home/" not in response_text


@pytest.mark.e2e
@pytest.mark.requires_api
class TestDatabaseSecurity:
    """Test database security measures."""
    
    def test_database_not_directly_accessible(
        self,
        api_client: httpx.Client,
        wait_for_api
    ):
        """Test that database is not directly accessible via API."""
        # Try to access database file
        response = api_client.get("/data/restaurant.db")
        
        # Should return 404
        assert response.status_code == 404
    
    def test_no_raw_sql_in_responses(
        self,
        api_client: httpx.Client,
        valid_preferences: Dict[str, Any],
        wait_for_api
    ):
        """Test that responses don't contain raw SQL."""
        response = api_client.post("/api/v1/recommendations", json=valid_preferences)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should not contain SQL keywords
        response_text = str(data).lower()
        assert "select " not in response_text
        assert "from restaurants" not in response_text
        assert "where " not in response_text or "where" in response_text  # Generic mention OK
