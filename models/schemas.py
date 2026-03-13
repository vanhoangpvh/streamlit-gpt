"""
Data models and schemas for the application
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """Represents a chat message"""
    content: str
    role: MessageRole
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "content": self.content,
            "role": self.role.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class ChatSession:
    """Represents a chat session"""
    session_id: str
    title: str
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def add_message(self, message: Message) -> None:
        """Add a message to the session"""
        self.messages.append(message)
        self.updated_at = datetime.now()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history in Gemini API format"""
        history = []
        for msg in self.messages:
            # Skip system messages - Gemini API only supports "user" and "model"
            if msg.role == MessageRole.SYSTEM:
                continue
            
            # Convert role to Gemini API format
            # Gemini expects "user" and "model", not "assistant"
            role = msg.role.value
            if role == "assistant":
                role = "model"
            
            history.append({
                "role": role,
                "parts": [{"text": msg.content}]
            })
        return history


@dataclass
class APIResponse:
    """Standard API response structure"""
    status: str
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_success(self) -> bool:
        """Check if response is successful"""
        return self.status == "success"
