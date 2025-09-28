# API Documentation

## Chicago Legal Document Democratization Platform API

This document provides comprehensive documentation for the Chicago Legal Document Democratization Platform API.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Response Format

All API responses follow a consistent JSON format:

```json
{
  "status": "success|error",
  "timestamp": "2025-09-28T14:30:00.000Z",
  "data": { ... },
  "message": "Optional message"
}
```

## Endpoints

### Health Check

#### GET /health

Check the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-28T14:30:00.000Z",
  "service": "Chicago Legislation Democratization Platform",
  "version": "1.0.0",
  "data_source": "Chicago City Clerk API",
  "total_documents": 600
}
```

### Document Statistics

#### GET /api/v1/documents/stats/legislation

Get comprehensive statistics about the ingested Chicago legislation documents.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-09-28T14:30:00.000Z",
  "jurisdiction": "chicago",
  "data_source": "chicago_city_clerk_api",
  "total_documents": 600,
  "categories": {
    "general": 27,
    "governance": 42,
    "transportation": 25,
    "construction": 6
  },
  "sources": {
    "chicago_city_clerk_api": 600
  },
  "authorities": ["Chicago City Council"],
  "date_range": {
    "earliest": "2025-09-25T15:00:00+00:00",
    "latest": "2025-09-25T15:00:00+00:00"
  },
  "legislation_types": {
    "claim": 20,
    "order": 5,
    "ordinance": 44,
    "executive order": 2,
    "resolution": 27,
    "appointment": 2
  }
}
```

### Document Retrieval

#### GET /api/v1/documents/

Retrieve documents with optional filtering.

**Query Parameters:**
- `limit` (integer, optional): Maximum number of documents to return (default: 100)
- `category` (string, optional): Filter by category (construction, general, transportation, governance)
- `document_type` (string, optional): Filter by document type

**Response:**
```json
{
  "status": "success",
  "total_documents": 5,
  "limit": 5,
  "category_filter": null,
  "documents": [
    {
      "document_id": "368E241C-2D67-F011-BEC1-001DD8096BE6",
      "title": "Zoning Reclassification Map No. 3-I at 1457-1459 N Talman Ave",
      "content": "Zoning Reclassification Map No. 3-I at 1457-1459 N Talman Ave...",
      "document_type": "Ordinance",
      "category": "construction",
      "jurisdiction": "chicago",
      "authority": "Chicago City Council",
      "url": "https://api.chicityclerkelms.chicago.gov/matter/368E241C-2D67-F011-BEC1-001DD8096BE6",
      "effective_date": "2025-09-25T15:00:00+00:00",
      "metadata": {
        "record_number": "CL2025-0018900",
        "file_year": 2025,
        "status": "4-In Committee",
        "sponsor": "Alderman Smith",
        "committee_referral": "Committee on Zoning",
        "last_publication_date": "2025-09-25T15:00:00+00:00"
      }
    }
  ]
}
```

#### GET /api/v1/documents/{document_id}

Retrieve a specific document by its ID.

**Path Parameters:**
- `document_id` (string): The unique identifier of the document

**Response:**
```json
{
  "document_id": "368E241C-2D67-F011-BEC1-001DD8096BE6",
  "title": "Zoning Reclassification Map No. 3-I at 1457-1459 N Talman Ave",
  "content": "Full document content...",
  "document_type": "Ordinance",
  "category": "construction",
  "jurisdiction": "chicago",
  "authority": "Chicago City Council",
  "url": "https://api.chicityclerkelms.chicago.gov/matter/368E241C-2D67-F011-BEC1-001DD8096BE6",
  "effective_date": "2025-09-25T15:00:00+00:00",
  "metadata": { ... }
}
```

### Semantic Search

#### POST /api/v1/search/semantic

Perform advanced semantic search on Chicago legislation documents.

**Request Body:**
```json
{
  "query": "zoning permit construction building",
  "jurisdiction": "chicago",
  "category": "construction",
  "limit": 10
}
```

**Parameters:**
- `query` (string, required): Search query
- `jurisdiction` (string, optional): Filter by jurisdiction (default: "chicago")
- `category` (string, optional): Filter by category
- `limit` (integer, optional): Maximum number of results (default: 10)

**Response:**
```json
{
  "query": "zoning permit construction building",
  "jurisdiction": "chicago",
  "category_filter": "construction",
  "total_results": 5,
  "results": [
    {
      "document_id": "368E241C-2D67-F011-BEC1-001DD8096BE6",
      "title": "Zoning Reclassification Map No. 3-I at 1457-1459 N Talman Ave",
      "content": "Document content...",
      "document_type": "Ordinance",
      "category": "construction",
      "jurisdiction": "chicago",
      "authority": "Chicago City Council",
      "url": "https://api.chicityclerkelms.chicago.gov/matter/368E241C-2D67-F011-BEC1-001DD8096BE6",
      "effective_date": "2025-09-25T15:00:00+00:00",
      "metadata": { ... },
      "relevance_score": 0.95
    }
  ],
  "search_metadata": {
    "search_timestamp": "2025-09-28T14:30:00.000Z",
    "total_documents_searched": 600,
    "search_algorithm": "keyword_and_metadata_matching"
  }
}
```

