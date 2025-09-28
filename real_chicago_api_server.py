"""
Real Chicago Data API Server
Fetches and serves actual data from Chicago's official APIs
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import json
import structlog
from datetime import datetime

# Import our services
from app.services.real_chicago_data_service import real_chicago_data_service

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Real Chicago Legal Document Democratization Platform",
    description="AI-powered platform using real Chicago data from official APIs",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    category: Optional[str] = None
    jurisdiction: str = "chicago"

class SearchResponse(BaseModel):
    results: List[Dict]
    total_results: int
    query: str
    jurisdiction: str

class ChatRequest(BaseModel):
    message: str
    jurisdiction: str = "chicago"
    use_context: bool = True

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict]
    confidence_score: float
    jurisdiction: str
    model: str
    context_used: int

class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    document_type: str
    category: str
    jurisdiction: str
    authority: str
    url: str
    effective_date: str
    source: str

class IngestionRequest(BaseModel):
    limit_per_source: int = 10
    sources: Optional[List[str]] = None

# Global document store
documents = {}
conversation_history = []

def simple_similarity_search(query: str, top_k: int = 5) -> List[Dict]:
    """Simple keyword-based similarity search"""
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    scored_docs = []
    
    for doc_id, doc in documents.items():
        content_lower = doc["content"].lower()
        title_lower = doc["title"].lower()
        
        # Calculate simple similarity score
        content_words = set(content_lower.split())
        title_words = set(title_lower.split())
        
        # Count word matches
        content_matches = len(query_words.intersection(content_words))
        title_matches = len(query_words.intersection(title_words))
        
        # Weight title matches more heavily
        similarity_score = (content_matches * 0.7 + title_matches * 1.5) / len(query_words)
        
        if similarity_score > 0:
            doc_copy = doc.copy()
            doc_copy["similarity_score"] = min(similarity_score, 1.0)
            scored_docs.append(doc_copy)
    
    # Sort by similarity score
    scored_docs.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_docs[:top_k]

def classify_document_simple(text: str) -> str:
    """Simple keyword-based document classification"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["building", "construction", "permit", "contractor", "violation"]):
        return "construction"
    elif any(word in text_lower for word in ["business", "license", "company", "enterprise"]):
        return "business"
    elif any(word in text_lower for word in ["council", "meeting", "governance", "city"]):
        return "governance"
    elif any(word in text_lower for word in ["food", "inspection", "restaurant", "health"]):
        return "healthcare"
    else:
        return "general"

def generate_simple_answer(question: str, relevant_docs: List[Dict]) -> str:
    """Generate a simple answer based on relevant documents"""
    if not relevant_docs:
        return f"I don't have specific Chicago legal documents to answer your question about '{question}'. Please try rephrasing your question or search for more specific terms."
    
    top_doc = relevant_docs[0]
    content = top_doc["content"]
    title = top_doc["title"]
    authority = top_doc["authority"]
    
    question_lower = question.lower()
    
    # Generate contextual responses
    if any(word in question_lower for word in ["how", "process", "procedure", "steps"]):
        return f"Based on the real Chicago document '{title}' from the {authority}: {content[:200]}... To proceed, you should contact the {authority} directly or visit their website for the complete process and requirements."
    
    elif any(word in question_lower for word in ["what", "requirements", "need", "required"]):
        return f"According to the real Chicago data '{title}' from the {authority}: {content[:200]}... This document outlines the specific requirements and regulations for {top_doc['category']} in Chicago."
    
    elif any(word in question_lower for word in ["when", "time", "deadline", "schedule"]):
        return f"Based on the real Chicago data '{title}' from the {authority}: {content[:200]}... The document specifies timing requirements and deadlines for {top_doc['category']} in Chicago."
    
    elif any(word in question_lower for word in ["where", "location", "office", "contact"]):
        return f"According to the real Chicago data '{title}' from the {authority}: {content[:200]}... For more information about locations and contact details, you should visit the {authority} website or contact them directly."
    
    elif any(word in question_lower for word in ["cost", "fee", "price", "charge"]):
        return f"Based on the real Chicago data '{title}' from the {authority}: {content[:200]}... This document contains information about fees and costs associated with {top_doc['category']} in Chicago."
    
    else:
        return f"Based on the real Chicago data '{title}' from the {authority}: {content[:200]}... This information relates to {top_doc['category']} and may help answer your question about Chicago legal matters."

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    await real_chicago_data_service.initialize()
    logger.info("Real Chicago Legal Document Democratization Platform started")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Real Chicago Legal Document Democratization Platform API",
        "version": "2.0.0",
        "jurisdiction": "chicago",
        "data_source": "real_chicago_apis",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "jurisdiction": "chicago",
        "data_source": "real_chicago_apis",
        "services": {
            "api": "running",
            "real_chicago_data_service": "ready",
            "search_service": "ready",
            "chat_service": "ready"
        }
    }

