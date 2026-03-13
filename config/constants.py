"""
Application constants
"""

# Message roles
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"

# Session state keys
SESSION_KEY_MESSAGES = "messages"
SESSION_KEY_CHAT_HISTORY = "chat_history"
SESSION_KEY_CURRENT_SESSION = "current_session"

# Default messages
DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant powered by Google Gemini. 
You provide accurate, helpful, and informative responses. 
You should be friendly and conversational while maintaining professionalism."""

# UI Messages
MSG_WELCOME = "👋 Hãy bắt đầu cuộc trò chuyện của bạn!"
MSG_ERROR = "❌ Đã xảy ra lỗi. Vui lòng thử lại."
MSG_LOADING = "⏳ Đang xử lý..."

# API Response Status
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"
STATUS_PENDING = "pending"

# Available Gemini Models (Fallback)
AVAILABLE_MODELS = {
    "gemini-2.5-pro": {
        "display_name": "Gemini 2.5 Pro",
        "description": "Most advanced model - best for complex reasoning",
        "input_tokens": 1000000,
        "output_tokens": 100000,
    },
    "gemini-2.5-flash": {
        "display_name": "Gemini 2.5 Flash", 
        "description": "Fast and efficient model - best for low-latency tasks",
        "input_tokens": 1000000,
        "output_tokens": 100000,
    },
    "gemini-pro": {
        "display_name": "Gemini Pro",
        "description": "Previous generation - good for text-only tasks",
        "input_tokens": 32000,
        "output_tokens": 8192,
    },
    "gemini-pro-vision": {
        "display_name": "Gemini Pro Vision",
        "description": "Vision capabilities - can analyze images",
        "input_tokens": 12800,
        "output_tokens": 4096,
    }
}
