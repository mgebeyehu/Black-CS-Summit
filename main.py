#!/usr/bin/env python3
"""
Chicago Legal Document Democratization Platform
Main Server Entry Point

A comprehensive platform that democratizes access to Chicago legal documents,
policies, and legislation through intelligent search and AI-powered chat.
"""

import uvicorn
from chicago_legislation_server import app

if __name__ == "__main__":
    print("🏛️  Starting Chicago Legal Document Democratization Platform...")
    print("📚 Real-time Chicago legislation data integration")
    print("🤖 AI-powered legal document search and chat")
    print("🌐 Frontend: http://localhost:8000/")
    print("📖 API Docs: http://localhost:8000/api/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print()
    
    uvicorn.run(
        "chicago_legislation_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