@app.post("/api/v1/ingest/real-chicago")
async def trigger_real_chicago_ingestion(request: IngestionRequest):
    """Trigger real Chicago document ingestion from city APIs"""
    try:
        # Fetch real Chicago data
        real_documents = await real_chicago_data_service.fetch_all_real_chicago_data(
            limit_per_source=request.limit_per_source
        )
        
        # Store in global document store
        global documents
        for doc in real_documents:
            documents[doc["document_id"]] = doc
        
        return {
            "message": f"Real Chicago document ingestion completed successfully. Loaded {len(real_documents)} documents.",
            "jurisdiction": "chicago",
            "data_source": "real_chicago_apis",
            "documents_loaded": len(real_documents),
            "limit_per_source": request.limit_per_source
        }
        
    except Exception as e:
        logger.error("Real Chicago document ingestion failed", error=str(e))
        raise HTTPException(status_code=500, detail="Real Chicago document ingestion failed")

@app.post("/api/v1/search/semantic", response_model=SearchResponse)
async def semantic_search(request: SearchRequest):
    """Perform semantic search for real Chicago legal documents"""
    try:
        results = simple_similarity_search(request.query, request.top_k)
        
        # Filter by category if specified
        if request.category:
            results = [r for r in results if r.get("category") == request.category]
        
        # Add classification to results
        for result in results:
            result["category"] = classify_document_simple(result["content"])
            result["jurisdiction"] = "chicago"
        
        return SearchResponse(
            results=results,
            total_results=len(results),
            query=request.query,
            jurisdiction="chicago"
        )
        
    except Exception as e:
        logger.error("Semantic search failed", error=str(e))
        raise HTTPException(status_code=500, detail="Search failed")

