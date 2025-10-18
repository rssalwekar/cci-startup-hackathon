# Quick Start Script for Windows PowerShell

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  MockInterview.AI - Quick Setup Script" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/8] Checking Python installation..." -ForegroundColor Yellow
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCheck) {
    $pythonVersion = python --version 2>&1
    Write-Host "CheckMark Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "X Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "[2/8] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "CheckMark Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "CheckMark Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/8] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "CheckMark Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[4/8] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "CheckMark Dependencies installed" -ForegroundColor Green

# Check for .env file
Write-Host ""
Write-Host "[5/8] Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "CheckMark .env file exists" -ForegroundColor Green
} else {
    Write-Host "Warning .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "CheckMark .env file created from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "Warning IMPORTANT: Please edit .env and add your Supabase credentials!" -ForegroundColor Red
    Write-Host "  - SUPABASE_URL" -ForegroundColor Red
    Write-Host "  - SUPABASE_KEY" -ForegroundColor Red
    Write-Host "  - SUPABASE_SERVICE_KEY" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to open .env file..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    notepad ".env"
}

# Generate secret key if needed
Write-Host ""
Write-Host "[6/8] Checking Django secret key..." -ForegroundColor Yellow
$envContent = Get-Content ".env" -Raw
if ($envContent -match "SECRET_KEY=your_django_secret_key") {
    Write-Host "Warning Generating new Django secret key..." -ForegroundColor Yellow
    $secretKey = python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    $envContent = $envContent -replace "SECRET_KEY=your_django_secret_key", "SECRET_KEY=$secretKey"
    Set-Content ".env" $envContent
    Write-Host "CheckMark New secret key generated" -ForegroundColor Green
} else {
    Write-Host "CheckMark Secret key already configured" -ForegroundColor Green
}

# Run migrations
Write-Host ""
Write-Host "[7/8] Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations --noinput 2>&1 | Out-Null
python manage.py migrate --noinput 2>&1 | Out-Null
Write-Host "CheckMark Database migrations completed" -ForegroundColor Green

# Collect static files
Write-Host ""
Write-Host "[8/8] Setting up static files..." -ForegroundColor Yellow
if (-not (Test-Path "static")) {
    New-Item -ItemType Directory -Path "static" | Out-Null
}
Write-Host "CheckMark Static files directory ready" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Make sure your .env file has valid Supabase credentials"
Write-Host "2. Run: python manage.py createsuperuser (optional)"
Write-Host "3. Run: python manage.py runserver"
Write-Host "4. Visit: http://127.0.0.1:8000"
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "- README.md - Complete setup guide"
Write-Host "- API_INTEGRATION.md - API documentation"
Write-Host "- SUPABASE_SETUP.md - Supabase configuration"
Write-Host ""
Write-Host "To start the server now, run:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
