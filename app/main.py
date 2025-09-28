"""
Main FastAPI application for Legal Document Democratization Platform
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import init_db
from app.core.vector_db import init_vector_db
from app.core.graph_db import init_graph_db
from app.services.ml_service import ml_service
from app.services.vector_service import vector_service
from app.services.graph_service import graph_service
from app.services.data_ingestion_service import data_ingestion_service

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(
    title="Legal Document Democratization Platform",
    description="AI-powered platform for finding and understanding legal documents and policies",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize databases and services on startup"""
    logger.info("Starting Legal Document Democratization Platform")
    
    try:
        # Initialize databases
        await init_db()
        await init_vector_db()
        await init_graph_db()
        
        # Initialize ML services
        await ml_service.initialize()
        await vector_service.initialize()
        await graph_service.initialize()
        await data_ingestion_service.initialize()
        
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Legal Document Democratization Platform")
    await data_ingestion_service.close()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Legal Document Democratization Platform API",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "database": "connected",
            "vector_db": "connected",
            "graph_db": "connected"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )