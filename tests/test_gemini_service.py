"""
Test suite for Gemini service
"""

import pytest
from services.gemini_service import GeminiService
from models.schemas import APIResponse


class TestGeminiService:
    """Test cases for GeminiService"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = GeminiService()
    
    def test_service_initialization(self):
        """Test that service initializes correctly"""
        assert self.service is not None
        assert self.service.model is not None
    
    def test_get_model_info(self):
        """Test getting model information"""
        response = self.service.get_model_info()
        assert isinstance(response, APIResponse)
        assert response.is_success()
        assert "model" in response.data
    
    def test_prepare_chat_history(self):
        """Test chat history preparation"""
        history = [
            {"role": "user", "parts": [{"text": "Hello"}]},
            {"role": "assistant", "parts": [{"text": "Hi there!"}]}
        ]
        
        prepared = self.service._prepare_chat_history(history, None)
        assert len(prepared) == 2
        assert prepared[0]["role"] == "user"
    
    # Add more tests as needed
