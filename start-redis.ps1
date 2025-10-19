# Redis Startup Script for WSL
# This script checks if Redis is running and starts it if needed

Write-Host "Checking Redis status..." -ForegroundColor Cyan

# Check if Redis is already running and accessible
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
    Write-Host "✓ Redis is already running and accessible!" -ForegroundColor Green
} else {
    Write-Host "Starting Redis server..." -ForegroundColor Yellow
    
    # Stop any existing Redis instances
    wsl redis-cli shutdown 2>$null
    Start-Sleep -Seconds 1
    
    # Start Redis with proper binding
    wsl redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes
    Start-Sleep -Seconds 2
    
    # Verify it's running
    try {
        $pingResult = wsl redis-cli -h 172.27.247.142 ping 2>$null
        if ($pingResult -match "PONG") {
            Write-Host "✓ Redis started successfully and is accessible!" -ForegroundColor Green
            Write-Host "  Address: 172.27.247.142:6379" -ForegroundColor Gray
        } else {
            Write-Host "✗ Redis started but not accessible. Check your WSL network configuration." -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ Failed to start Redis. Check WSL installation." -ForegroundColor Red
    }
}
