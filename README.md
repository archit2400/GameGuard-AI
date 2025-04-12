# 🎮 GameGuard AI - Chat Moderation Bot

GameGuard is an AI-powered chat moderation tool built for online gaming communities. It detects offensive, spam, and toxic content in real-time using NLP models and filters messages accordingly.

## 🔧 Features
- Real-time moderation
- Offensive & spam detection
- API endpoints for moderation
- Future scope: Dashboard, multi-language support

## 🚀 Tech Stack
- Python (Flask/FastAPI)
- Transformers (Hugging Face)
- SQLite/MongoDB
- Optional: Tailwind CSS (Frontend)

## 🔌 API Endpoints
- `/moderate` → POST → Returns moderation result
- `/report` → POST → Logs flagged messages

## 📦 Setup

```bash
pip install -r requirements.txt
python app.py
