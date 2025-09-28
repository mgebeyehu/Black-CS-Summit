@echo off
REM Chicago Legal Document Democratization Platform
REM Startup Script for Windows

echo 🏛️  Starting Chicago Legal Document Democratization Platform...
echo 📚 Real-time Chicago legislation data integration
echo 🤖 AI-powered legal document search and chat
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.10+ and try again.
    pause
    exit /b 1
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📦 Installing Python dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found. Please ensure you're in the correct directory.
    pause
    exit /b 1
)

REM Set environment variables if .env exists
if exist ".env" (
    echo 🔧 Loading environment variables...
    for /f "delims=" %%i in (.env) do set %%i
)

REM Start the application
echo 🚀 Starting the application...
echo 🌐 Frontend: http://localhost:8000/
echo 📖 API Docs: http://localhost:8000/api/docs
echo ❤️  Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
