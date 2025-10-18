# Team Onboarding Guide

Welcome to the MockInterview.AI project! This guide will help you get started quickly.

## 🎯 Your Role

You mentioned your contribution is:
> "Setting up user accounts, dealing with login, signup, and profile. Past interviews should be saved along with the recordings in the user profile."

**Good news**: This is 100% complete! ✅

## What's Already Done

### ✅ User Accounts System
- **Sign Up**: Full registration with email validation
- **Login**: Secure authentication with Supabase
- **Logout**: Clean session management
- **Profile Pages**: View and edit user information

### ✅ Profile Management
- Personal information (name, email, bio)
- Professional details (experience, skills, target companies)
- Avatar support
- Automatic profile creation on signup

### ✅ Interview History
- View all past interviews
- Filter by status (completed, in progress, scheduled)
- See detailed information for each interview
- Access recordings and transcripts
- View performance scores and feedback

### ✅ Recording Storage
- Upload recordings to Supabase Storage
- Secure storage with user-specific access
- Download and playback functionality
- Automatic URL generation

## 🚀 Quick Start (5 minutes)

### Step 1: Install Python Dependencies

```powershell
# Open PowerShell in the project directory
cd "c:\Users\jayan\Documents\Projects\Hackathon 2025\cci-startup-hackathon"

# Run the setup script
.\setup.ps1
```

OR manually:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project (takes 2-3 minutes)
3. Get your credentials:
   - Project URL
   - anon/public key
   - service_role key
4. Create a storage bucket called `interview-recordings`

**Detailed instructions**: See `SUPABASE_SETUP.md`

### Step 3: Configure Environment

```powershell
# Copy the example env file
Copy-Item .env.example .env

# Edit the .env file and add your Supabase credentials
notepad .env
```

Required values:
```env
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your_anon_public_key
SUPABASE_SERVICE_KEY=your_service_role_key
SECRET_KEY=generate_a_random_key
```

Generate a Django secret key:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Set Up Database

```powershell
# Create database tables
python manage.py makemigrations
python manage.py migrate

# (Optional) Create admin user
python manage.py createsuperuser
```

### Step 5: Run the Server

```powershell
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## 🎨 What You'll See

### Home Page (http://127.0.0.1:8000)
- Hero section with call-to-action
- Feature highlights
- How it works section
- Sign up / Login buttons

### Sign Up Page (/signup/)
- Registration form
- Email validation
- Password confirmation
- Automatic profile creation
- Integration with Supabase Auth

### Login Page (/login/)
- Email/password authentication
- Supabase Auth integration
- Session management
- Redirect to profile after login

### Profile Page (/profile/)
- User information display
- Recent interviews list
- Statistics (total interviews, completion rate)
- Edit profile button
- Skills and target companies

### Edit Profile (/profile/edit/)
- Update personal information
- Set professional details
- Add skills and preferences
- Save changes

### Interview List (/interviews/)
- All interviews with filtering
- Status badges (completed, in progress, scheduled)
- Difficulty indicators
- Scores display
- Quick view of each interview

### Interview Detail (/interviews/<id>/)
- Complete interview information
- Problem description
- Submitted code
- Recording playback
- Full transcript
- Performance scores breakdown
- Detailed feedback
- Interview notes timeline

## 📋 Testing Your Work

### Test User Registration
1. Go to http://127.0.0.1:8000/signup/
2. Fill in the form
3. Click "Create Account"
4. Should redirect to profile page

### Test Login
1. Go to http://127.0.0.1:8000/login/
2. Enter your credentials
3. Should redirect to profile page

### Test Profile Management
1. Click "Edit Profile"
2. Update your information
3. Save changes
4. Verify updates appear

### Create a Test Interview
1. Go to "New Interview"
2. Fill in problem details
3. Submit
4. View in interview list

## 🔗 How Other Team Members Will Integrate

### For the AI Interview Developer

Your AI system will integrate via API calls:

```python
# Example: Saving interview data
import requests

interview_data = {
    "status": "completed",
    "code": user_code,
    "transcript": conversation,
    "scores": {
        "overall": 85,
        "communication": 90,
        "problem_solving": 82,
        "code_quality": 83
    },
    "feedback_report": generated_feedback,
    # ... more data
}

