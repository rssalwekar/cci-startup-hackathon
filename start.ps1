Write-Host "Starting AI Interview Platform..." -ForegroundColor Cyan

Write-Host "Checking Redis..."
$ping = wsl redis-cli -h 172.27.247.142 ping 2>$null
if ($ping -match "PONG") {
    Write-Host "Redis is running" -ForegroundColor Green
} else {
    Write-Host "Starting Redis..." -ForegroundColor Yellow
    wsl redis-cli shutdown 2>$null
    Start-Sleep -Seconds 1
    wsl redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes
    Start-Sleep -Seconds 2
    Write-Host "Redis started" -ForegroundColor Green
}

Write-Host "Starting Django server at http://127.0.0.1:8000"
python -m daphne -b 127.0.0.1 -p 8000 interview_platform.asgi:application
