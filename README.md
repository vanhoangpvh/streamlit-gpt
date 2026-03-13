# 🤖 Streamlit Gemini Chat Application

Một ứng dụng web chat tương tác sử dụng Google Gemini API và Streamlit, được xây dựng với kiến trúc sạch và dễ mở rộng.

## ✨ Tính Năng

- 💬 Chat tương tác với Google Gemini API
- 📝 Quản lý multiple chat sessions
- ⚙️ Cấu hình tùy chỉnh (temperature, model selection, system prompt)
- 📊 Lịch sử tin nhắn được lưu trữ
- 🎨 Giao diện người dùng thân thiện
- 🔒 Xử lý lỗi toàn diện
- 📝 Logging và debugging

## 🏗️ Cấu Trúc Dự Án

```
streamlit-gpt/
├── app/                      # Main application
│   ├── main.py              # Entry point
│   └── pages/               # Additional Streamlit pages
├── config/                  # Configuration
│   ├── settings.py          # Environment & app settings
│   └── constants.py         # Global constants
├── services/                # Business logic
│   ├── gemini_service.py    # Gemini API wrapper
│   └── chat_service.py      # Chat management
├── models/                  # Data models
│   └── schemas.py           # Pydantic models
├── ui/                      # UI components
│   ├── components.py        # Reusable UI components
│   └── chat_interface.py    # Main chat interface
├── utils/                   # Utility functions
│   ├── logger.py            # Logging configuration
│   └── helpers.py           # Helper functions
├── tests/                   # Unit tests
│   └── test_gemini_service.py
├── .env                     # Environment variables
├── .gitignore              # Git ignore file
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Cài Đặt & Chạy

### 1. Clone hoặc tải dự án
```bash
cd streamlit-gpt
```

### 2. Tạo virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment
Tạo file `.env` và thêm API key của bạn:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
DEBUG=False
```

### 5. Chạy ứng dụng
```bash
streamlit run app/main.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`

## 📚 Cách Sử Dụng

### Chat Interface
1. Nhập tin nhắn vào input field
2. Nhấn Enter để gửi
3. Phản hồi từ Gemini sẽ xuất hiện tức thì

### Session Management
- **New Chat**: Tạo cuộc trò chuyện mới
- **Save**: Lưu cuộc trò chuyện hiện tại
- **Clear**: Xóa tất cả tin nhắn

### Settings
- **Temperature**: Điều chỉnh độ ngẫu nhiên của phản hồi (0-2)
- **Model**: Chọn mô hình Gemini
- **System Prompt**: Tùy chỉnh hành vi AI

## 🔑 Cấu Trúc File Chính

### config/settings.py
Quản lý tất cả cài đặt ứng dụng:
```python
from config.settings import settings
settings.GEMINI_API_KEY
settings.TEMPERATURE
```

### services/gemini_service.py
Wrapper cho Gemini API:
```python
from services.gemini_service import GeminiService
service = GeminiService()
response = service.generate_response(message, history)
```

### services/chat_service.py
Quản lý chat sessions:
```python
from services.chat_service import ChatService
chat_service = ChatService()
session = chat_service.create_session()
```

### models/schemas.py
Data models:
```python
from models.schemas import Message, ChatSession, MessageRole
```

## 🧪 Testing

Chạy unit tests:
```bash
pytest tests/
```

Chạy test cụ thể:
```bash
pytest tests/test_gemini_service.py -v
```

## 📖 API Reference

### GeminiService

#### generate_response()
```python
response = gemini_service.generate_response(
    user_message="Xin chào",
    conversation_history=[...],
    system_prompt="Optional prompt"
)
```

#### stream_response()
```python
for chunk in gemini_service.stream_response(message, history):
    print(chunk)
```

### ChatService

#### create_session()
```python
session = chat_service.create_session(title="My Chat")
```

#### add_message()
```python
message = chat_service.add_message(
    session_id="...",
    content="Hello",
    role=MessageRole.USER
)
```

#### process_user_message()
```python
response = await chat_service.process_user_message(
    session_id="...",
    user_message="Hello"
)
```

## 🛠️ Tùy Chỉnh & Mở Rộng

### Thêm Page Mới
1. Tạo file trong `app/pages/`
2. Sử dụng Streamlit multi-page app functionality

### Tích Hợp Database
Thêm vào `services/` layer:
```python
# services/database_service.py
class DatabaseService:
    def save_session(self, session): pass
    def load_session(self, session_id): pass
```

### Custom Components
Thêm vào `ui/components.py`:
```python
def render_custom_component(): pass
```

## 🔐 Security Best Practices

1. **Không commit .env file**
   - Luôn thêm `.env` vào `.gitignore`
   - Sử dụng environment variables cho sensitive data

2. **API Key Management**
   - Giữ API key bí mật
   - Sử dụng secret management tools cho production

3. **Input Validation**
   - Validate user inputs trước khi gửi đến API
   - Kiểm tra message length limits

## 📝 Environment Variables

```
GEMINI_API_KEY=your_api_key           # Gemini API Key (required)
GEMINI_MODEL=gemini-pro               # Model to use
DEBUG=False                           # Enable debug mode
APP_TITLE=Streamlit Gemini           # App title
```

## 🐛 Troubleshooting

### API Key Error
```
ValueError: GEMINI_API_KEY not set in environment variables
```
**Giải pháp**: Thêm `GEMINI_API_KEY` vào `.env` file

### Import Error
```
ModuleNotFoundError: No module named 'google'
```
**Giải pháp**: Chạy `pip install -r requirements.txt`

### Streamlit Error
```
streamlit.errors.StreamlitAPIException
```
**Giải pháp**: Restart Streamlit server

## 📦 Dependencies

- **streamlit** - Web framework
- **google-generativeai** - Gemini API client
- **python-dotenv** - Environment variable management
- **pydantic** - Data validation
- **pytest** - Testing framework

## 🤝 Contributing

1. Tạo feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add your feature'`
3. Push branch: `git push origin feature/your-feature`
4. Tạo Pull Request

## 📄 License

Dự án này được cấp phép dưới MIT License

## 📞 Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra `.env` configuration
2. Xem logs trong console
3. Chạy `pytest` để kiểm tra các tests

## 🎯 Roadmap

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication
- [ ] Chat history export (PDF/JSON)
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Dark mode UI theme
- [ ] Docker deployment

---

**Made with ❤️ using Streamlit & Google Gemini API**
