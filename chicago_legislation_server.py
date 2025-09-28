"""
Chicago Legislation API Server

A FastAPI server that provides access to real Chicago legislation, ordinances, 
resolutions, and policies from the official Chicago City Clerk API.
"""

import asyncio
import structlog
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, status, Query, Path as FastAPIPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.services.chicago_legislation_service import chicago_legislation_service

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

# Create FastAPI app
app = FastAPI(
    title="Chicago Legislation Democratization Platform",
    description="Real-time access to Chicago legislation, ordinances, resolutions, and policies",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Mount static files for the React frontend
frontend_path = Path(__file__).parent / "project" / "dist"
if frontend_path.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_path / "assets")), name="assets")

# Serve the React frontend
@app.get("/")
async def serve_frontend():
    """Serve the React frontend"""
    frontend_file = frontend_path / "index.html"
    logger.info(f"Frontend path: {frontend_path}")
    logger.info(f"Frontend file exists: {frontend_file.exists()}")
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    else:
        return JSONResponse(
            status_code=404,
            content={"error": f"Frontend not built. Path: {frontend_path}, File: {frontend_file}"}
        )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Chicago Legislation Democratization Platform...")
    await chicago_legislation_service.initialize()
    logger.info("Chicago Legislation Service initialized successfully")
    logger.info("API Documentation: http://localhost:8000/api/docs")
    logger.info("Health Check: http://localhost:8000/health")
    logger.info("Frontend: http://localhost:8000/")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Chicago Legislation Democratization Platform...")
    await chicago_legislation_service.close()
    logger.info("Application shutdown complete")

# Health check endpoint
@app.get("/health", 
         summary="Health Check",
         description="Check the health status of the Chicago Legislation API",
         tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Chicago Legislation Democratization Platform",
        "version": "1.0.0",
        "data_source": "Chicago City Clerk API",
        "total_documents": len(chicago_legislation_service.documents)
    }

# Data sources endpoint
@app.get("/api/v1/data-sources",
         summary="Get Data Sources",
         description="Get information about available data sources",
         tags=["System"])
async def get_data_sources():
    """Get available data sources"""
    return {
        "sources": [
            {
                "name": "Chicago City Clerk API",
                "url": "https://api.chicityclerkelms.chicago.gov",
                "description": "Official Chicago legislation, ordinances, resolutions, and policies",
                "status": "active",
                "total_documents": len(chicago_legislation_service.documents)
            }
        ],
        "last_updated": datetime.now().isoformat()
    }

# Legislation ingestion endpoint
@app.post("/api/v1/ingest/legislation",
          summary="Ingest Chicago Legislation",
          description="Fetch and ingest real Chicago legislation from the City Clerk API",
          tags=["Data Ingestion"])
async def ingest_legislation(
    request_data: Optional[Dict[str, Any]] = None
):
    """Ingest Chicago legislation data"""
    try:
        limits = None
        force_refresh = False
        
        if request_data:
            limits = request_data.get("limits")
            force_refresh = request_data.get("force_refresh", False)
        
        if limits is None:
            limits = {
                "recent": 100,
                "ordinances": 50,
                "resolutions": 50,
                "executive_orders": 25,
                "zoning": 25,
                "business": 25,
                "transportation": 25
            }
        
        logger.info("Starting Chicago legislation ingestion", limits=limits)
        ingestion_summary = await chicago_legislation_service.ingest_comprehensive_legislation(limits)
        
        return {
            "status": "success",
            "message": "Chicago legislation ingestion completed successfully",
            "timestamp": datetime.now().isoformat(),
            **ingestion_summary
        }
    except Exception as e:
        logger.error("Failed to ingest Chicago legislation", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest Chicago legislation: {str(e)}"
        )

# Document statistics endpoint
@app.get("/api/v1/documents/stats/legislation",
         summary="Get Legislation Statistics",
         description="Get comprehensive statistics about ingested Chicago legislation",
         tags=["Documents"])
async def get_legislation_stats():
    """Get legislation statistics"""
    try:
        stats = chicago_legislation_service.get_legislation_stats()
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            **stats
        }
    except Exception as e:
        logger.error("Failed to get legislation statistics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get legislation statistics: {str(e)}"
        )

# Get all documents endpoint
@app.get("/api/v1/documents/",
         summary="Get All Documents",
         description="Retrieve all ingested Chicago legislation documents",
         tags=["Documents"])
