"""
Gemini API service wrapper
"""

import google.generativeai as genai
from typing import List, Optional, Dict, Any
from config.settings import settings
from models.schemas import Message, MessageRole, APIResponse
from utils.logger import logger


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini service"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.current_model = settings.GEMINI_MODEL
    
    def set_model(self, model_name: str) -> None:
        """
        Set the current model to use
        
        Args:
            model_name: Name of the model to use
        """
        self.current_model = model_name
        logger.info(f"Model changed to: {model_name}")
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        model_name: Optional[str] = None
    ) -> APIResponse:
        """
        Generate response from Gemini API
        
        Args:
            user_message: User's input message
            conversation_history: Previous conversation history
            system_prompt: Optional system prompt
            model_name: Optional model name to use
            
        Returns:
            APIResponse containing the generated response
        """
        try:
            # Use provided model or current model
            model_to_use = model_name or self.current_model
            
            # Create model instance
            model = genai.GenerativeModel(model_to_use)
            
            # Prepare chat history for the API
            chat_history = self._prepare_chat_history(conversation_history, system_prompt)
            
            # Debug logging
            logger.debug(f"Chat history count: {len(chat_history)}")
            if chat_history:
                logger.debug(f"Last message role: {chat_history[-1].get('role', 'unknown')}")
            
            # Start chat session
            chat = model.start_chat(history=chat_history)
            
            # Send message and get response
            response = chat.send_message(
                user_message,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.TEMPERATURE,
                    top_p=settings.TOP_P,
                    top_k=settings.TOP_K,
                    max_output_tokens=2048,
                )
            )
            
            assistant_message = response.text
            
            logger.info(f"Generated response successfully (model: {model_to_use}, length: {len(assistant_message)})")
            
            return APIResponse(
                status="success",
                data=assistant_message,
                metadata={"model": model_to_use}
            )
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return APIResponse(
                status="error",
                error=f"Failed to generate response: {str(e)}"
            )
    
    def _prepare_chat_history(
        self,
        conversation_history: List[Dict[str, Any]],
        system_prompt: Optional[str]
    ) -> List[Dict[str, Any]]:
        """
        Prepare chat history for Gemini API
        
        Args:
            conversation_history: Raw conversation history
            system_prompt: System prompt to include
            
        Returns:
            Formatted chat history
        """
        # Filter to remove incomplete entries and format properly
        history = []
        
        for msg in conversation_history:
            if "role" in msg and "parts" in msg:
                history.append(msg)
        
        return history
    
    def stream_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        model_name: Optional[str] = None
    ):
        """
        Stream response from Gemini API
        
        Args:
            user_message: User's input message
            conversation_history: Previous conversation history
            model_name: Optional model name to use
            
        Yields:
            Response chunks
        """
        try:
            # Use provided model or current model
            model_to_use = model_name or self.current_model
            
            # Create model instance
            model = genai.GenerativeModel(model_to_use)
            
            chat_history = self._prepare_chat_history(conversation_history, None)
            chat = model.start_chat(history=chat_history)
            
            response = chat.send_message(
                user_message,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.TEMPERATURE,
                    top_p=settings.TOP_P,
                    top_k=settings.TOP_K,
                )
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Error streaming response: {str(e)}")
            yield f"Error: {str(e)}"
    
    def get_model_info(self) -> APIResponse:
        """
        Get information about the Gemini model
        
        Returns:
            APIResponse with model information
        """
        try:
            info = {
                "model": settings.GEMINI_MODEL,
                "temperature": settings.TEMPERATURE,
                "top_p": settings.TOP_P,
                "top_k": settings.TOP_K,
            }
            return APIResponse(status="success", data=info)
        except Exception as e:
            return APIResponse(status="error", error=str(e))
    
    def list_available_models(self) -> APIResponse:
        """
        List all available Gemini models from API
        
        Returns:
            APIResponse with list of available models
        """
        try:
            models = genai.list_models()
            
            # Filter for generative models that support generateContent
            available_models = []
            for model in models:
                # Check if model supports generateContent
                if "generateContent" in model.supported_generation_methods:
                    available_models.append({
                        "name": model.name.split("/")[-1],  # Remove "models/" prefix
                        "display_name": model.display_name,
                        "description": model.description,
                        "input_token_limit": model.input_token_limit,
                        "output_token_limit": model.output_token_limit,
                    })
            
            logger.info(f"Found {len(available_models)} available models")
            
            return APIResponse(
                status="success",
                data=available_models
            )
            
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return APIResponse(
                status="error",
                error=f"Failed to fetch models: {str(e)}",
                data=[
                    {"name": "gemini-pro", "display_name": "Gemini Pro"},
                    {"name": "gemini-2.5-pro", "display_name": "Gemini 2.5 Pro"},
                    {"name": "gemini-2.5-flash", "display_name": "Gemini 2.5 Flash"},
                ]
            )
