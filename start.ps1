# Complete Startup Script for AI Interview Platform
# Starts Redis and Django development server

Write-Host "`n=== AI Interview Platform Startup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check and start Redis
Write-Host "[1/2] Checking Redis..." -ForegroundColor Yellow

$redisRunning = $false
try {
    $pingResult = wsl redis-cli -h 172.27.247.142 ping 2>$null
    if ($pingResult -match "PONG") {
        $redisRunning = $true
    }
} catch {
    $redisRunning = $false
}

if ($redisRunning) {
    Write-Host "      ✓ Redis is already running" -ForegroundColor Green
} else {
    Write-Host "      Starting Redis..." -ForegroundColor Gray
    wsl redis-cli shutdown 2>$null
    Start-Sleep -Seconds 1
    wsl redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes
    Start-Sleep -Seconds 2
    
    $pingResult = wsl redis-cli -h 172.27.247.142 ping 2>$null
    if ($pingResult -match "PONG") {
        Write-Host "      ✓ Redis started successfully (172.27.247.142:6379)" -ForegroundColor Green
    } else {
        Write-Host "      ✗ Redis failed to start" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Start Django Server
Write-Host "`n[2/2] Starting Django server..." -ForegroundColor Yellow
Write-Host "      Server will be available at: https://127.0.0.1:8000" -ForegroundColor Gray
Write-Host "      Press Ctrl+C to stop the server`n" -ForegroundColor Gray
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

# Start Django with Daphne (for WebSocket support)
python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application
