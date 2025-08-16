# 🎙️ 30 Days of AI Voice Agents — Day 13: Documentation

An AI-powered **Voice Agent** built with **FastAPI**, **Google Gemini**, **AssemblyAI**, and **Murf**, enabling real-time voice conversations with AI.  
You can speak to the agent, and it will respond in **text** and **natural-sounding voice**.

---

## 📌 Project Overview

This project is part of the **30 Days of AI Voice Agents** challenge.  
The goal: Build a fully functional **voice-enabled AI agent** that can:

- Understand speech
- Generate intelligent responses
- Speak back using TTS
- Handle failures gracefully with fallbacks

---

## 🛠️ Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** — Backend API framework
- **[AssemblyAI](https://www.assemblyai.com/)** — Speech-to-Text (STT)
- **[Google Gemini](https://ai.google.dev/)** — Large Language Model
- **[Murf](https://murf.ai/)** — Text-to-Speech (TTS)
- **[Jinja2](https://jinja.palletsprojects.com/)** — HTML templating
- **HTML, CSS, JavaScript** — Frontend
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — Environment variable management

---

## 🏗️ Architecture

1. **User speaks into the microphone** 🎤
2. Audio is sent to the backend (`/llm/query` or `/agent/chat/{session_id}`).
3. Backend flow:
   - **AssemblyAI** → Speech → Text
   - **Google Gemini** → Generate AI response
   - **Murf** → Convert text to voice
4. Response is returned to the frontend:
   - Text transcription
   - AI response text
   - AI response audio file
5. **Fallback handling**:
   - If STT fails → Error + fallback audio
   - If LLM fails → Use fallback text
   - If TTS fails → Use fallback.mp3

---

## ✨ Features

- 🎤 Real-time **voice interaction**
- 📝 **Speech-to-Text** transcription
- 🤖 **AI-generated** responses
- 🔊 Natural-sounding **voice output**
- 🛡️ Fallback audio & text on errors
- 🗨️ Multi-turn **chat history**
- 🌐 Web UI built with HTML, CSS, JS

---

## 📂 Project Structure

```
VOICE-AGENT/
│
├── static/                # Frontend static assets
│   ├── fallback.mp3
│   ├── main.js
│   └── style.css
│
├── templates/
│   └── index.html         # Main UI
│
├── uploads/               # Uploaded audio (created at runtime)
├── main.py                # FastAPI backend
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
MURF_API_KEY=your_murf_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

If any API key is missing, the system will still run but will fall back to predefined audio/text.

---

## 🚀 Running the Project

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/voice-agent.git
cd voice-agent
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` file

Add your API keys as shown above.

### 5️⃣ Run the FastAPI server

```bash
uvicorn main:app --reload
```

### 6️⃣ Open in browser

```
http://127.0.0.1:8000
```

---

## 🧪 API Endpoints

| Method | Endpoint                   | Description                           |
| ------ | -------------------------- | ------------------------------------- |
| POST   | `/llm/query`               | Send text/audio → Get AI text & voice |
| POST   | `/agent/chat/{session_id}` | Multi-turn conversation               |
| POST   | `/upload`                  | Upload audio file                     |
| POST   | `/transcribe/file`         | Transcribe uploaded audio             |
| POST   | `/tts/echo`                | Echo transcription as TTS             |

---

## 📸 Screenshots

### Main UI

<img width="2496" height="1180" alt="ui" src="https://github.com/user-attachments/assets/7ed9a1e8-3ae8-44ca-8a9c-363b0f7c00c4" />


### Project Structure

voice-agent/
│── app/
│   ├── main.py          # FastAPI entry point
│   ├── models/          # Pydantic schemas
│   │   ├── llm.py
│   │   └── chat.py
│   ├── services/        # External services logic
│   │   ├── assemblyai.py
│   │   ├── gemini.py
│   │   └── murf.py
│   ├── routes/          # API endpoints
│   │   ├── llm_routes.py
│   │   ├── chat_routes.py
│   │   ├── tts_routes.py
│   │   └── upload_routes.py
│   ├── utils/           # Utility functions (logging, error handlers)
│   │   └── logger.py
│   └── __init__.py
│
│── static/
│── templates/
│── uploads/
│── .env
│── README.md
│── requirements.txt

<img width="334" height="676" alt="image" src="https://github.com/user-attachments/assets/ce090739-1197-4db2-876d-ebb65c94fb9a" />




---

## 📜 License

MIT License – Free to use and modify.

---