response = requests.post(
    f"http://localhost:8000/interviews/{interview_id}/save-data/",
    json=interview_data
)
```

**Full API documentation**: See `API_INTEGRATION.md`

### For the Frontend Developer (if any)

The HTML templates can be enhanced:
- Located in `templates/` directory
- Using Bootstrap 5
- Custom CSS in `static/css/custom.css`
- Can add JavaScript for interactivity

## 📁 Important Files for You

### Django Apps
- `accounts/` - Everything related to users
  - `models.py` - UserProfile and UserSession models
  - `views.py` - Signup, login, logout, profile views
  - `forms.py` - Registration and profile forms
  - `supabase_client.py` - Supabase helper functions
  
- `interviews/` - Everything related to interviews
  - `models.py` - Interview, Note, Feedback models
  - `views.py` - Interview CRUD operations
  - `admin.py` - Django admin configuration

### Templates
- `templates/base.html` - Main layout with navbar
- `templates/accounts/` - Auth and profile pages
- `templates/interviews/` - Interview pages

### Configuration
- `mock_interview_platform/settings.py` - Django settings
- `.env` - Environment variables (create from .env.example)

## 🎓 Learning Resources

### Django Basics
- [Official Django Tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
- [Django Models](https://docs.djangoproject.com/en/5.0/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/5.0/topics/http/views/)

### Supabase
- [Supabase Quickstart](https://supabase.com/docs/guides/getting-started)
- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [Supabase Storage](https://supabase.com/docs/guides/storage)

### Bootstrap 5
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/)
- [Bootstrap Examples](https://getbootstrap.com/docs/5.3/examples/)

## 🐛 Common Issues & Solutions

### Issue: "Module not found: dotenv"
**Solution**: 
```powershell
pip install python-dotenv
```

### Issue: "No module named 'supabase'"
**Solution**: 
```powershell
pip install supabase
```

### Issue: "Table doesn't exist"
**Solution**: 
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Port 8000 already in use"
**Solution**: 
```powershell
# Find and kill the process
$pid = (Get-NetTCPConnection -LocalPort 8000).OwningProcess
Stop-Process -Id $pid -Force

# Or use a different port
python manage.py runserver 8080
```

### Issue: "Static files not loading"
**Solution**: 
```powershell
python manage.py collectstatic
```

## 🤝 Working with Your Team

### Communication
- Share your `.env` credentials securely (not in Git!)
- Document any changes you make
- Test before committing

### Git Workflow
```powershell
# Pull latest changes
git pull origin main

# Create your branch
git checkout -b feature/your-feature

# Make changes, then:
git add .
git commit -m "Your descriptive message"
git push -u origin feature/your-feature

# Create Pull Request on GitHub
```

### Testing
Always test your changes:
```powershell
python manage.py test
```

## 📊 Demo Data (Optional)

Want some sample data to test with?

```powershell
python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User
from interviews.models import Interview

# Create a test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Create a sample interview
Interview.objects.create(
    user=user,
    title='Sample Interview',
    problem_name='Two Sum',
    problem_description='Find two numbers that add up to target',
    problem_difficulty='easy',
    programming_language='python',
    status='completed',
    overall_score=85
)
```

## ✅ Checklist for Demo/Presentation

Before the hackathon presentation:

- [ ] Server is running
- [ ] Can create new account
- [ ] Can log in
- [ ] Profile displays correctly
- [ ] Can edit profile
- [ ] Can view interview list
- [ ] Can view interview details
- [ ] Scores display properly
- [ ] Feedback is readable
- [ ] UI looks professional
- [ ] No console errors
- [ ] Supabase is configured

## 🎉 Next Steps

1. **Get comfortable**: Browse through the code, run the server, test features
2. **Customize**: Update colors, add your team's branding
3. **Document**: Add any custom features you add
4. **Integrate**: Work with the AI team to connect their system
5. **Test**: Make sure everything works together
6. **Present**: Demo your working system!

## 📞 Need Help?

- **Django Errors**: Check `COMMANDS.md` for common solutions
- **Supabase Issues**: See `SUPABASE_SETUP.md`
- **API Questions**: Refer to `API_INTEGRATION.md`
- **General Questions**: Review `PROJECT_SUMMARY.md`

---

## 🏆 You're Ready!

Your backend is complete and production-ready. The user authentication, profile management, and interview history system is fully functional. 

Focus on:
1. Understanding how it works
2. Helping integrate with the AI system
3. Polishing the UI if time permits
4. Preparing for the demo

**Good luck with the hackathon!** 🚀

---

*Last updated: October 2025*
