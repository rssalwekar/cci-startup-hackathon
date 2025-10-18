# AI Coding Interview Platform

A Django-based platform that provides AI-powered coding interviews with real-time chat, problem selection, and comprehensive feedback.

## Features

- **AI Interview Agent**: Conducts coding interviews with personalized problem selection
- **Real-time Chat**: Interactive chat interface with the AI interviewer
- **Problem Database**: LeetCode-style problems with varying difficulty levels
- **Code Editor**: Built-in IDE for writing and testing solutions
- **WebSocket Communication**: Real-time updates and chat functionality
- **Session Management**: Track interview sessions and progress
- **Comprehensive Feedback**: AI-generated feedback and performance analysis

### Setup Instructions

```bash
# 1. Install dependencies
pip install -r requirements.txt
brew install redis

# 2. Set up environment
cp .env.example .env  # Add KRONOS_API_KEY

# 3. Run migrations
python manage.py migrate
python manage.py create_demo_user

# 4. Start services
brew services start redis
python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application

# 5. Kill server
pkill -f daphne
```

### Usage

1. Navigate to `http://127.0.0.1:8000/`
2. Login with demo credentials:
   - Username: `demo`
   - Password: `demo123`
3. Click "Start Interview" to begin
4. Chat with the AI interviewer to set your preferences
5. Solve the selected coding problem with real-time guidance

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
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML, CSS, JavaScript
- **Message Broker**: Redis

## API Endpoints

- `GET /ai-interview/start/` - Start new interview
- `GET /ai-interview/interview/<session_id>/` - Interview page
- `POST /ai-interview/api/submit-code/<session_id>/` - Submit code
- `GET /ai-interview/api/session-data/<session_id>/` - Get session data
- `WebSocket /ws/interview/<session_id>/` - Real-time chat

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