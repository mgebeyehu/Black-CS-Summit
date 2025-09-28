#!/usr/bin/env python3
"""
Basic API Tests for Chicago Legal Document Democratization Platform
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_document_stats():
    """Test document statistics endpoint"""
    print("Testing document stats...")
    try:
        response = requests.get("http://localhost:8000/api/v1/documents/stats/legislation")
        assert response.status_code == 200
        data = response.json()
        assert "total_documents" in data
        print(f"✅ Document stats: {data['total_documents']} documents")
        return True
    except Exception as e:
        print(f"❌ Document stats failed: {e}")
        return False

def test_search_endpoint():
    """Test semantic search endpoint"""
    print("Testing search endpoint...")
    try:
        payload = {
            "query": "zoning permit",
            "jurisdiction": "chicago",
            "limit": 3
        }
        response = requests.post("http://localhost:8000/api/v1/search/semantic", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        print(f"✅ Search returned {data['total_results']} results")
        return True
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

def test_chat_endpoint():
    """Test AI chat endpoint"""
    print("Testing chat endpoint...")
    try:
        payload = {
            "user_message": "What is a zoning permit?",
            "use_context": True,
            "max_context_docs": 2
        }
        response = requests.post("http://localhost:8000/api/v1/chat/ask", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        print("✅ Chat endpoint working")
        return True
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running API Tests for Chicago Legal Document Platform")
    print("=" * 60)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        test_health_endpoint,
        test_document_stats,
        test_search_endpoint,
        test_chat_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Platform is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the server logs.")
        return 1

if __name__ == "__main__":
    exit(main())
