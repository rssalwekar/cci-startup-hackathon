# MockInterview.AI - SWE Interview Practice Platform

A comprehensive web application for practicing technical interviews with AI-powered feedback. Built for the CCI Startup Hackathon 2025.

## 🎯 Features

### User Authentication & Profiles
- **Sign Up/Login/Logout**: Secure authentication powered by Supabase Auth
- **User Profiles**: Manage personal information, skills, and target companies
- **Session Management**: Persistent login sessions with automatic token refresh

### Interview Management
- **Interview History**: View all past interviews with detailed information
- **Recording Storage**: Audio/video recordings stored securely in Supabase Storage
- **Transcripts**: Full interview transcripts for review
- **Code Submissions**: Save and review submitted code solutions

### AI Feedback & Analytics
- **Performance Scores**: Overall, communication, problem-solving, and code quality scores
- **Detailed Reports**: Comprehensive feedback on strengths and areas for improvement
- **Category Breakdown**: Feedback organized by communication, problem-solving, testing, etc.
- **Interview Notes**: Timestamped observations and hints given during the interview

## 🛠️ Tech Stack

- **Backend**: Django 5.0.1
- **Database**: SQLite (development) / PostgreSQL (production via Supabase)
- **Authentication**: Supabase Auth
- **Storage**: Supabase Storage (for recordings)
- **Frontend**: Bootstrap 5.3, Django Templates
- **Icons**: Bootstrap Icons

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Supabase account (free tier available)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```powershell
git clone <repository-url>
cd cci-startup-hackathon
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a new project
2. In your Supabase dashboard:
   - Go to **Settings** → **API**
   - Copy your **Project URL** and **anon/public key**
   - Copy your **service_role key** (for admin operations)
3. Create a storage bucket called `interview-recordings`:
   - Go to **Storage** in the sidebar
   - Click **New Bucket**
   - Name it `interview-recordings`
   - Set it to **Public** or **Private** based on your needs

### 5. Configure Environment Variables

Copy the example environment file and fill in your Supabase credentials:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your credentials:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

To generate a Django secret key, run:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run Database Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser (Optional)

```powershell
python manage.py createsuperuser
```

### 8. Run the Development Server

```powershell
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser!

## 📁 Project Structure

