"""
Chat interface logic
"""

import streamlit as st
from typing import Optional
from services.chat_service import ChatService
from services.gemini_service import GeminiService
from models.schemas import MessageRole
from config.constants import DEFAULT_SYSTEM_PROMPT, MSG_LOADING
from config.settings import settings
from ui.components import (
    display_chat_history,
    render_sidebar_session_management,
    render_settings_sidebar,
    render_error_message,
    render_success_message,
    render_info_message
)
from utils.logger import logger


class ChatInterface:
    """Main chat interface logic"""
    
    def __init__(self):
        """Initialize chat interface"""
        self._init_session_state()
        self.chat_service = st.session_state.chat_service
        self.gemini_service = st.session_state.gemini_service
    
    def _init_session_state(self) -> None:
        """Initialize Streamlit session state"""
        # Initialize ChatService once and persist in session state
        if "chat_service" not in st.session_state:
            st.session_state.chat_service = ChatService()
        
        # Initialize GeminiService once and persist in session state
        if "gemini_service" not in st.session_state:
            st.session_state.gemini_service = GeminiService()
        
        # Initialize current session
        if "current_session_id" not in st.session_state:
            session = st.session_state.chat_service.create_session()
            st.session_state.current_session_id = session.session_id
        
        if "system_prompt" not in st.session_state:
            st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
        
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = settings.GEMINI_MODEL
    
    def render_sidebar(self) -> None:
        """Render sidebar controls"""
        st.sidebar.markdown("## 🎯 Streamlit Gemini AI")
        
        # Session management
        action = render_sidebar_session_management()
        
        if action == "new_chat":
            session = self.chat_service.create_session()
            st.session_state.current_session_id = session.session_id
            st.rerun()
        elif action == "clear_chat":
            session_id = st.session_state.current_session_id
            session = self.chat_service.get_session(session_id)
            if session:
                session.messages.clear()
                render_success_message("Chat cleared!")
                st.rerun()
        
        st.sidebar.markdown("---")
        
        # Settings
        settings_dict = render_settings_sidebar()
        
        # Update selected model in session state
        if "model" in settings_dict:
            st.session_state.selected_model = settings_dict["model"]
        
        st.sidebar.markdown("---")
        
        # System prompt
        st.sidebar.markdown("### 📝 System Prompt")
        st.session_state.system_prompt = st.sidebar.text_area(
            "Customize system prompt:",
            value=st.session_state.system_prompt,
            height=150,
            key="system_prompt_input"
        )
        
        # Model info
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ℹ️ Model Info")
        model_info = st.session_state.gemini_service.get_model_info()
        if model_info.is_success():
            st.sidebar.json(model_info.data)
    
    def render_main_chat(self) -> None:
        """Render main chat interface"""
        st.markdown("# 🤖 Streamlit Gemini Chat")
        
        session_id = st.session_state.current_session_id
        session = self.chat_service.get_session(session_id)
        
        if not session:
            render_error_message("Session not found!")
            return
        
        # Display chat history
        st.markdown("---")
        
        with st.container():
            if session.messages:
                display_chat_history(session.messages)
            else:
                render_info_message("Bắt đầu một cuộc trò chuyện mới!")
        
        st.markdown("---")
        
        # Chat input
        user_input = st.chat_input("Nhập tin nhắn của bạn...")
        
        if user_input:
            # Display user message
            st.chat_message("user").write(user_input)
            
            # Generate response
            with st.spinner(MSG_LOADING):
                try:
                    response = st.session_state.gemini_service.generate_response(
                        user_message=user_input,
                        conversation_history=self.chat_service.get_conversation_history(session_id),
                        system_prompt=st.session_state.system_prompt,
                        model_name=st.session_state.selected_model
                    )
                    
                    if response.is_success():
                        # Add messages to session
                        self.chat_service.add_message(
                            session_id,
                            user_input,
                            MessageRole.USER
                        )
                        
                        self.chat_service.add_message(
                            session_id,
                            response.data,
                            MessageRole.ASSISTANT
                        )
                        
                        # Display assistant response
                        with st.chat_message("assistant"):
                            st.write(response.data)
                        
                        st.rerun()
                    else:
                        render_error_message(response.error)
                
                except Exception as e:
                    logger.error(f"Error in chat interface: {str(e)}")
                    render_error_message(str(e))
    
    def run(self) -> None:
        """Run the chat interface"""
        # Configure page
        st.set_page_config(
            page_title="Streamlit Gemini",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Render sidebar
        self.render_sidebar()
        
        # Render main chat
        self.render_main_chat()
