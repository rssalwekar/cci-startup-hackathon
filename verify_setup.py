# Verify Setup - Test Script
# Run this to make sure everything is configured correctly

import os
import sys
from pathlib import Path

print("=" * 60)
print("MockInterview.AI - Setup Verification")
print("=" * 60)
print()

# Check Python version
print("[1/10] Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 8:
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
else:
    print(f"✗ Python version too old: {version.major}.{version.minor}")
    print("   Please upgrade to Python 3.8 or higher")
    sys.exit(1)

# Check if we're in a virtual environment
print("\n[2/10] Checking virtual environment...")
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✓ Virtual environment is active")
else:
    print("⚠ Virtual environment not detected")
    print("   Consider activating venv: .\\venv\\Scripts\\Activate.ps1")

# Check required packages
print("\n[3/10] Checking required packages...")
required_packages = [
    'django',
    'supabase',
    'dotenv',
    'psycopg2',
    'PIL',
    'requests',
    'corsheaders'
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package if package != 'PIL' else 'PIL')
        print(f"✓ {package}")
    except ImportError:
        print(f"✗ {package} (missing)")
        missing_packages.append(package)

if missing_packages:
    print("\n⚠ Missing packages detected. Install with:")
    print("   pip install -r requirements.txt")

# Check .env file
print("\n[4/10] Checking environment configuration...")
if Path('.env').exists():
    print("✓ .env file exists")
    
    # Check if .env has required values
    from dotenv import load_dotenv
    load_dotenv()
    
    required_env_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY',
        'SUPABASE_SERVICE_KEY',
        'SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
            print(f"✗ {var} (not configured)")
        else:
            print(f"✓ {var}")
    
    if missing_vars:
        print("\n⚠ Please configure these variables in .env file")
else:
    print("✗ .env file not found")
    print("   Copy .env.example to .env and configure it")

# Check Django setup
print("\n[5/10] Checking Django installation...")
try:
    import django
    print(f"✓ Django {django.get_version()}")
except ImportError:
    print("✗ Django not installed")

# Check if Django can be imported
print("\n[6/10] Checking Django configuration...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mock_interview_platform.settings')
    import django
    django.setup()
    print("✓ Django settings loaded successfully")
except Exception as e:
    print(f"✗ Django configuration error: {e}")

# Check database
print("\n[7/10] Checking database...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✓ Database connection working")
except Exception as e:
    print(f"✗ Database error: {e}")
    print("   Run: python manage.py migrate")

# Check if migrations are applied
print("\n[8/10] Checking migrations...")
try:
    from django.db.migrations.executor import MigrationExecutor
    from django.db import connection
    
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    plan = executor.migration_plan(targets)
    
    if plan:
        print(f"⚠ {len(plan)} unapplied migration(s)")
        print("   Run: python manage.py migrate")
    else:
        print("✓ All migrations applied")
except Exception as e:
    print(f"✗ Migration check failed: {e}")

# Check if accounts and interviews apps are installed
print("\n[9/10] Checking Django apps...")
try:
    from django.apps import apps
    
    if apps.is_installed('accounts'):
        print("✓ accounts app installed")
    else:
        print("✗ accounts app not installed")
    
    if apps.is_installed('interviews'):
        print("✓ interviews app installed")
    else:
        print("✗ interviews app not installed")
except Exception as e:
    print(f"✗ App check failed: {e}")

# Check Supabase connection
print("\n[10/10] Testing Supabase connection...")
try:
    from accounts.supabase_client import SupabaseClient
    
    client = SupabaseClient.get_client()
    print("✓ Supabase client initialized")
    
    # Try to list storage buckets
    try:
        buckets = client.storage.list_buckets()
        print(f"✓ Supabase connection working ({len(buckets)} bucket(s) found)")
    except Exception as e:
        print(f"⚠ Supabase connection warning: {e}")
        print("   Check your SUPABASE_KEY in .env")
        
except Exception as e:
    print(f"✗ Supabase setup error: {e}")
    print("   Configure Supabase credentials in .env")

# Summary
print("\n" + "=" * 60)
print("Verification Complete!")
print("=" * 60)
print("\nNext steps:")
print("1. Fix any issues marked with ✗ or ⚠")
print("2. Run: python manage.py migrate (if needed)")
print("3. Run: python manage.py createsuperuser (optional)")
print("4. Run: python manage.py runserver")
print("5. Visit: http://127.0.0.1:8000")
print("\nFor detailed instructions, see README.md")
print()
