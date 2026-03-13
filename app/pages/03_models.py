"""
Available Models Page
Display all available Gemini models with their capabilities
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
from services.gemini_service import GeminiService


def main():
    """Main page function"""
    st.set_page_config(
        page_title="Available Models",
        page_icon="🤖",
        layout="wide"
    )
    
    st.markdown("# 🤖 Available Gemini Models")
    st.markdown("---")
    
    try:
        gemini_service = GeminiService()
        response = gemini_service.list_available_models()
        
        if response.is_success() and response.data:
            models = response.data
            st.success(f"✅ Found {len(models)} available models")
            
            st.markdown("---")
            
            # Display models in tabs or columns
            for model in models:
                with st.expander(f"🔹 {model.get('name', 'Unknown')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Display Name:** {model.get('display_name', 'N/A')}")
                        st.write(f"**Name:** `{model.get('name', 'N/A')}`")
                    
                    with col2:
                        st.write(f"**Input Token Limit:** {model.get('input_token_limit', 'N/A'):,}")
                        st.write(f"**Output Token Limit:** {model.get('output_token_limit', 'N/A'):,}")
                    
                    if model.get('description'):
                        st.info(f"📝 {model.get('description')}")
            
            st.markdown("---")
            
            # Display in table format
            st.markdown("### 📊 Models Summary")
            
            models_data = []
            for model in models:
                models_data.append({
                    "Name": model.get("name", "N/A"),
                    "Display Name": model.get("display_name", "N/A"),
                    "Input Tokens": model.get("input_token_limit", 0),
                    "Output Tokens": model.get("output_token_limit", 0),
                })
            
            st.dataframe(models_data, use_container_width=True)
            
        else:
            st.warning("⚠️ Could not fetch models from API")
            st.info("Fallback models available:")
            default_models = [
                "gemini-2.5-pro - Latest generation model",
                "gemini-2.5-flash - Fast generation model",
                "gemini-pro - Previous generation",
                "gemini-pro-vision - Vision capabilities"
            ]
            for model in default_models:
                st.write(f"• {model}")
    
    except Exception as e:
        st.error(f"❌ Error fetching models: {str(e)}")
        st.info("Please check your API key configuration")


if __name__ == "__main__":
    main()
