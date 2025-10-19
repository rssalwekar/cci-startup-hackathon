# InterVue - AI Coding Interview Platform# InterVue - AI-Powered Coding Interview Platform# AI Coding Interview Platform



An intelligent platform that simulates real technical interviews using AI. Practice coding with voice interaction, real-time feedback, and comprehensive performance analysis.



## FeaturesInterVue is an intelligent coding interview platform that simulates real technical interviews using AI. Practice coding problems with voice interaction, real-time feedback, and comprehensive performance analysis.



- 🤖 **AI Interview Agent** - Natural conversation-based coding interviews

- 🎤 **Voice Interaction** - Speak with the AI using text-to-speech and speech-to-text

- 💻 **Monaco IDE** - Professional code editor with syntax highlighting## Features## Features

- 🎯 **LeetCode Integration** - Dynamic problem selection by difficulty and topic

- ⚡ **Real-time Testing** - Execute code against test cases instantly

- 📊 **Performance Analytics** - Detailed feedback on code quality and communication

- 🎥 **Session Recording** - Review interviews with video/audio playback- 🤖 **AI Interview Agent** - Conducts realistic coding interviews with natural conversation- **AI Interview Agent**: Conducts coding interviews with personalized problem selection from LeetCode



## Prerequisites- 🎤 **Voice Interaction** - Speak naturally with the AI interviewer using text-to-speech and speech-to-text- **Voice Interaction**: Speech-to-text and text-to-speech using ElevenLabs for natural conversation



- **Python 3.8+**- 💻 **Monaco Code Editor** - Professional IDE with syntax highlighting and auto-completion- **Real-time Chat**: Interactive chat interface with the AI interviewer

- **Redis** (via WSL for Windows, or Homebrew/apt for Mac/Linux)

- **Git**- 🎯 **LeetCode Integration** - Access to real LeetCode problems with dynamic difficulty selection- **Dynamic Problem Selection**: LeetCode API integration with difficulty and topic preferences



## Quick Start- ⚡ **Real-time Code Execution** - Test your code against LeetCode test cases instantly- **Monaco IDE**: Built-in code editor with syntax highlighting and auto-completion



### 1. Clone and Setup- 📊 **Performance Analytics** - Get detailed feedback on code quality, communication, and problem-solving- **Test Case Execution**: Real-time code testing with Piston API



```bash- 🎥 **Interview Recording** - Review your interviews with video/audio playback- **Resizable UI**: Drag-to-resize panels for optimal workspace layout

git clone https://github.com/rssalwekar/cci-startup-hackathon.git

cd cci-startup-hackathon- 👤 **User Profiles** - Track your progress, statistics, and interview history- **Interview Recording**: Video/audio recording of interview sessions



# Create virtual environment- **Results Page**: Comprehensive feedback with chat transcript, code, and AI analysis

python -m venv .venv

## Tech Stack- **WebSocket Communication**: Real-time updates and chat functionality

# Activate virtual environment

# Windows:- **Session Management**: Track interview sessions and progress

.venv\Scripts\activate

# Mac/Linux:- **Backend**: Django 5.2, Django Channels (WebSockets)

source .venv/bin/activate

- **AI**: Kronos Labs Hermes API### Setup Instructions

# Install dependencies

pip install -r requirements.txt- **Voice**: ElevenLabs API

```

- **Code Execution**: Piston API```bash

### 2. Environment Variables

- **Frontend**: HTML, CSS, JavaScript, Monaco Editor# 1. Install dependencies

Create a `.env` file in the root directory:

- **Database**: SQLite (development) / PostgreSQL (production-ready)pip install -r requirements.txt

```env

KRONOS_API_KEY=your_kronos_api_key_here- **Message Broker**: Redis

ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here

- **Storage**: Supabase (optional cloud storage)# 2. Set up environment variables

# Optional: Supabase for cloud storage

SUPABASE_URL=your_supabase_url# Create .env file with:

SUPABASE_KEY=your_supabase_key

SUPABASE_BUCKET=interview-recordings---KRONOS_API_KEY=your_kronos_api_key_here

```

ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here, SUPABASE credentials

### 3. Database Setup

## Prerequisites

```bash

python manage.py migrate# 3. Run migrations

python manage.py create_demo_user  # Creates demo/demo123

```### Windows Userspython manage.py migrate



### 4. Run the Application- Python 3.8+



**Windows (Automated):**- WSL (Windows Subsystem for Linux) with Redis installed# 4. Create a user account (or use signup page)

```powershell

.\start.ps1- Gitpython manage.py createsuperuser

```

```

**Mac/Linux (Manual):**

```bash### Mac/Linux Users

# Terminal 1 - Start Redis

redis-server- Python 3.8+### Starting the Application



# Terminal 2 - Start Django- Redis installed via Homebrew/apt

source .venv/bin/activate

python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application- Git**Option 1: Automated Startup (Windows with WSL - Recommended)**

```

```powershell

### 5. Access

---# Starts Redis and Django server automatically

Navigate to `http://127.0.0.1:8000` in your browser.

