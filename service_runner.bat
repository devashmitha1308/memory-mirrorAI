@echo off
cd /d "C:\Users\devas\Dropbox\memory mirror AI"

:: Check if port 8501 is already listening
netstat -ano | findstr :8501 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    start "" "C:\Program Files\Python313\pythonw.exe" -m streamlit run app.py --server.port 8501 --server.headless true
)
