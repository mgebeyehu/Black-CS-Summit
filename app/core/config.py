"""
Configuration settings for the Legal Document Democratization Platform
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Legal Document Democratization Platform"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/legal_docs_db"
    
    # Vector Database (Chroma)
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "legal_documents"
    
    # Graph Database (Neo4j)
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    
    # Redis (for caching and background tasks)
    REDIS_URL: str = "redis://localhost:6379"
    
    # ML Models
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CLASSIFICATION_MODEL: str = "microsoft/DialoGPT-medium"
    
    # Data Sources
    DATA_GOV_API_KEY: Optional[str] = None
    CONGRESS_GOV_API_KEY: Optional[str] = None
    CHICAGO_API_APP_TOKEN: str = "YOUR_CHICAGO_API_APP_TOKEN"  # Optional, but good practice
    
    # AI Services
    GEMINI_API_KEY: Optional[str] = None
    
    # Document Processing
    MAX_DOCUMENT_SIZE: int = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FILE_TYPES: List[str] = [".pdf", ".docx", ".txt", ".html"]
    
    # Real-time Updates
    ENABLE_REAL_TIME_UPDATES: bool = True
    UPDATE_CHECK_INTERVAL: int = 3600  # 1 hour in seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