.\start.ps1

## Usage

## Installation```

1. **Sign up** or login with `demo` / `demo123`

2. **Start Interview** - Set difficulty and topics

3. **Code & Communicate** - Use voice or chat to discuss your approach

4. **Submit & Test** - Run code against test cases### 1. Clone the Repository**Option 2: Manual Startup**

5. **Review** - Get AI feedback and review past interviews

```powershell

## Tech Stack

```bash# Start Redis (if not already running)

- **Backend**: Django 5.2, Channels (WebSockets)

- **AI**: Kronos Labs Hermes APIgit clone https://github.com/rssalwekar/cci-startup-hackathon.git.\start-redis.ps1

- **Voice**: ElevenLabs API

- **Code Execution**: Piston APIcd cci-startup-hackathon

- **Database**: SQLite / PostgreSQL

- **Frontend**: Monaco Editor, JavaScript```# Start Django server



## API Keyspython -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application



Get your API keys:### 2. Create Virtual Environment```

- **Kronos Labs**: https://kronosai.com

- **ElevenLabs**: https://elevenlabs.io

- **Supabase** (optional): https://supabase.com

**Windows:****Option 3: Individual Commands**

## Troubleshooting

```powershell```bash

**Redis not running (Windows)?**

```powershellpython -m venv .venv# Terminal 1: Start Redis in WSL

wsl redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes

```.venv\Scripts\activatewsl redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes



**Port 8000 already in use?**```

```bash

# Windows:# Terminal 2: Start Django

netstat -ano | findstr :8000

taskkill /PID <PID> /F**Mac/Linux:**python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application



# Mac/Linux:```bash```

lsof -ti:8000 | xargs kill -9

```python3 -m venv .venv



**Database issues?**source .venv/bin/activate### Usage

```bash

rm db.sqlite3```

python manage.py migrate

```1. Navigate to `http://127.0.0.1:8000/`



## Project Structure### 3. Install Dependencies2. Sign up for a new account at `/accounts/signup/` or login



```3. Complete your profile and upload an avatar (optional)

cci-startup-hackathon/

├── ai_interview/          # Main Django app```bash3. Click "Start Interview" to begin

├── interview_platform/    # Django settings

├── templates/             # HTML templatespip install -r requirements.txt4. **Set Preferences**: Tell the AI your difficulty (easy/medium/hard) and topic preferences (arrays, strings, trees, etc.)

├── static/                # CSS, JS files

└── media/                 # User uploads```5. **Voice Interaction**: Use the microphone button to speak naturally with the AI

```

6. **Solve Problems**: Write code in the Monaco IDE and submit to run test cases

## Contributing

### 4. Set Up Environment Variables7. **Get Feedback**: Receive real-time AI guidance and comprehensive feedback

This is a hackathon project created by Team CodeWrestlers for the CCI Startup Hackathon 2025.

8. **View Results**: After ending the interview, see detailed results with video recording and analysis

## License

Create a `.env` file in the root directory:

Educational purposes only.

### Advanced Features

```env

# Required API Keys- **Problem Name Requests**: Ask for specific problems like "two sum" or "valid parentheses"

KRONOS_API_KEY=your_kronos_api_key_here- **Resizable Panels**: Drag the resize handles to customize your workspace layout

ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here- **Test Case Execution**: Submit code to run against LeetCode test cases

- **Interview Recording**: Sessions are automatically recorded for review

# Optional: Supabase for cloud storage (leave blank for local storage)- **Voice Controls**: Continuous speech recognition for hands-free interaction

SUPABASE_URL=your_supabase_url

SUPABASE_KEY=your_supabase_key## Project Structure

SUPABASE_BUCKET=interview-recordings

``````

ai_interview/

### 5. Run Database Migrations├── models.py          # Database models

├── views.py           # View functions

```bash├── ai_agent.py        # Core AI interview logic

python manage.py migrate├── consumers.py       # WebSocket consumers

```├── routing.py         # WebSocket routing

├── urls.py           # URL patterns

### 6. Create Demo User (Optional)├── admin.py          # Admin interface

└── management/

```bash    └── commands/     # Custom management commands

python manage.py create_demo_user

```templates/

├── ai_interview/     # Interview page templates

Or create your own superuser:└── registration/     # Authentication templates

```bash```

python manage.py createsuperuser

```## AI Agent Features



---The AI interview agent provides:



## Running the Application- **Skill Assessment**: Evaluates user preferences and skill level

- **Problem Selection**: Chooses appropriate LeetCode problems

### Windows (Recommended - Automated)- **Real-time Guidance**: Provides hints and feedback during problem solving

- **Code Analysis**: Reviews submitted code for correctness and quality

**Option 1: Use the startup script**- **Comprehensive Feedback**: Generates detailed performance reports

```powershell

.\start.ps1## Technologies Used

```

This automatically starts Redis (in WSL) and the Django server.- **Backend**: Django, Django REST Framework

- **Real-time Communication**: Django Channels, WebSockets

**Option 2: Manual startup**- **AI Integration**: Kronos Labs Hermes API

```powershell- **Voice Services**: ElevenLabs API for natural speech synthesis

