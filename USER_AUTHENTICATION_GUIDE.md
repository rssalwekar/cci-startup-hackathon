# User Authentication & Profile System Setup Guide

This guide explains the new user authentication and profile management features added to the AI Coding Interview platform.

## New Features

### 1. **User Registration & Authentication**
- Custom signup page with email validation
- Enhanced login page with signup link
- Automatic user profile creation on signup
- Session management and logout functionality

### 2. **User Profiles**
- Extended user profiles with:
  - Avatar upload (stored in Supabase)
  - Bio and location
  - Social links (GitHub, LinkedIn, Website)
  - Preferred programming language
  - Statistics (total interviews, problems solved, average score)

### 3. **Interview History**
- View all past interviews with filtering and search
- Filter by status (completed, active, preparing)
- Filter by difficulty (easy, medium, hard)
- Pagination support
- Display scores and performance metrics
- Interview recordings playback

### 4. **Interview Recordings**
- Support for audio, video, and screen recordings
- Recordings stored in Supabase Storage
- Playback in interview detail view
- Recording duration tracking

### 5. **Performance Metrics**
- Overall performance score (0-100)
- Code quality score
- Communication score
- Problem solving score

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

New packages added:
- `supabase==2.9.0` - Supabase client for storage
- `Pillow==11.0.0` - Image processing for avatars

### 2. Set Up Supabase

1. Create a Supabase account at https://supabase.com
2. Create a new project
3. Go to Settings > API to get your credentials:
   - Project URL
   - Anon/Public key
4. Create a storage bucket named `interview-recordings`:
   - Go to Storage in Supabase dashboard
   - Click "New bucket"
   - Name it `interview-recordings`
   - Make it public for easy access
   - Set appropriate file size limits

### 3. Environment Variables

Update your `.env` file with Supabase credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key-here
SUPABASE_BUCKET=interview-recordings
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the new `UserProfile` model and update the `InterviewSession` model with recording fields.

### 5. Create Profiles for Existing Users

If you have existing users, their profiles will be created automatically. You can also run:

```python
python manage.py shell
from django.contrib.auth.models import User
from ai_interview.models import UserProfile

for user in User.objects.all():
    UserProfile.objects.get_or_create(user=user)
```

### 6. Start Services

Make sure both Redis and Django are running:

```bash
# Start Redis (if using WSL)
wsl redis-server --bind 0.0.0.0 --protected-mode no

# Start Django (in another terminal)
python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application
```

## New URLs

### Authentication
- `/accounts/signup/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout

### Profile Management
- `/ai-interview/profile/` - View user profile
- `/ai-interview/profile/edit/` - Edit profile
- `/ai-interview/profile/upload-avatar/` - Upload avatar (API endpoint)

### Interview History
- `/ai-interview/history/` - View all interviews with filters
- `/ai-interview/history/<id>/` - View interview details
- `/ai-interview/history/<id>/delete/` - Delete interview (API endpoint)

## Database Schema Changes

### New Model: `UserProfile`
```python
- user (OneToOne with User)
- bio (TextField)
- avatar_url (URLField)
- location (CharField)
- github_url, linkedin_url, website_url (URLField)
- preferred_language (CharField)
- total_interviews, total_problems_solved (IntegerField)
- average_score (FloatField)
- created_at, updated_at (DateTimeField)
```

### Updated Model: `InterviewSession`
```python
# New fields:
- audio_recording_url (URLField)
- video_recording_url (URLField)
- screen_recording_url (URLField)
- recording_duration (IntegerField)
- performance_score (FloatField)
- code_quality_score (FloatField)
- communication_score (FloatField)
- problem_solving_score (FloatField)
```

## Usage Guide

### For Users

1. **Sign Up**: Visit `/accounts/signup/` to create a new account
2. **Complete Profile**: After login, go to Profile > Edit Profile to add:
   - Profile picture
   - Bio and location
   - Social media links
   - Preferred programming language

3. **Start Interviews**: Click "New Interview" to begin a coding session
4. **View History**: Access all past interviews from the History page
5. **Review Performance**: Check scores, recordings, and feedback in interview details

### For Developers

#### Uploading Recordings

To upload a recording during an interview session:

```python
from ai_interview.supabase_service import supabase_service

# Upload audio recording
success, url = supabase_service.upload_recording(
    file_data=audio_bytes,
    user_id=request.user.id,
    session_id=session.id,
    recording_type='audio'
)

if success:
    session.audio_recording_url = url
    session.save()
```

#### Updating Profile Statistics

Statistics are automatically updated when viewing the profile:

```python
profile = request.user.profile
profile.update_statistics()  # Recalculates all stats
```

## File Structure

```
ai_interview/
├── auth_views.py              # New authentication views
├── supabase_service.py        # Supabase integration
├── models.py                  # Updated with UserProfile
├── admin.py                   # Updated with UserProfile admin
└── urls.py                    # Updated with new routes

templates/
├── registration/
│   ├── signup.html           # New signup page
│   └── login.html            # Updated with signup link
└── ai_interview/
    ├── profile.html          # User profile page
    ├── edit_profile.html     # Profile editing
    ├── history.html          # Interview history list
    └── interview_detail.html # Interview details with recordings
```

## Testing

1. **Test Signup**: Create a new account at `/accounts/signup/`
2. **Test Profile**: Upload an avatar and edit profile info
3. **Test History**: Complete an interview and view it in history
4. **Test Filters**: Use the history filters to search interviews
5. **Test Recordings**: If you implement recording, test playback

## Troubleshooting

### Supabase Connection Issues
- Verify your `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check if the bucket `interview-recordings` exists
- Ensure the bucket is set to public access

### Migration Errors
```bash
# Reset migrations if needed (WARNING: deletes data)
python manage.py migrate ai_interview zero
python manage.py migrate
```

### Profile Not Created
```bash
# Manually create profiles for existing users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from ai_interview.models import UserProfile
>>> for user in User.objects.all():
...     UserProfile.objects.get_or_create(user=user)
```

## Next Steps

To fully implement recording functionality:

1. **Client-Side Recording**: Add JavaScript MediaRecorder API to capture audio/video
2. **Upload to Supabase**: Send recorded blobs to the upload endpoint
3. **Update Session**: Save recording URLs to the InterviewSession model
4. **Playback**: Recordings will automatically appear in interview details

## Contributing

When adding new features:
1. Update models in `models.py`
2. Create migrations with `python manage.py makemigrations`
3. Add views in `auth_views.py` or `views.py`
4. Create templates in `templates/ai_interview/`
5. Update URLs in `urls.py`
6. Test all functionality before committing

## Security Notes

- Avatar uploads are limited to 5MB
- Only image files are accepted for avatars
- Supabase handles authentication and storage security
- Use environment variables for all sensitive credentials
- Never commit `.env` file to version control
