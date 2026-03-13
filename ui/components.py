"""
Reusable UI components for Streamlit
"""

import streamlit as st
from typing import Optional, List, Callable
from models.schemas import Message, MessageRole


def display_message(message: Message, key: Optional[str] = None) -> None:
    """
    Display a single message in chat interface
    
    Args:
        message: Message to display
        key: Optional key for Streamlit
    """
    if message.role == MessageRole.USER:
        with st.chat_message("user"):
            st.write(message.content)
    elif message.role == MessageRole.ASSISTANT:
        with st.chat_message("assistant"):
            st.write(message.content)
    elif message.role == MessageRole.SYSTEM:
        with st.chat_message("assistant"):
            st.info(f"System: {message.content}")


def display_chat_history(messages: List[Message]) -> None:
    """
    Display all messages in chat history
    
    Args:
        messages: List of messages to display
    """
    for i, message in enumerate(messages):
        display_message(message, key=f"message_{i}")


def render_sidebar_session_management() -> Optional[str]:
    """
    Render session management controls in sidebar
    
    Returns:
        Selected action or None
    """
    st.sidebar.markdown("### 💬 Session Management")
    
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        if st.button("➕ New Chat"):
            return "new_chat"
    
    with col2:
        if st.button("💾 Save"):
            return "save_session"
    
    with col3:
        if st.button("🗑️ Clear"):
            return "clear_chat"
    
    return None


def render_settings_sidebar() -> dict:
    """
    Render settings controls in sidebar
    
    Returns:
        Dictionary of selected settings
    """
    st.sidebar.markdown("### ⚙️ Settings")
    
    settings = {}
    
    # Temperature slider
    settings["temperature"] = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Control randomness of responses"
    )
    
    # Model selection - with fallback to default models
    try:
        from services.gemini_service import GeminiService
        gemini_service = GeminiService()
        models_response = gemini_service.list_available_models()
        
        if models_response.is_success() and models_response.data:
            model_names = [m["name"] for m in models_response.data]
            display_names = [f"{m['name']}" for m in models_response.data]
            selected_idx = 0
            
            selected_display = st.sidebar.selectbox(
                "Model",
                display_names,
                index=selected_idx
            )
            settings["model"] = model_names[display_names.index(selected_display)]
        else:
            # Fallback to default models
            default_models = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-pro", "gemini-pro-vision"]
            settings["model"] = st.sidebar.selectbox(
                "Model",
                default_models
            )
    except Exception as e:
        # Fallback if service fails
        default_models = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-pro", "gemini-pro-vision"]
        settings["model"] = st.sidebar.selectbox(
            "Model",
            default_models
        )
    
    return settings


def render_error_message(error: str) -> None:
    """
    Display error message
    
    Args:
        error: Error message to display
    """
    st.error(f"❌ Error: {error}")


def render_warning_message(warning: str) -> None:
    """
    Display warning message
    
    Args:
        warning: Warning message to display
    """
    st.warning(f"⚠️ Warning: {warning}")


def render_success_message(success: str) -> None:
    """
    Display success message
    
    Args:
        success: Success message to display
    """
    st.success(f"✅ {success}")


def render_info_message(info: str) -> None:
    """
    Display info message
    
    Args:
        info: Info message to display
    """
    st.info(f"ℹ️ {info}")