# Terminal 1: Start Redis in WSL- **Code Execution**: Piston API for running test cases

wsl redis-server --bind 0.0.0.0 --protected-mode no- **Problem Database**: LeetCode GraphQL API

- **Database**: SQLite (development), PostgreSQL (production ready)

# Terminal 2: Start Django server- **Frontend**: HTML, CSS, JavaScript, Monaco Editor

python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application- **Message Broker**: Redis

```- **Media Handling**: Django FileField for video/audio storage



### Mac/Linux## API Endpoints



**Terminal 1: Start Redis**- `GET /ai-interview/start/` - Start new interview

```bash- `GET /ai-interview/interview/<session_id>/` - Interview page

# Start Redis server- `GET /ai-interview/results/<session_id>/` - Interview results page

redis-server- `POST /ai-interview/api/submit-code/<session_id>/` - Submit code

```- `GET /ai-interview/api/session-data/<session_id>/` - Get session data

- `GET /ai-interview/get-function-signature/<session_id>/` - Get function signature

**Terminal 2: Start Django**- `GET /ai-interview/get-test-cases/<session_id>/` - Get test cases

```bash- `POST /ai-interview/api/synthesize-speech/` - Text-to-speech conversion

# Activate virtual environment- `POST /ai-interview/api/get-last-ai-message/<session_id>/` - Get last AI message for re-speak

source .venv/bin/activate- `WebSocket /ws/interview/<session_id>/` - Real-time chat and code submission



# Start Django server## Contributing

python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application

```This is a hackathon project. For production use, consider:



### Access the Application- Adding proper authentication and user management

- Implementing code execution sandbox

Open your browser and navigate to:- Adding more problem categories and difficulty levels

```- Enhancing the AI agent with more sophisticated guidance

http://127.0.0.1:8000- Adding session recording and playback features

```- Implementing proper error handling and logging



---## License



## Usage GuideThis project is part of a hackathon and is for educational purposes.


1. **Sign Up / Login** - Create an account or login at `http://127.0.0.1:8000/accounts/signup/`

2. **Start Interview** - Click "Start Interview" from the home page

3. **Set Preferences** - Tell the AI your:
   - Difficulty level (Easy, Medium, Hard)
   - Topic preferences (Arrays, Strings, Trees, etc.)
   - Or request a specific problem by name

4. **Code & Communicate** - Use the Monaco editor to write code and voice/chat to discuss your approach

5. **Submit & Test** - Run your code against LeetCode test cases in real-time

6. **Get Feedback** - Receive comprehensive AI-generated feedback on your performance

7. **Review History** - Access past interviews from your profile page

---

## Project Structure

```
cci-startup-hackathon/
├── ai_interview/              # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── ai_agent.py           # AI interview logic
│   ├── consumers.py          # WebSocket handlers
│   ├── leetcode_service.py   # LeetCode API integration
│   └── auth_views.py         # Authentication views
├── interview_platform/        # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py               # ASGI configuration
├── templates/                 # HTML templates
│   ├── ai_interview/
│   └── registration/
├── static/                    # Static files (CSS, JS)
├── media/                     # User uploads (recordings, avatars)
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

---

## Configuration

### Redis Configuration

The application requires Redis for WebSocket support. Default connection:
- **Host**: `172.27.247.142` (WSL) or `127.0.0.1` (Mac/Linux)
- **Port**: `6379`

To change Redis settings, edit `interview_platform/settings.py`:
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],  # Update for your setup
        },
    },
}
```

### Database

- **Development**: SQLite (default, no setup required)
- **Production**: Switch to PostgreSQL by updating `DATABASES` in `settings.py`

---

## API Keys

### Required APIs:

1. **Kronos Labs API** - For AI interview agent
   - Sign up at: https://kronosai.com
   - Add `KRONOS_API_KEY` to `.env`

2. **ElevenLabs API** - For text-to-speech voice
   - Sign up at: https://elevenlabs.io
   - Add `ELEVEN_LABS_API_KEY` to `.env`

### Optional APIs:

3. **Supabase** - For cloud storage (optional, defaults to local storage)
   - Sign up at: https://supabase.com
   - Create a storage bucket named `interview-recordings`
   - Add credentials to `.env`

---

## Troubleshooting

### Redis Connection Issues (Windows)
```powershell
# Check if Redis is running in WSL
wsl redis-cli ping
# Should return: PONG

# If not running, start Redis:
wsl redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes
```

### Port Already in Use
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Database Migration Errors
```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py create_demo_user
```

---

## Contributing

This is a hackathon project. Contributions, issues, and feature requests are welcome!

---

## License

This project was created for the CCI Startup Hackathon and is available for educational purposes.

---

## Team

Created by Team CodeWrestlers for the CCI Startup Hackathon 2025.

---

## Acknowledgments

- LeetCode for problem database
- Kronos Labs for AI capabilities
- ElevenLabs for voice synthesis
- Piston API for code execution
