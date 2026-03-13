@echo off
REM Run script for Streamlit Gemini App (Windows PowerShell)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please create .env file with GEMINI_API_KEY
    exit /b 1
)

REM Start Streamlit
echo 🚀 Starting Streamlit Gemini Application...
streamlit run app/main.py
