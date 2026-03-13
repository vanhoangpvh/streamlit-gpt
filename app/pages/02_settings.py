"""
Example page: Settings & Preferences
This demonstrates how to create additional Streamlit pages
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
from config.settings import settings
from ui.components import render_success_message, render_info_message


def render_settings_page():
    """Render settings page"""
    st.set_page_config(
        page_title="Settings",
        page_icon="⚙️",
        layout="wide"
    )
    
    st.markdown("# ⚙️ Settings & Configuration")
    
    # Current Configuration
    st.markdown("## Current Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Gemini Model:** {settings.GEMINI_MODEL}")
        st.info(f"**Temperature:** {settings.TEMPERATURE}")
        st.info(f"**Top P:** {settings.TOP_P}")
    
    with col2:
        st.info(f"**Top K:** {settings.TOP_K}")
        st.info(f"**Debug Mode:** {settings.DEBUG}")
        st.info(f"**Max History:** {settings.MAX_HISTORY_LENGTH}")
    
    st.markdown("---")
    
    # Model Information
    st.markdown("## 🤖 Model Information")
    
    model_info = {
        "Model": settings.GEMINI_MODEL,
        "Framework": "Google Generative AI",
        "API": "v1",
        "Status": "Active"
    }
    
    st.json(model_info)
    
    st.markdown("---")
    
    # Application Info
    st.markdown("## ℹ️ Application Information")
    
    app_info = {
        "App Name": settings.APP_TITLE,
        "Version": "1.0.0",
        "Framework": "Streamlit",
        "Python": "3.8+"
    }
    
    st.json(app_info)
    
    st.markdown("---")
    
    # Feature Flags
    st.markdown("## 🚩 Features")
    
    features = {
        "Chat Interface": "✅ Enabled",
        "Session Management": "✅ Enabled",
        "Message History": "✅ Enabled",
        "Export Chat": "🔄 In Development",
        "Database": "🔄 In Development",
        "Authentication": "🔄 In Development"
    }
    
    for feature, status in features.items():
        st.write(f"{feature}: {status}")


if __name__ == "__main__":
    render_settings_page()
