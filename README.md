# MeetMate 🎓🤖  
### AI-Powered Meeting Transcription, Summarization & Email Assistant

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-00A67E.svg?logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![Gemini AI](https://img.shields.io/badge/Google-Gemini_AI-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)

**MeetMate** is an end-to-end AI meeting assistant designed to transcribe meeting audio recordings, generate structured executive summaries using Generative AI, and automatically distribute those notes to team members via email.

Whether you're hosting online classes, team standups, or client calls, MeetMate reduces manual note-taking to zero.

---

## ✨ Features

- 🎙️ **Local Speech-to-Text (OpenAI Whisper)**: Transcribe meeting audio (`mp3`, `wav`, `m4a`) offline with high accuracy and translation support.
- 🧠 **Smart Executive Summaries (Gemini 1.5 Flash)**: Categorizes transcripts into **Executive Summary**, **Key Decisions**, **Action Items**, and **Open Questions**.
- ⚡ **Built-in Local Fallback Engine**: Works offline or without API keys using pattern-based summarization.
- 🌐 **Futuristic Streamlit Web App**: Clean, dark-themed UI to upload files, configure emails, and trigger real-time processing pipelines.
- 📧 **Automated SMTP Email Delivery**: Sends formatted meeting minutes and text attachments directly to attendees.
- 🤖 **Automated Meeting Bot (Selenium)**: Experimental browser bot capable of auto-joining Google Meet sessions.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.8+
- **Transcription**: `openai-whisper`
- **Generative AI**: `google-generativeai` (Gemini API)
- **Web Interface**: `streamlit`
- **Automation Bot**: `selenium`
- **Email Delivery**: `smtplib` & `email.mime`
- **Environment Management**: `python-dotenv`

---

## 📂 Repository Architecture

```text
MeetMate/
├── app.py                  # Streamlit Web GUI Application
├── main.py                 # Terminal/CLI Workflow Controller
├── transcribe.py           # Audio-to-Text Module (OpenAI Whisper Engine)
├── summarize.py            # AI Summarizer (Gemini API + Local Fallback)
├── send_email.py           # Automated Email Dispatcher
├── bot.py                  # Selenium Google Meet Auto-Joiner Bot
├── requirements.txt        # Required Python Libraries
├── .env.example            # Environment Configuration Template
├── README.md               # Project Documentation
├── audio/                  # Input directory for meeting audio files
└── outputs/                # Output directory for generated transcripts & summaries
```

---

## ⚡ Quick Start Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Riteshjadhav123/MeetMate.git
cd MeetMate
```

### 2️⃣ Set Up Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: For Whisper AI transcription, ensure `ffmpeg` is installed on your system).*

---

## 🔑 Environment Configuration

Create a `.env` file in the project root directory (refer to `.env.example`):

```env
# Gemini API Key for AI Summarization
GEMINI_API_KEY=your_gemini_api_key_here

# Email Credentials for SMTP Dispatch
SENDER_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=team_member@example.com
```

> 🔒 **Security Notice**: Never commit your `.env` file or API secrets to GitHub.

---

## 🚀 Running MeetMate

### Option A: Interactive Web Interface (Recommended)
Launch the Streamlit web dashboard:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`, upload your meeting audio, set receiver emails, and click **Generate & Send Summary**.

### Option B: Command Line Interface (CLI)
Run the background execution script:
```bash
python main.py
```

---

## 🔮 Roadmap & Future Enhancements

- [ ] Real-time live microphone stream transcription
- [ ] Speaker diarization (who spoke when)
- [ ] Direct Google Calendar & Zoom API integration
- [ ] Multi-language translation dashboard

---

## 👨‍💻 Author

**Ritesh Jhadav**  
- 🐙 GitHub: [@Riteshjadhav123](https://github.com/Riteshjadhav123)  
- 🎓 Artificial Intelligence & Data Science  
- 💡 Project: **MeetMate AI**

---
