#!/bin/bash

# Chicago Legal Document Democratization Platform
# Startup Script for Production Deployment

echo "🏛️  Starting Chicago Legal Document Democratization Platform..."
echo "📚 Real-time Chicago legislation data integration"
echo "🤖 AI-powered legal document search and chat"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found. Please ensure you're in the correct directory."
    exit 1
fi

# Set environment variables if .env exists
if [ -f ".env" ]; then
    echo "🔧 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start the application
echo "🚀 Starting the application..."
echo "🌐 Frontend: http://localhost:8000/"
echo "📖 API Docs: http://localhost:8000/api/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
