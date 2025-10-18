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

## Setup Instructions

### Prerequisites

- Python 3.8+
- Redis server (for WebSocket channels)
- Kronos Labs API key

### Installation

1. **Clone the repository and navigate to the project directory**

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework channels channels-redis kronoslabs python-dotenv
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   KRONOS_API_KEY=your_kronos_api_key_here
   SECRET_KEY=django-insecure-qk%9y7uv_a!e+5b#8^b@2jjlzi9beh&v=3*s#a$av0jbmxlc27
   DEBUG=True
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create demo user and populate problems**
   ```bash
   python manage.py create_demo_user
   python manage.py populate_problems
   ```

7. **Start Redis server** (required for WebSocket functionality)
   ```bash
   redis-server
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
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