### AI Chat

#### POST /api/v1/chat/ask

Ask the AI chat agent questions about Chicago legislation.

**Request Body:**
```json
{
  "user_message": "How do I get a zoning permit in Chicago?",
  "use_context": true,
  "max_context_docs": 3
}
```

**Parameters:**
- `user_message` (string, required): The user's question
- `use_context` (boolean, optional): Whether to use document context (default: true)
- `max_context_docs` (integer, optional): Maximum context documents (default: 3)

**Response:**
```json
{
  "answer": "To get a zoning permit in Chicago, you need to...",
  "sources": [
    {
      "document_id": "368E241C-2D67-F011-BEC1-001DD8096BE6",
      "title": "Zoning Reclassification Map No. 3-I at 1457-1459 N Talman Ave",
      "url": "https://api.chicityclerkelms.chicago.gov/matter/368E241C-2D67-F011-BEC1-001DD8096BE6",
      "relevance_score": 0.95
    }
  ],
  "confidence_score": 0.87,
  "jurisdiction": "chicago",
  "model": "keyword_based_chat",
  "context_used": 3,
  "total_documents_searched": 600,
  "search_metadata": {
    "query_processed": "zoning permit chicago",
    "documents_found": 5,
    "search_timestamp": "2025-09-28T14:30:00.000Z"
  }
}
```

### Chat History

#### GET /api/v1/chat/history

Retrieve chat history.

**Query Parameters:**
- `limit` (integer, optional): Maximum number of messages (default: 5)

**Response:**
```json
{
  "chat_history": [
    {
      "role": "user",
      "message": "How do I get a zoning permit?",
      "timestamp": "2025-09-28T14:30:00.000Z"
    },
    {
      "role": "assistant",
      "message": "To get a zoning permit in Chicago...",
      "timestamp": "2025-09-28T14:30:01.000Z"
    }
  ],
  "total_messages": 2
}
```

#### POST /api/v1/chat/clear

Clear the chat history.

**Response:**
```json
{
  "status": "success",
  "message": "Chat history cleared successfully"
}
```

### Search Suggestions

#### GET /api/v1/search/suggestions

Get popular search suggestions.

**Response:**
```json
{
  "suggestions": [
    "How do I get a zoning permit in Chicago?",
    "What are the business license requirements?",
    "How do I apply for handicapped parking?",
    "What are the current zoning regulations?",
    "How do I get a sign permit?"
  ],
  "jurisdiction": "chicago"
}
```

### Data Ingestion

#### POST /api/v1/ingest/legislation

Trigger ingestion of Chicago legislation data.

**Request Body:**
```json
{
  "limits": {
    "recent": 100,
    "ordinances": 50,
    "resolutions": 50,
    "zoning": 25,
    "business": 25
  },
  "force_refresh": false
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Chicago legislation ingestion completed successfully",
  "timestamp": "2025-09-28T14:30:00.000Z",
  "jurisdiction": "chicago",
  "data_source": "chicago_city_clerk_api",
  "documents_loaded": 600,
  "limits": {
    "recent": 100,
    "ordinances": 50,
    "resolutions": 50,
    "zoning": 25,
    "business": 25
  },
  "categories": {
    "general": 27,
    "governance": 42,
    "transportation": 25,
    "construction": 6
  },
  "sources": {
    "chicago_city_clerk_api": 600
  }
}
```

### System Analytics

#### GET /api/v1/analytics

Get system-wide analytics and metrics.

**Response:**
```json
{
  "total_documents": 600,
  "total_chat_sessions": 15,
  "category_breakdown": {
    "general": 27,
    "governance": 42,
    "transportation": 25,
    "construction": 6
  },
  "source_breakdown": {
    "chicago_city_clerk_api": 600
  },
  "legislation_types": {
    "claim": 20,
    "order": 5,
    "ordinance": 44,
    "executive order": 2,
    "resolution": 27,
    "appointment": 2
  },
  "date_range": {
    "earliest": "2025-09-25T15:00:00+00:00",
    "latest": "2025-09-25T15:00:00+00:00"
  },
  "system_health": {
    "data_freshness": "current",
    "api_status": "healthy",
    "search_performance": "optimal"
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Document with ID 'invalid-id' not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "query"],
      "msg": "Input should be a valid string",
      "input": null
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error occurred"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. However, we recommend:
- No more than 100 requests per minute per IP
- Reasonable delays between bulk operations
- Respectful usage of the API

## Data Sources

The API integrates with the following data sources:
- **Chicago City Clerk API**: Official legislation and policy data
- **Real-time Updates**: Live synchronization with Chicago's legislative system

## Support

For API support and questions:
- **Documentation**: Check this documentation first
- **Issues**: Report issues on GitHub
- **Contact**: [Your contact information]

---

**Last Updated**: September 28, 2025
