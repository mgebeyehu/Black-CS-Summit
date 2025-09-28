"""
Test script for the Real Chicago Data API
Tests the platform with actual data from Chicago's official APIs
"""
import requests
import json
import time

def test_real_chicago_api():
    """Test the real Chicago data API"""
    base_url = "http://localhost:8000"
    
    print("="*80)
    print("REAL CHICAGO DATA LEGAL DOCUMENT DEMOCRATIZATION PLATFORM - API TEST")
    print("="*80)
    
    # Test 1: Health Check
    print("\n1. HEALTH CHECK")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("[SUCCESS] Real Chicago API is healthy!")
            print(f"   Jurisdiction: {health_data.get('jurisdiction', 'unknown')}")
            print(f"   Data Source: {health_data.get('data_source', 'unknown')}")
            print(f"   Services: {', '.join(health_data['services'].keys())}")
        else:
            print("[ERROR] Health check failed")
            return
    except Exception as e:
        print(f"[ERROR] Cannot connect to API: {e}")
        return
    
    # Test 2: Data Sources Information
    print("\n2. REAL CHICAGO DATA SOURCES")
    try:
        response = requests.get(f"{base_url}/api/v1/data-sources")
        if response.status_code == 200:
            sources = response.json()
            print(f"[SUCCESS] Jurisdiction: {sources.get('jurisdiction', 'unknown')}")
            print(f"   Data Source: {sources.get('data_source', 'unknown')}")
            print("   Available APIs:")
            for source_name, url in sources['data_sources'].items():
                print(f"      - {source_name}: {url}")
        else:
            print("[ERROR] Failed to get data sources")
    except Exception as e:
        print(f"[ERROR] Error getting data sources: {e}")
    
    # Test 3: Trigger Real Data Ingestion
    print("\n3. TRIGGER REAL CHICAGO DATA INGESTION")
    try:
        ingestion_data = {"limit_per_source": 5}
        response = requests.post(f"{base_url}/api/v1/ingest/real-chicago", json=ingestion_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] Real Chicago data ingestion completed!")
            print(f"   Jurisdiction: {result.get('jurisdiction', 'unknown')}")
            print(f"   Data Source: {result.get('data_source', 'unknown')}")
            print(f"   Documents Loaded: {result.get('documents_loaded', 0)}")
            print(f"   Limit Per Source: {result.get('limit_per_source', 0)}")
        else:
            print(f"[ERROR] Ingestion failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Error during ingestion: {e}")
    
    # Test 4: Document Statistics
    print("\n4. REAL CHICAGO DOCUMENT STATISTICS")
    try:
        response = requests.get(f"{base_url}/api/v1/documents/stats/overview")
        if response.status_code == 200:
            stats = response.json()
            print(f"[SUCCESS] Jurisdiction: {stats.get('jurisdiction', 'unknown')}")
            print(f"   Data Source: {stats.get('data_source', 'unknown')}")
            print(f"   Total Documents: {stats['total_documents']}")
            print("   Categories:")
            for category, count in stats['categories'].items():
                print(f"      - {category}: {count} documents")
            print(f"   Sources: {', '.join(stats['sources'])}")
            print(f"   Authorities: {', '.join(stats['authorities'])}")
        else:
            print("[ERROR] Failed to get document stats")
    except Exception as e:
        print(f"[ERROR] Error getting stats: {e}")
    
    # Test 5: Get Sample Documents
    print("\n5. REAL CHICAGO DOCUMENTS SAMPLE")
    try:
        response = requests.get(f"{base_url}/api/v1/documents/")
        if response.status_code == 200:
            documents = response.json()
            print(f"[SUCCESS] Found {len(documents)} real Chicago documents:")
            for i, doc in enumerate(documents[:3], 1):  # Show first 3
                print(f"   {i}. {doc['title']}")
                print(f"      Category: {doc['category']}")
                print(f"      Authority: {doc['authority']}")
                print(f"      Type: {doc['document_type']}")
                print(f"      Source: {doc['source']}")
                print(f"      Date: {doc['effective_date']}")
                print()
        else:
            print("[ERROR] Failed to get documents")
    except Exception as e:
        print(f"[ERROR] Error getting documents: {e}")
    
    # Test 6: Real Data Semantic Search
    print("\n6. REAL CHICAGO DATA SEMANTIC SEARCH")
    search_queries = [
        "Chicago building permits",
        "business license requirements",
        "city council meetings",
        "food inspection violations",
        "building violations"
    ]
    
    for query in search_queries:
        print(f"\nSearch Query: '{query}'")
        try:
            search_data = {"query": query, "top_k": 3, "jurisdiction": "chicago"}
            response = requests.post(f"{base_url}/api/v1/search/semantic", json=search_data)
            
            if response.status_code == 200:
                results = response.json()
                print(f"   Jurisdiction: {results.get('jurisdiction', 'unknown')}")
                print(f"   Found {results['total_results']} results:")
                
                for i, result in enumerate(results['results'], 1):
                    print(f"   {i}. {result['title']}")
                    print(f"      Similarity: {result['similarity_score']:.3f}")
                    print(f"      Category: {result['category']}")
                    print(f"      Authority: {result['authority']}")
                    print(f"      Source: {result.get('source', 'unknown')}")
            else:
                print("   [ERROR] Search failed")
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
    
    # Test 7: Real Data AI Chat
    print("\n7. REAL CHICAGO DATA AI CHAT")
    chat_questions = [
        "How do I get a building permit in Chicago?",
        "What are the business license requirements for a restaurant?",
        "What are the food inspection requirements?",
        "How much does it cost to get a business license?",
        "What are the building violation penalties?"
    ]
    
    for i, question in enumerate(chat_questions, 1):
        print(f"\n{i}. Question: {question}")
        try:
            chat_data = {"message": question, "jurisdiction": "chicago", "use_context": True}
            response = requests.post(f"{base_url}/api/v1/chat/ask", json=chat_data)
            
            if response.status_code == 200:
                chat_response = response.json()
                print(f"   AI Model: {chat_response.get('model', 'unknown')}")
                print(f"   Answer: {chat_response['answer'][:200]}...")
                print(f"   Confidence: {chat_response['confidence_score']:.3f}")
                print(f"   Context Used: {chat_response['context_used']} documents")
                print(f"   Jurisdiction: {chat_response.get('jurisdiction', 'unknown')}")
                
                if chat_response['sources']:
                    print("   Sources:")
                    for source in chat_response['sources'][:2]:
                        print(f"      - {source['title']} ({source['authority']})")
            else:
                print("   [ERROR] Chat failed")
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
    
    # Test 8: Chat History
    print("\n8. CHAT CONVERSATION HISTORY")
    try:
        response = requests.get(f"{base_url}/api/v1/chat/history?limit=3")
        if response.status_code == 200:
            history = response.json()
            print(f"[SUCCESS] Found {history['total_messages']} recent messages")
            for msg in history['conversation_history']:
                print(f"   User: {msg['user_message'][:50]}...")
                print(f"   AI: {msg['ai_response'][:50]}...")
                print(f"   Time: {msg['timestamp']}")
                print()
        else:
            print("[ERROR] Failed to get chat history")
    except Exception as e:
        print(f"[ERROR] Error getting history: {e}")
    
    # Test 9: Search Suggestions
    print("\n9. REAL CHICAGO SEARCH SUGGESTIONS")
    try:
        response = requests.get(f"{base_url}/api/v1/search/suggestions")
        if response.status_code == 200:
            suggestions = response.json()
            print(f"[SUCCESS] Jurisdiction: {suggestions.get('jurisdiction', 'unknown')}")
            print(f"   Data Source: {suggestions.get('data_source', 'unknown')}")
            print("   Suggested questions:")
            for suggestion in suggestions['suggestions']:
                print(f"      - {suggestion}")
        else:
            print("[ERROR] Failed to get suggestions")
    except Exception as e:
        print(f"[ERROR] Error getting suggestions: {e}")
    
    # Test 10: Clear Chat History
    print("\n10. CLEAR CHAT HISTORY")
    try:
        response = requests.post(f"{base_url}/api/v1/chat/clear")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] {result['message']}")
        else:
            print("[ERROR] Failed to clear chat history")
    except Exception as e:
        print(f"[ERROR] Error clearing history: {e}")
    
    print("\n" + "="*80)
    print("REAL CHICAGO DATA API TEST COMPLETE!")
    print("The Real Chicago Legal Document Democratization Platform provides:")
    print("   - Real data from Chicago's official APIs")
    print("   - Building permits, business licenses, city council meetings")
    print("   - Food inspections and building violations")
    print("   - Intelligent search and AI chat")
    print("   - Source attribution to Chicago authorities")
    print("   - Live data from Chicago's open data portal")
    print("="*80)

if __name__ == "__main__":
    print("Testing Real Chicago Legal Document Democratization Platform API...")
    print("Make sure the real Chicago API server is running on http://localhost:8000")
    print()
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    test_real_chicago_api()
