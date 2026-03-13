#!/bin/bash
# Run script for Streamlit Gemini App

# Activate virtual environment (optional)
# source venv/bin/activate  # For macOS/Linux
# venv\Scripts\activate     # For Windows

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with GEMINI_API_KEY"
    exit 1
fi

# Start Streamlit
echo "🚀 Starting Streamlit Gemini Application..."
streamlit run app/main.py
