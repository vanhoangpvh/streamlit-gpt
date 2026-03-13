"""
Example page: Chat History
This demonstrates how to create additional Streamlit pages
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
from services.chat_service import ChatService
from ui.components import render_error_message, render_success_message
import json


def render_chat_history_page():
    """Render chat history page"""
    st.set_page_config(
        page_title="Chat History",
        page_icon="📜",
        layout="wide"
    )
    
    st.markdown("# 📜 Chat History")
    
    chat_service = ChatService()
    sessions = chat_service.get_all_sessions()
    
    if not sessions:
        st.info("No chat sessions found")
        return
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sessions", len(sessions))
    with col2:
        total_messages = sum(len(s.messages) for s in sessions)
        st.metric("Total Messages", total_messages)
    with col3:
        avg_messages = total_messages / len(sessions) if sessions else 0
        st.metric("Average Messages/Session", f"{avg_messages:.1f}")
    
    st.markdown("---")
    
    # Sessions list
    st.markdown("## Sessions")
    
    for session in sessions:
        with st.expander(f"🗨️ {session.title} ({len(session.messages)} messages)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**ID:** {session.session_id}")
                st.write(f"**Created:** {session.created_at}")
                st.write(f"**Updated:** {session.updated_at}")
            
            with col2:
                if st.button("📥 Export", key=f"export_{session.session_id}"):
                    exported = chat_service.export_session(session.session_id)
                    st.json(exported)
            
            # Messages
            st.markdown("### Messages")
            for msg in session.messages:
                if msg.role.value == "user":
                    st.write(f"**👤 You:** {msg.content}")
                else:
                    st.write(f"**🤖 Assistant:** {msg.content}")
                st.caption(f"*{msg.timestamp}*")


if __name__ == "__main__":
    render_chat_history_page()
