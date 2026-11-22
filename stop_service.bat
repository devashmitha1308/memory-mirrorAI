@echo off
echo Stopping MemoryMirror AI background service...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501 ^| findstr LISTENING') do (
    echo Terminating PID: %%a
    taskkill /F /PID %%a
)
echo MemoryMirror AI stopped.
pause
