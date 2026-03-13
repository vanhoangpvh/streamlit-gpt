"""
Chat service - Business logic for chat management
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from models.schemas import Message, MessageRole, ChatSession
from services.gemini_service import GeminiService
from config.constants import SESSION_KEY_MESSAGES, SESSION_KEY_CHAT_HISTORY
from utils.logger import logger


class ChatService:
    """Service for managing chat sessions and messages"""
    
    def __init__(self):
        """Initialize chat service"""
        self.gemini_service = GeminiService()
        self.sessions: Dict[str, ChatSession] = {}
    
    def create_session(self, title: str = "New Chat") -> ChatSession:
        """
        Create a new chat session
        
        Args:
            title: Session title
            
        Returns:
            New ChatSession instance
        """
        session_id = str(uuid.uuid4())
        session = ChatSession(session_id=session_id, title=title)
        self.sessions[session_id] = session
        
        logger.info(f"Created new chat session: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get a chat session by ID
        
        Args:
            session_id: Session ID
            
        Returns:
            ChatSession or None if not found
        """
        return self.sessions.get(session_id)
    
    def add_message(
        self,
        session_id: str,
        content: str,
        role: MessageRole
    ) -> Optional[Message]:
        """
        Add a message to a session
        
        Args:
            session_id: Session ID
            content: Message content
            role: Message role (user or assistant)
            
        Returns:
            Added Message or None if session not found
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        message = Message(content=content, role=role)
        session.add_message(message)
        
        return message
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            List of messages in Gemini API format
        """
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.get_conversation_history()
    
    async def process_user_message(
        self,
        session_id: str,
        user_message: str,
        system_prompt: Optional[str] = None
    ) -> Optional[str]:
        """
        Process user message and generate AI response
        
        Args:
            session_id: Session ID
            user_message: User's message
            system_prompt: Optional system prompt
            
        Returns:
            AI response or None if error occurred
        """
        # Add user message to session
        self.add_message(session_id, user_message, MessageRole.USER)
        
        # Get conversation history
        history = self.get_conversation_history(session_id)
        
        # Generate response using Gemini
        response = self.gemini_service.generate_response(
            user_message=user_message,
            conversation_history=history,
            system_prompt=system_prompt
        )
        
        if response.is_success():
            assistant_message = response.data
            # Add assistant message to session
            self.add_message(session_id, assistant_message, MessageRole.ASSISTANT)
            return assistant_message
        else:
            logger.error(f"Failed to generate response: {response.error}")
            return None
    
    def get_all_sessions(self) -> List[ChatSession]:
        """
        Get all chat sessions
        
        Returns:
            List of all ChatSession instances
        """
        return list(self.sessions.values())
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a chat session
        
        Args:
            session_id: Session ID
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted chat session: {session_id}")
            return True
        return False
    
    def export_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Export session as dictionary
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data as dictionary or None if not found
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session.session_id,
            "title": session.title,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "messages": [msg.to_dict() for msg in session.messages]
        }
