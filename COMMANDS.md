# Development Commands

## Virtual Environment

### Activate
```powershell
.\venv\Scripts\Activate.ps1
```

### Deactivate
```powershell
deactivate
```

## Django Commands

### Run Development Server
```powershell
python manage.py runserver
```

### Run on Different Port
```powershell
python manage.py runserver 8080
```

### Make Migrations
```powershell
python manage.py makemigrations
```

### Apply Migrations
```powershell
python manage.py migrate
```

### Create Superuser
```powershell
python manage.py createsuperuser
```

### Open Django Shell
```powershell
python manage.py shell
```

### Collect Static Files
```powershell
python manage.py collectstatic
```

### Create New App
```powershell
python manage.py startapp app_name
```

## Database Commands

### Reset Database (SQLite)
```powershell
Remove-Item db.sqlite3
python manage.py migrate
```

### Show Migrations
```powershell
python manage.py showmigrations
```

### SQL for Migration
```powershell
python manage.py sqlmigrate app_name migration_number
```

## Testing

### Run All Tests
```powershell
python manage.py test
```

### Run Specific App Tests
```powershell
python manage.py test accounts
python manage.py test interviews
```

### Run with Coverage
```powershell
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Creates htmlcov/index.html
```

## Dependency Management

### Install New Package
```powershell
pip install package_name
pip freeze > requirements.txt
```

### Update All Packages
```powershell
pip install --upgrade -r requirements.txt
```

### List Installed Packages
```powershell
pip list
```

## Git Commands

### Initial Setup
```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

### Daily Workflow
```powershell
git status
git add .
git commit -m "Your commit message"
git push
```

### Create Feature Branch
```powershell
git checkout -b feature/your-feature-name
# Make changes
git add .
git commit -m "Add your feature"
git push -u origin feature/your-feature-name
```

### Pull Latest Changes
```powershell
git pull origin main
```

## Useful Django Queries (in shell)

### Get All Users
```python
from django.contrib.auth.models import User
users = User.objects.all()
```

### Get User Profile
```python
from accounts.models import UserProfile
profile = UserProfile.objects.get(user__username='username')
```

### Get User's Interviews
```python
from interviews.models import Interview
interviews = Interview.objects.filter(user__username='username')
```

### Create Test Interview
```python
from django.contrib.auth.models import User
from interviews.models import Interview

user = User.objects.first()
interview = Interview.objects.create(
    user=user,
    title="Test Interview",
    problem_name="Two Sum",
    problem_description="Test description",
    difficulty="medium",
    programming_language="python"
)
```

## Environment Variables

### View Current Environment
```powershell
Get-Content .env
```

### Edit Environment
```powershell
notepad .env
```

## Supabase Testing

### Test Supabase Connection
```python
from accounts.supabase_client import SupabaseClient

client = SupabaseClient.get_client()
print("Connected!")
```

### Test Authentication
```python
from accounts.supabase_client import sign_up_user, sign_in_user

# Sign up
result = sign_up_user("test@example.com", "password123")
print(result)

# Sign in
result = sign_in_user("test@example.com", "password123")
print(result)
```

## Production Deployment

### Collect Static Files for Production
```powershell
python manage.py collectstatic --noinput
```

### Check Deployment Readiness
```powershell
python manage.py check --deploy
```

### Generate Requirements for Production
```powershell
pip freeze > requirements.txt
```

## Troubleshooting

### Clear Python Cache
```powershell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force
```

### Reset Migrations (Careful!)
```powershell
# Delete migration files
Get-ChildItem -Path . -Include "0*.py" -Recurse | Where-Object { $_.DirectoryName -like "*migrations*" } | Remove-Item

# Delete database
Remove-Item db.sqlite3

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

### Check Port Usage
```powershell
netstat -ano | findstr :8000
```

### Kill Process on Port 8000
```powershell
# Find PID
$pid = (Get-NetTCPConnection -LocalPort 8000).OwningProcess
# Kill process
Stop-Process -Id $pid -Force
```

## Quick Setup (New Machine)

```powershell
# Run all setup commands at once
.\setup.ps1
```

Or manually:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env with your credentials
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Maintenance

### Check Django Version
```powershell
python -m django --version
```

### Update Django
```powershell
pip install --upgrade django
pip freeze > requirements.txt
```

### View Logs (if configured)
```powershell
Get-Content -Path "logs/django.log" -Tail 50 -Wait
```

## Common Issues

### Import Error
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1
```

### Migration Conflicts
```powershell
python manage.py migrate --fake app_name migration_name
```

### Static Files Not Loading
```powershell
python manage.py collectstatic --clear
python manage.py collectstatic
```

---

Save this file for quick reference during development!