```
cci-startup-hackathon/
├── accounts/                    # User authentication & profiles
│   ├── models.py               # UserProfile, UserSession models
│   ├── views.py                # Auth views (signup, login, logout, profile)
│   ├── forms.py                # Authentication forms
│   ├── supabase_client.py      # Supabase integration utilities
│   ├── urls.py                 # Account-related URLs
│   └── admin.py                # Django admin configuration
├── interviews/                  # Interview management
│   ├── models.py               # Interview, InterviewNote, InterviewFeedbackPoint
│   ├── views.py                # Interview CRUD operations
│   ├── urls.py                 # Interview-related URLs
│   └── admin.py                # Django admin configuration
├── mock_interview_platform/     # Django project settings
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI configuration
├── templates/                   # HTML templates
│   ├── base.html               # Base template with navbar/footer
│   ├── accounts/               # Auth templates
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── profile.html
│   │   └── edit_profile.html
│   └── interviews/             # Interview templates
│       ├── interview_list.html
│       ├── interview_detail.html
│       ├── create_interview.html
│       └── confirm_delete.html
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔗 API Endpoints

### Accounts

- `GET /` - Home page
- `GET /signup/` - Sign up page
- `POST /signup/` - Create new account
- `GET /login/` - Login page
- `POST /login/` - Authenticate user
- `GET /logout/` - Logout user
- `GET /profile/` - View user profile
- `GET /profile/edit/` - Edit profile page
- `POST /profile/edit/` - Update profile

### Interviews

- `GET /interviews/` - List all interviews
- `GET /interviews/<id>/` - View interview details
- `GET /interviews/create/` - Create interview page
- `POST /interviews/create/` - Create new interview
- `POST /interviews/<id>/upload-recording/` - Upload audio/video recording
- `POST /interviews/<id>/save-data/` - Save interview data (for AI integration)
- `POST /interviews/<id>/delete/` - Delete interview

## 💾 Database Models

### UserProfile
Extends Django's User model with additional fields:
- `supabase_user_id`: Linked Supabase Auth user
- `bio`, `avatar_url`, `phone_number`
- `years_of_experience`
- `target_companies`, `preferred_languages`

### UserSession
Tracks Supabase authentication sessions:
- `supabase_session_token`, `refresh_token`
- `expires_at`, `is_active`

### Interview
Main interview data:
- Problem details (name, description, difficulty, link)
- Status (scheduled, in_progress, completed)
- Timing (scheduled_at, started_at, completed_at)
- Recording (recording_url, transcript)
- Code (submitted_code, programming_language)
- Scores (overall, communication, problem_solving, code_quality)
- Feedback (report, strengths, areas_for_improvement)

### InterviewNote
Timestamped notes during the interview:
- `content`, `note_type`, `timestamp`

### InterviewFeedbackPoint
Individual feedback items categorized by:
- `category` (communication, problem_solving, code_quality, etc.)
- `is_positive` (strength vs. improvement area)
- `point` (the actual feedback text)

## 🔌 Integrating with AI Interview System

Your team's AI interview system can interact with this backend through the following endpoints:

### 1. Create Interview
```python
POST /interviews/create/
{
    "title": "Mock Interview #1",
    "problem_name": "Two Sum",
    "problem_description": "Given an array of integers...",
    "difficulty": "easy",
    "language": "python"
}
```

### 2. Update Interview Status
```python
POST /interviews/<id>/save-data/
{
    "status": "in_progress",  # or "completed"
    "code": "def twoSum(nums, target):\n    ...",
    "transcript": "AI: Let's start with...",
    "scores": {
        "overall": 85,
        "communication": 90,
        "problem_solving": 82,
        "code_quality": 83
    },
    "feedback_report": "Overall, you did well...",
    "strengths": "Good communication, clear thought process",
    "areas_for_improvement": "Consider edge cases earlier",
    "feedback_points": [
        {
            "category": "communication",
            "is_positive": true,
            "point": "Clearly explained your approach"
        }
    ],
    "notes": [
        {
            "content": "User asked for clarification on input constraints",
            "type": "question_asked",
            "timestamp": "2025-01-15T10:30:00Z"
        }
    ]
}
```

### 3. Upload Recording
```python
POST /interviews/<id>/upload-recording/
Content-Type: multipart/form-data

recording: <audio/video file>
```

## 🎨 Customization

### Adding New Features

1. **Models**: Add new fields to `accounts/models.py` or `interviews/models.py`
2. **Views**: Create new views in the respective `views.py` files
3. **Templates**: Add new templates in the `templates/` directory
4. **URLs**: Update `urls.py` files to route to new views

### Styling

The project uses Bootstrap 5. Custom styles are in `templates/base.html` within the `<style>` tag. You can:
- Modify color scheme (CSS variables at top of `<style>`)
- Add custom CSS files in a `static/` directory
- Override Bootstrap classes

## 🧪 Testing

Run Django tests:

```powershell
python manage.py test
```

## 🚢 Deployment

### Using Heroku

1. Install Heroku CLI
2. Create a new Heroku app
3. Set environment variables in Heroku dashboard
4. Deploy:

```powershell
git push heroku main
```

### Using Railway/Render

1. Connect your GitHub repository
2. Set environment variables in the dashboard
3. Deploy automatically on push

### Environment Variables for Production

Make sure to set:
- `DEBUG=False`
- `SECRET_KEY=<strong-secret-key>`
- `ALLOWED_HOSTS=yourdomain.com`
- All Supabase credentials

## 🤝 Contributing

This is a hackathon project! Team members can:

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Create a pull request

## 📝 License

This project was created for the CCI Startup Hackathon 2025.

## 🙋‍♂️ Support

For questions or issues, contact the team or create an issue in the repository.

## 🎓 Learn More

- [Django Documentation](https://docs.djangoproject.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

Built with ❤️ for CCI Startup Hackathon 2025
