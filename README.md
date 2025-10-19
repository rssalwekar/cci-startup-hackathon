# InterVue - AI Coding Interview Platform

An intelligent platform that simulates real technical interviews using AI. Practice coding problems with voice interaction, real-time feedback, and comprehensive performance analysis.

## Features

- AI Interview Agent - Natural conversation-based coding interviews
- Voice Interaction - Text-to-speech and speech-to-text communication  
- Monaco IDE - Professional code editor with syntax highlighting
- LeetCode Integration - Dynamic problem selection by difficulty and topic
- Real-time Testing - Execute code against test cases instantly
- Performance Analytics - Detailed feedback on code quality and communication
- Session Recording - Review interviews with video/audio playback

## Prerequisites

- Python 3.8+
- Redis (WSL for Windows, or Homebrew/apt for Mac/Linux)
- Git

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/rssalwekar/cci-startup-hackathon.git
cd cci-startup-hackathon
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with:

```env
KRONOS_API_KEY=your_kronos_api_key_here
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here
```

**Get API Keys from:**
- Kronos Labs: https://kronoslabs.org/
- ElevenLabs: https://elevenlabs.io

### 5. Setup Database

```bash
python manage.py migrate
python manage.py create_demo_user
```

## Running the Application

Windows: Run .\start.ps1
Mac/Linux: Start redis-server in one terminal, then run python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application

Access at: http://127.0.0.1:8000

## Usage

1. Sign up or login (demo: demo/demo123)
2. Start Interview - Set difficulty and topics
3. Code & Communicate - Use voice or chat
4. Submit & Test - Run code against test cases
5. Get Feedback - Receive AI analysis
6. Review History - Access past interviews

## Tech Stack

Backend: Django 5.2, Channels, REST Framework
AI: Kronos Labs Hermes API
Voice: ElevenLabs API
Code Execution: Piston API
Database: SQLite / PostgreSQL
Frontend: Monaco Editor, JavaScript

## Troubleshooting

Redis not running (Windows): wsl redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes
Port 8000 in use: netstat -ano | findstr :8000 then taskkill /PID <PID> /F
Database issues: rm db.sqlite3 then python manage.py migrate

## Team

Created by Team CodeWrestlers for the CCI Startup Hackathon 2025.

## License

Educational purposes only.
