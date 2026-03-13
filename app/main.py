"""
Main entry point for Streamlit Gemini App
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import settings
from ui.chat_interface import ChatInterface
from utils.logger import logger


def main():
    """Main application entry point"""
    try:
        # Validate settings
        settings.validate()
        
        logger.info("Starting Streamlit Gemini Application")
        
        # Initialize and run chat interface
        chat_interface = ChatInterface()
        chat_interface.run()
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