async def get_all_documents(
    limit: int = Query(100, description="Maximum number of documents to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    document_type: Optional[str] = Query(None, description="Filter by document type")
):
    """Get all documents with optional filtering"""
    try:
        documents = chicago_legislation_service.get_all_documents(limit)
        
        # Apply filters
        if category:
            documents = [doc for doc in documents if doc.get("category") == category]
        
        if document_type:
            documents = [doc for doc in documents if doc.get("document_type") == document_type]
        
        return {
            "status": "success",
            "total_documents": len(documents),
            "documents": documents,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error("Failed to get documents", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get documents: {str(e)}"
        )

# Get document by ID endpoint
@app.get("/api/v1/documents/{document_id}",
         summary="Get Document by ID",
         description="Retrieve a specific Chicago legislation document by its ID",
         tags=["Documents"])
async def get_document_by_id(document_id: str):
    """Get a specific document by ID"""
    document = chicago_legislation_service.documents.get(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{document_id}' not found"
        )
    
    return {
        "status": "success",
        "document": document,
        "timestamp": datetime.now().isoformat()
    }

# Advanced semantic search endpoint
@app.post("/api/v1/search/semantic",
          summary="Advanced Semantic Search",
          description="Perform advanced semantic search through Chicago legislation",
          tags=["Search"])
async def advanced_semantic_search(
    request_data: Dict[str, Any]
):
    """Perform advanced semantic search"""
    try:
        query = request_data.get("query", "")
        jurisdiction = request_data.get("jurisdiction", "chicago")
        category = request_data.get("category")
        limit = request_data.get("limit", 10)
        
        if not query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search query cannot be empty"
            )
        
        results = chicago_legislation_service.advanced_semantic_search(
            query, jurisdiction, category, limit
        )
        
        return {
            "query": query,
            "jurisdiction": jurisdiction,
            "category_filter": category,
            "total_results": len(results),
            "results": results,
            "search_metadata": {
                "search_timestamp": datetime.now().isoformat(),
                "total_documents_searched": len(chicago_legislation_service.documents),
                "search_algorithm": "keyword_and_metadata_matching"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to perform semantic search", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Semantic search failed: {str(e)}"
        )

# AI chat endpoint
@app.post("/api/v1/chat/ask",
          summary="AI Chat with Legislation Context",
          description="Ask questions about Chicago legislation with AI-powered responses",
          tags=["Chat"])
async def ask_legislation_chat_agent(
    request_data: Dict[str, Any]
):
    """Ask the AI chat agent with legislation context"""
    try:
        user_message = request_data.get("user_message", "")
        use_context = request_data.get("use_context", True)
        max_context_docs = request_data.get("max_context_docs", 5)
        
        if not user_message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User message cannot be empty"
            )
        
        # Perform semantic search to get relevant documents
        recommended_documents = []
        if use_context:
            recommended_documents = chicago_legislation_service.advanced_semantic_search(
                user_message, jurisdiction="chicago", limit=max_context_docs
            )
        
        # Generate response using the legislation chat service
        response = chicago_legislation_service.generate_legislation_chat_response(
            user_message, recommended_documents
        )
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to generate chat response", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chat response: {str(e)}"
        )

# Analytics endpoint
@app.get("/api/v1/analytics",
         summary="Get System Analytics",
         description="Get comprehensive analytics about the Chicago legislation system",
         tags=["Analytics"])
async def get_analytics():
    """Get system analytics"""
    try:
        analytics = chicago_legislation_service.get_analytics()
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            **analytics
        }
    except Exception as e:
        logger.error("Failed to get analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics: {str(e)}"
        )

# Chat history endpoint
@app.get("/api/v1/chat/history",
         summary="Get Chat History",
         description="Retrieve chat conversation history",
         tags=["Chat"])
async def get_chat_history(
    limit: int = Query(20, description="Maximum number of chat messages to return")
):
    """Get chat history"""
    try:
        history = chicago_legislation_service.get_chat_history(limit)
        return {
            "status": "success",
            "total_messages": len(history),
            "chat_history": history,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error("Failed to get chat history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat history: {str(e)}"
        )

# Clear chat history endpoint
@app.post("/api/v1/chat/clear",
          summary="Clear Chat History",
          description="Clear the chat conversation history",
          tags=["Chat"])
async def clear_chat_history():
    """Clear chat history"""
    try:
        chicago_legislation_service.clear_chat_history()
        return {
            "status": "success",
            "message": "Chat history cleared successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error("Failed to clear chat history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear chat history: {str(e)}"
        )

# Search suggestions endpoint
@app.get("/api/v1/search/suggestions",
         summary="Get Search Suggestions",
         description="Get suggested search queries for Chicago legislation",
         tags=["Search"])
async def get_search_suggestions(
    jurisdiction: Optional[str] = Query("chicago", description="Jurisdiction for suggestions")
):
    """Get search suggestions"""
    try:
        suggestions = chicago_legislation_service.get_search_suggestions(jurisdiction)
        return {
            "status": "success",
            "jurisdiction": jurisdiction,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error("Failed to get search suggestions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get search suggestions: {str(e)}"
        )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "detail": str(exc)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error("Internal server error", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "chicago_legislation_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