@app.post("/api/v1/chat/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """Ask questions about real Chicago legal documents"""
    try:
        # Get relevant documents for context if requested
        relevant_docs = []
        if request.use_context:
            relevant_docs = simple_similarity_search(request.message, top_k=3)
        
        # Generate answer based on relevant documents
        answer = generate_simple_answer(request.message, relevant_docs)
        
        # Calculate confidence score
        confidence_score = 0.8 if relevant_docs else 0.3
        if relevant_docs:
            confidence_score = min(relevant_docs[0]["similarity_score"] + 0.2, 1.0)
        
        # Extract sources
        sources = []
        if relevant_docs:
            for doc in relevant_docs[:3]:
                sources.append({
                    "title": doc["title"],
                    "authority": doc["authority"],
                    "url": doc["url"],
                    "category": doc["category"],
                    "similarity_score": doc["similarity_score"]
                })
        
        # Store conversation history
        conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": request.message,
            "ai_response": answer,
            "sources": sources,
            "jurisdiction": request.jurisdiction
        })
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence_score=confidence_score,
            jurisdiction="chicago",
            model="real-chicago-data-based",
            context_used=len(relevant_docs)
        )
        
    except Exception as e:
        logger.error("Chat request failed", error=str(e))
        raise HTTPException(status_code=500, detail="Chat request failed")

@app.get("/api/v1/documents/", response_model=List[DocumentResponse])
async def get_documents():
    """Get all available real Chicago documents"""
    try:
        document_list = []
        for doc_id, doc_data in documents.items():
            document_list.append(DocumentResponse(
                id=doc_data["document_id"],
                title=doc_data["title"],
                content=doc_data["content"],
                document_type=doc_data["document_type"],
                category=doc_data["category"],
                jurisdiction="chicago",
                authority=doc_data["authority"],
                url=doc_data["url"],
                effective_date=doc_data["effective_date"],
                source=doc_data["source"]
            ))
        
        return document_list
        
    except Exception as e:
        logger.error("Failed to get documents", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve documents")

@app.get("/api/v1/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Get a specific real Chicago document by ID"""
    try:
        if document_id not in documents:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc_data = documents[document_id]
        
        return DocumentResponse(
            id=doc_data["document_id"],
            title=doc_data["title"],
            content=doc_data["content"],
            document_type=doc_data["document_type"],
            category=doc_data["category"],
            jurisdiction="chicago",
            authority=doc_data["authority"],
            url=doc_data["url"],
            effective_date=doc_data["effective_date"],
            source=doc_data["source"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get document {document_id}", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve document")

@app.get("/api/v1/documents/stats/overview")
async def get_document_stats():
    """Get real Chicago document statistics"""
    try:
        total_docs = len(documents)
        
        # Count by category
        categories = {}
        sources = set()
        authorities = set()
        
        for doc_data in documents.values():
            category = doc_data["category"]
            categories[category] = categories.get(category, 0) + 1
            sources.add(doc_data["source"])
            authorities.add(doc_data["authority"])
        
        return {
            "jurisdiction": "chicago",
            "data_source": "real_chicago_apis",
            "total_documents": total_docs,
            "categories": categories,
            "sources": list(sources),
            "authorities": list(authorities)
        }
        
    except Exception as e:
        logger.error("Failed to get document stats", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get document statistics")

@app.get("/api/v1/chat/history")
async def get_chat_history(limit: int = 10):
    """Get recent chat conversation history"""
    try:
        recent_history = conversation_history[-limit:] if conversation_history else []
        return {
            "conversation_history": recent_history,
            "total_messages": len(recent_history)
        }
    except Exception as e:
        logger.error("Failed to get chat history", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get chat history")

@app.post("/api/v1/chat/clear")
async def clear_chat_history():
    """Clear chat conversation history"""
    try:
        global conversation_history
        conversation_history = []
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        logger.error("Failed to clear chat history", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to clear chat history")

@app.get("/api/v1/search/suggestions")
async def get_search_suggestions():
    """Get suggested search queries for real Chicago data"""
    return {
        "jurisdiction": "chicago",
        "data_source": "real_chicago_apis",
        "suggestions": [
            "How do I get a building permit in Chicago?",
            "What are the business license requirements?",
            "What happened at the last city council meeting?",
            "What are the food inspection requirements?",
            "How much does a business license cost?",
            "What are the building violation penalties?",
            "Where can I find food inspection results?",
            "How do I contact the Department of Buildings?"
        ]
    }

@app.get("/api/v1/data-sources")
async def get_data_sources():
    """Get information about real Chicago data sources"""
    return {
        "jurisdiction": "chicago",
        "data_sources": {
            "building_permits": "https://data.cityofchicago.org/resource/ydr8-5enu.json",
            "business_licenses": "https://data.cityofchicago.org/resource/uupf-x98q.json",
            "city_council_meetings": "https://data.cityofchicago.org/resource/7c8c-9w7x.json",
            "food_inspections": "https://data.cityofchicago.org/resource/4ijn-s7e5.json",
            "building_violations": "https://data.cityofchicago.org/resource/22u3-xenr.json"
        },
        "description": "Real-time data from Chicago's official open data portal"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Real Chicago Legal Document Democratization Platform API...")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("Data Source: Real Chicago APIs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
