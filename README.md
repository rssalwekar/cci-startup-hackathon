# AI Coding Interview Platform

A comprehensive Django-based platform that provides AI-powered coding interviews with real-time chat, voice interaction, problem selection, and comprehensive feedback.

## Features

- **AI Interview Agent**: Conducts coding interviews with personalized problem selection from LeetCode
- **Voice Interaction**: Speech-to-text and text-to-speech using ElevenLabs for natural conversation
- **Real-time Chat**: Interactive chat interface with the AI interviewer
- **Dynamic Problem Selection**: LeetCode API integration with difficulty and topic preferences
- **Monaco IDE**: Built-in code editor with syntax highlighting and auto-completion
- **Test Case Execution**: Real-time code testing with Piston API
- **Resizable UI**: Drag-to-resize panels for optimal workspace layout
- **Interview Recording**: Video/audio recording of interview sessions
- **Results Page**: Comprehensive feedback with chat transcript, code, and AI analysis
- **WebSocket Communication**: Real-time updates and chat functionality
- **Session Management**: Track interview sessions and progress

### Setup Instructions

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment variables
# Create .env file with:
KRONOS_API_KEY=your_kronos_api_key_here
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here, SUPABASE credentials

# 3. Run migrations
python manage.py migrate

# 4. Create a user account (or use signup page)
python manage.py createsuperuser
```

### Starting the Application

**Option 1: Automated Startup (Windows with WSL - Recommended)**
```powershell
# Starts Redis and Django server automatically
.\start.ps1
```

**Option 2: Manual Startup**
```powershell
# Start Redis (if not already running)
.\start-redis.ps1

# Start Django server
python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application
```

**Option 3: Individual Commands**
```bash
# Terminal 1: Start Redis in WSL
wsl redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes

# Terminal 2: Start Django
python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application
```

### Usage

1. Navigate to `http://127.0.0.1:8000/`
2. Sign up for a new account at `/accounts/signup/` or login
3. Complete your profile and upload an avatar (optional)
3. Click "Start Interview" to begin
4. **Set Preferences**: Tell the AI your difficulty (easy/medium/hard) and topic preferences (arrays, strings, trees, etc.)
5. **Voice Interaction**: Use the microphone button to speak naturally with the AI
6. **Solve Problems**: Write code in the Monaco IDE and submit to run test cases
7. **Get Feedback**: Receive real-time AI guidance and comprehensive feedback
8. **View Results**: After ending the interview, see detailed results with video recording and analysis

### Advanced Features

- **Problem Name Requests**: Ask for specific problems like "two sum" or "valid parentheses"
- **Resizable Panels**: Drag the resize handles to customize your workspace layout
- **Test Case Execution**: Submit code to run against LeetCode test cases
- **Interview Recording**: Sessions are automatically recorded for review
- **Voice Controls**: Continuous speech recognition for hands-free interaction

## Project Structure

```
ai_interview/
├── models.py          # Database models
├── views.py           # View functions
├── ai_agent.py        # Core AI interview logic
├── consumers.py       # WebSocket consumers
├── routing.py         # WebSocket routing
├── urls.py           # URL patterns
├── admin.py          # Admin interface
└── management/
    └── commands/     # Custom management commands

templates/
├── ai_interview/     # Interview page templates
└── registration/     # Authentication templates
```

## AI Agent Features

The AI interview agent provides:

- **Skill Assessment**: Evaluates user preferences and skill level
- **Problem Selection**: Chooses appropriate LeetCode problems
- **Real-time Guidance**: Provides hints and feedback during problem solving
- **Code Analysis**: Reviews submitted code for correctness and quality
- **Comprehensive Feedback**: Generates detailed performance reports

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Real-time Communication**: Django Channels, WebSockets
- **AI Integration**: Kronos Labs Hermes API
- **Voice Services**: ElevenLabs API for natural speech synthesis
- **Code Execution**: Piston API for running test cases
- **Problem Database**: LeetCode GraphQL API
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML, CSS, JavaScript, Monaco Editor
- **Message Broker**: Redis
- **Media Handling**: Django FileField for video/audio storage

## API Endpoints

- `GET /ai-interview/start/` - Start new interview
- `GET /ai-interview/interview/<session_id>/` - Interview page
- `GET /ai-interview/results/<session_id>/` - Interview results page
- `POST /ai-interview/api/submit-code/<session_id>/` - Submit code
- `GET /ai-interview/api/session-data/<session_id>/` - Get session data
- `GET /ai-interview/get-function-signature/<session_id>/` - Get function signature
- `GET /ai-interview/get-test-cases/<session_id>/` - Get test cases
- `POST /ai-interview/api/synthesize-speech/` - Text-to-speech conversion
- `POST /ai-interview/api/get-last-ai-message/<session_id>/` - Get last AI message for re-speak
- `WebSocket /ws/interview/<session_id>/` - Real-time chat and code submission

## Contributing

This is a hackathon project. For production use, consider:

- Adding proper authentication and user management
- Implementing code execution sandbox
- Adding more problem categories and difficulty levels
- Enhancing the AI agent with more sophisticated guidance
- Adding session recording and playback features
- Implementing proper error handling and logging

## License

This project is part of a hackathon and is for educational purposes.
