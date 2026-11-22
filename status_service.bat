@echo off
echo Checking MemoryMirror AI Service Status...
netstat -ano | findstr :8501 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    echo [STATUS] ONLINE - MemoryMirror AI is running on http://localhost:8501
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501 ^| findstr LISTENING') do (
        echo [INFO] Process ID: %%a
    )
) else (
    echo [STATUS] OFFLINE - MemoryMirror AI is not currently listening on port 8501.
)
pause
