"""
Configuration settings for Streamlit Gemini App
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    # Streamlit Configuration
    APP_TITLE: str = "Streamlit GPT"
    APP_ICON: str = "🤖"
    PAGE_LAYOUT: str = "wide"
    
    # Chat Configuration
    MAX_HISTORY_LENGTH: int = 50
    MAX_MESSAGE_LENGTH: int = 4000
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.95
    TOP_K: int = 40
    
    # UI Configuration
    SIDEBAR_WIDTH: int = 300
    MESSAGE_DISPLAY_LIMIT: int = 100
    
    # Debug Mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required settings"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in environment variables")
        return True


# Create settings instance
settings = Settings()
