"""
Chicago City Clerk Legislation API Service

This service fetches real Chicago legislation, ordinances, resolutions, and policies
from the official Chicago City Clerk API.
"""

import asyncio
import aiohttp
import requests
from typing import List, Dict, Optional, Any
import structlog
from datetime import datetime, timedelta
import json
import re
import hashlib

logger = structlog.get_logger()

class ChicagoLegislationService:
    def __init__(self):
        self.session = None
        self.documents = {}
        self.chat_history = []
        self.search_history = []
        
        # Chicago City Clerk API endpoints
        self.base_url = "https://api.chicityclerkelms.chicago.gov"
        self.endpoints = {
            "matters": f"{self.base_url}/matter",
            "search": f"{self.base_url}/search",
            "bodies": f"{self.base_url}/body",
            "persons": f"{self.base_url}/person",
            "meetings": f"{self.base_url}/meeting"
        }

    async def initialize(self):
        """Initialize the Chicago legislation service"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                "User-Agent": "Chicago Legal Document Platform/1.0",
                "Accept": "application/json"
            }
        )
        logger.info("Chicago Legislation Service initialized")

    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()

    async def fetch_recent_legislation(self, limit: int = 100) -> List[Dict]:
        """Fetch recent Chicago legislation and policies"""
        logger.info(f"Fetching {limit} recent Chicago legislation items...")
        
        try:
            async with self.session.get(
                self.endpoints["matters"],
                params={
                    "limit": limit,
                    "order": "introductionDate DESC"
                }
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                matters = data.get("data", [])
                logger.info(f"Fetched {len(matters)} legislation items from Chicago API")
                
                documents = []
                for matter in matters:
                    doc = self._process_legislation_item(matter)
                    if doc:
                        documents.append(doc)
                
                return documents
                
        except aiohttp.ClientError as e:
            logger.error(f"Failed to fetch Chicago legislation", error=str(e))
            return []

    async def fetch_legislation_by_category(self, category: str, limit: int = 50) -> List[Dict]:
        """Fetch legislation by specific category"""
        logger.info(f"Fetching {limit} {category} legislation items...")
        
        try:
            async with self.session.get(
                self.endpoints["matters"],
                params={
                    "limit": limit,
                    "matterCategory": category,
                    "order": "introductionDate DESC"
                }
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                matters = data.get("data", [])
                logger.info(f"Fetched {len(matters)} {category} items")
                
                documents = []
                for matter in matters:
                    doc = self._process_legislation_item(matter)
                    if doc:
                        documents.append(doc)
                
                return documents
                
        except aiohttp.ClientError as e:
            logger.error(f"Failed to fetch {category} legislation", error=str(e))
            return []

    async def search_legislation(self, query: str, limit: int = 50) -> List[Dict]:
        """Search Chicago legislation by text"""
        logger.info(f"Searching Chicago legislation for: {query}")
        
        try:
            async with self.session.get(
                self.endpoints["search"],
                params={
                    "q": query,
                    "limit": limit
                }
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                matters = data.get("data", [])
                logger.info(f"Found {len(matters)} results for: {query}")
                
                documents = []
                for matter in matters:
                    doc = self._process_legislation_item(matter)
                    if doc:
                        documents.append(doc)
                
                return documents
                
        except aiohttp.ClientError as e:
            logger.error(f"Failed to search Chicago legislation", error=str(e))
            return []

    def _process_legislation_item(self, matter: Dict) -> Optional[Dict]:
        """Process a single legislation item into our document format"""
        try:
            # Extract key information
            matter_id = matter.get("matterId", "")
            title = matter.get("title", "Untitled Legislation")
            record_number = matter.get("recordNumber", "")
            matter_type = matter.get("type", "Unknown")
            category = matter.get("matterCategory", "General")
            status = matter.get("statusDescription", "Unknown")
            sponsor = matter.get("filingSponsor", "Unknown")
            introduction_date = matter.get("introductionDate", "")
            committee = matter.get("committeReferral", "")
            key_legislation = matter.get("keyLegislation", "NO") == "YES"
            
            # Create comprehensive content
            content = f"""
            {title}
            
            Record Number: {record_number}
            Type: {matter_type}
            Category: {category}
            Status: {status}
            Sponsor: {sponsor}
            Introduction Date: {introduction_date}
            Committee Referral: {committee}
            Key Legislation: {'Yes' if key_legislation else 'No'}
            Economic Disclosure Required: {'Yes' if matter.get('economicDisclosure') == 'YES' else 'No'}
            Routine: {'Yes' if matter.get('routine') == 'YES' else 'No'}
            Agreed Calendar: {'Yes' if matter.get('agreedCalendar') == 'YES' else 'No'}
            
            Description: {matter.get('nicknameAlias', 'No additional description available')}
            """
            
            # Generate document ID
            doc_id = f"chicago_leg_{matter_id}"
            
            # Determine document category for our system
            system_category = self._map_category_to_system(category, matter_type)
            
            # Create document
            document = {
                "source": "chicago_city_clerk_api",
                "document_id": doc_id,
                "title": title,
                "content": content.strip(),
                "document_type": matter_type.lower(),
                "category": system_category,
                "jurisdiction": "chicago",
                "authority": "Chicago City Council",
                "url": f"https://chicago.legistar.com/LegislationDetail.aspx?ID={matter_id}",
                "effective_date": introduction_date,
                "metadata": {
                    "matter_id": matter_id,
                    "record_number": record_number,
                    "matter_type": matter_type,
                    "matter_category": category,
                    "status": status,
                    "sponsor": sponsor,
                    "committee_referral": committee,
                    "key_legislation": key_legislation,
                    "economic_disclosure": matter.get('economicDisclosure'),
                    "routine": matter.get('routine'),
                    "agreed_calendar": matter.get('agreedCalendar'),
                    "introduction_type": matter.get('introductionType'),
                    "controlling_body": matter.get('controllingBody'),
                    "file_year": matter.get('fileYear'),
                    "last_publication_date": matter.get('lastPublicationDate')
                }
            }
            
            return document
            
        except Exception as e:
            logger.error(f"Failed to process legislation item", error=str(e))
            return None

    def _map_category_to_system(self, category: str, matter_type: str) -> str:
        """Map Chicago legislation categories to our system categories"""
        category_lower = category.lower()
        type_lower = matter_type.lower()
        
        # Map based on category and type
        if "zoning" in category_lower or "building" in category_lower:
            return "construction"
        elif "business" in category_lower or "license" in category_lower:
            return "business"
        elif "health" in category_lower or "food" in category_lower:
            return "healthcare"
        elif "parking" in category_lower or "traffic" in category_lower or "transportation" in category_lower:
            return "transportation"
        elif "finance" in category_lower or "budget" in category_lower:
            return "finance"
        elif "public safety" in category_lower or "police" in category_lower or "fire" in category_lower:
            return "public_safety"
        elif "education" in category_lower or "school" in category_lower:
            return "education"
        elif "environment" in category_lower or "sustainability" in category_lower:
            return "environment"
        elif "housing" in category_lower or "residential" in category_lower:
            return "housing"
        elif "executive order" in type_lower or "proclamation" in type_lower:
            return "governance"
        elif "resolution" in type_lower:
            return "governance"
        elif "ordinance" in type_lower:
            return "governance"
        else:
            return "general"

    async def ingest_comprehensive_legislation(self, limits: Dict[str, int] = None) -> Dict:
        """Ingest comprehensive Chicago legislation data"""
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
        
        all_documents = []
        
        # Fetch recent legislation
        logger.info("Fetching recent Chicago legislation...")
        recent_docs = await self.fetch_recent_legislation(limits["recent"])
        all_documents.extend(recent_docs)
        
        # Fetch by categories
        categories_to_fetch = [
            ("ZONING RECLASSIFICATIONS", limits.get("zoning", 25)),
            ("BUSINESS LICENSES", limits.get("business", 25)),
            ("PARKING", limits.get("transportation", 25)),
            ("TRANSPORTATION", limits.get("transportation", 25)),
            ("EXECUTIVE ORDERS & PROCLAMATIONS", limits.get("executive_orders", 25))
        ]
        
        for category, limit in categories_to_fetch:
            if limit > 0:
                logger.info(f"Fetching {category} legislation...")
                category_docs = await self.fetch_legislation_by_category(category, limit)
                all_documents.extend(category_docs)
        
        # Process and store documents
        total_ingested = 0
        for doc_data in all_documents:
            try:
                # Enhanced document processing
                doc_data["summary"] = doc_data["content"][:300] + "..." if len(doc_data["content"]) > 300 else doc_data["content"]
                
                # Add searchable keywords
                doc_data["keywords"] = self._extract_keywords(doc_data["content"])
                
                # Add document hash for deduplication
                doc_data["content_hash"] = hashlib.md5(doc_data["content"].encode()).hexdigest()
                
                self.documents[doc_data["document_id"]] = doc_data
                total_ingested += 1
            except Exception as e:
                logger.error(f"Failed to process document {doc_data.get('document_id')}", error=str(e))
        
        logger.info(f"Successfully ingested {total_ingested} Chicago legislation documents.")
        return {
            "jurisdiction": "chicago",
            "data_source": "chicago_city_clerk_api",
            "documents_loaded": total_ingested,
            "limits": limits,
            "categories": self._get_category_breakdown(),
            "sources": self._get_source_breakdown()
        }

    def _extract_keywords(self, content: str) -> List[tuple]:
        """Extract keywords from document content"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top keywords
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    def _get_category_breakdown(self) -> Dict[str, int]:
        """Get breakdown of documents by category"""
        categories = {}
        for doc in self.documents.values():
            category = doc.get("category", "unknown")
            categories[category] = categories.get(category, 0) + 1
        return categories

    def _get_source_breakdown(self) -> Dict[str, int]:
        """Get breakdown of documents by source"""
        sources = {}
        for doc in self.documents.values():
            source = doc.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
        return sources

    def get_legislation_stats(self) -> Dict:
        """Get statistics about ingested legislation"""
        categories = self._get_category_breakdown()
        sources = self._get_source_breakdown()
        authorities = set()
        
        for doc in self.documents.values():
            authorities.add(doc.get("authority", "Unknown"))
        
        return {
            "jurisdiction": "chicago",
            "data_source": "chicago_city_clerk_api",
            "total_documents": len(self.documents),
            "categories": categories,
            "sources": sources,
            "authorities": list(authorities),
            "date_range": self._get_date_range(),
            "legislation_types": self._get_legislation_types()
        }

    def _get_date_range(self) -> Dict[str, str]:
        """Get date range of documents"""
        dates = []
        for doc in self.documents.values():
            if doc.get("effective_date"):
                dates.append(doc["effective_date"])
        
        if dates:
            return {
                "earliest": min(dates),
                "latest": max(dates)
            }
        return {"earliest": "N/A", "latest": "N/A"}

    def _get_legislation_types(self) -> Dict[str, int]:
        """Get breakdown by legislation type"""
        types = {}
        for doc in self.documents.values():
            doc_type = doc.get("document_type", "unknown")
            types[doc_type] = types.get(doc_type, 0) + 1
        return types

    def get_all_documents(self, limit: int = 100) -> List[Dict]:
        """Get all ingested documents"""
        return list(self.documents.values())[:limit]

    def advanced_semantic_search(self, query: str, jurisdiction: Optional[str] = None, 
                                category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Advanced semantic search through Chicago legislation"""
        results = []
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        for doc_id, doc in self.documents.items():
            if jurisdiction and doc["jurisdiction"] != jurisdiction:
                continue
            if category and doc["category"] != category:
                continue
            
            # Multi-algorithm scoring
            score = 0
            
            # 1. Title matching (highest weight)
            title_words = set(doc["title"].lower().split())
            title_overlap = len(query_words.intersection(title_words))
            if title_overlap > 0:
                score += 0.4 * (title_overlap / len(query_words))
            
            # 2. Content matching
            content_lower = doc["content"].lower()
            content_matches = sum(1 for word in query_words if word in content_lower)
            if content_matches > 0:
                score += 0.3 * (content_matches / len(query_words))
            
            # 3. Metadata matching
            metadata = doc.get("metadata", {})
            if any(word in str(metadata.get("matter_category", "")).lower() for word in query_words):
                score += 0.2
            
            if any(word in str(metadata.get("sponsor", "")).lower() for word in query_words):
                score += 0.1
            
            if score > 0:
                doc_copy = doc.copy()
                doc_copy["similarity_score"] = min(score, 1.0)
                doc_copy["match_reasons"] = self._get_match_reasons(query_words, doc)
                results.append(doc_copy)
        
        # Sort by similarity score and return top results
        results.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)
        return results[:limit]

    def _get_match_reasons(self, query_words: set, doc: Dict) -> List[str]:
        """Get reasons why a document matched the query"""
        reasons = []
        
        title_words = set(doc["title"].lower().split())
        if query_words.intersection(title_words):
            reasons.append("Title match")
        
        content_lower = doc["content"].lower()
        if any(word in content_lower for word in query_words):
            reasons.append("Content match")
        
        metadata = doc.get("metadata", {})
        if any(word in str(metadata.get("matter_category", "")).lower() for word in query_words):
            reasons.append("Category match")
        
        if any(word in str(metadata.get("sponsor", "")).lower() for word in query_words):
            reasons.append("Sponsor match")
        
        return reasons

    def generate_legislation_chat_response(self, user_message: str, 
                                         recommended_documents: List[Dict]) -> Dict:
        """Generate chat response based on Chicago legislation"""
        self.chat_history.append({
            "role": "user", 
            "message": user_message, 
            "timestamp": datetime.now().isoformat()
        })
        
        # Build context from recommended documents
        context_str = ""
        sources_list = []
        
        if recommended_documents:
            for i, doc in enumerate(recommended_documents):
                title = doc.get("title", "Untitled Legislation")
                content_snippet = doc.get("content", "No content available.")[:400] + "..."
                context_str += f"Legislation {i+1}: {title}\nContent: {content_snippet}\n\n"
                sources_list.append({
                    "title": doc.get("title"),
                    "authority": doc.get("authority"),
                    "url": doc.get("url"),
                    "category": doc.get("category"),
                    "similarity_score": doc.get("similarity_score", 0.0),
                    "match_reasons": doc.get("match_reasons", [])
                })
        
        # Generate intelligent response
        response_text = "I'm sorry, I couldn't find specific Chicago legislation related to your query."
        confidence_score = 0.0
        
        if recommended_documents:
            best_doc = recommended_documents[0]
            confidence_score = best_doc.get("similarity_score", 0.5)
            
            # Generate context-aware response
            response_text = self._generate_legislation_response(user_message, best_doc, recommended_documents)
        
        response = {
            "answer": response_text,
            "sources": sources_list,
            "confidence_score": confidence_score,
            "jurisdiction": "chicago",
            "model": "chicago-legislation-based",
            "context_used": len(recommended_documents),
            "total_documents_searched": len(self.documents),
            "search_metadata": {
                "query_processed": user_message,
                "documents_found": len(recommended_documents),
                "search_timestamp": datetime.now().isoformat()
            }
        }
        
        self.chat_history.append({
            "role": "ai", 
            "message": response_text, 
            "timestamp": datetime.now().isoformat()
        })
        
        return response

    def _generate_legislation_response(self, user_message: str, best_doc: Dict, 
                                     all_docs: List[Dict]) -> str:
        """Generate contextual response based on Chicago legislation"""
        user_message_lower = user_message.lower()
        doc_type = best_doc.get("document_type", "")
        category = best_doc.get("category", "")
        metadata = best_doc.get("metadata", {})
        
        # Zoning responses
        if "zoning" in user_message_lower:
            return f"""Based on Chicago zoning legislation '{best_doc['title']}':

**Zoning Information:**
- Record Number: {metadata.get('record_number', 'N/A')}
- Type: {metadata.get('matter_type', 'N/A')}
- Status: {metadata.get('status', 'N/A')}
- Sponsor: {metadata.get('sponsor', 'N/A')}
- Committee: {metadata.get('committee_referral', 'N/A')}

**Next Steps:**
For zoning matters in Chicago:
1. Contact the Committee on Zoning, Landmarks and Building Standards
2. Review the full legislation text
3. Check for public hearing requirements
4. Consult with the Department of Planning and Development

For more information, visit the Chicago City Clerk's office or the Department of Planning and Development."""

        # Business license responses
        elif "business" in user_message_lower or "license" in user_message_lower:
            return f"""Based on Chicago business legislation '{best_doc['title']}':

**Business Information:**
- Record Number: {metadata.get('record_number', 'N/A')}
- Type: {metadata.get('matter_type', 'N/A')}
- Status: {metadata.get('status', 'N/A')}
- Sponsor: {metadata.get('sponsor', 'N/A')}
- Category: {metadata.get('matter_category', 'N/A')}

**Requirements:**
For business matters in Chicago:
1. Contact the Department of Business Affairs and Consumer Protection
2. Review all applicable regulations
3. Complete required applications
4. Pay necessary fees

Contact the Chicago Department of Business Affairs and Consumer Protection at 312-744-6060 for assistance."""

        # Transportation/Parking responses
        elif "parking" in user_message_lower or "traffic" in user_message_lower:
            return f"""Based on Chicago transportation legislation '{best_doc['title']}':

**Transportation Information:**
- Record Number: {metadata.get('record_number', 'N/A')}
- Type: {metadata.get('matter_type', 'N/A')}
- Status: {metadata.get('status', 'N/A')}
- Sponsor: {metadata.get('sponsor', 'N/A')}
- Committee: {metadata.get('committee_referral', 'N/A')}

**Requirements:**
For transportation matters in Chicago:
1. Contact the Committee on Pedestrian and Traffic Safety
2. Review traffic and parking regulations
3. Check for permit requirements
4. Consult with the Department of Transportation

Contact the Chicago Department of Transportation for more information."""

        # General response
        else:
            return f"""Based on Chicago legislation '{best_doc['title']}':

**Legislation Details:**
- Record Number: {metadata.get('record_number', 'N/A')}
- Type: {metadata.get('matter_type', 'N/A')}
- Status: {metadata.get('status', 'N/A')}
- Sponsor: {metadata.get('sponsor', 'N/A')}
- Committee: {metadata.get('committee_referral', 'N/A')}
- Introduction Date: {metadata.get('introduction_date', 'N/A')}

**Content:**
{best_doc['content'][:300]}...

**Source Information:**
- Authority: {best_doc.get('authority', 'N/A')}
- Category: {category}
- Document Type: {doc_type}

For more detailed information, please contact the relevant Chicago department or visit the official Chicago government website."""

    def get_chat_history(self, limit: int = 20) -> List[Dict]:
        """Retrieve chat history"""
        return self.chat_history[-limit:]

    def clear_chat_history(self):
        """Clear the chat history"""
        self.chat_history = []
        logger.info("Chat history cleared.")

    def get_search_suggestions(self, jurisdiction: Optional[str] = None) -> List[str]:
        """Generate search suggestions for Chicago legislation"""
        suggestions = [
            "How do I get a zoning permit in Chicago?",
            "What are the business license requirements?",
            "How do I apply for handicapped parking?",
            "What are the current zoning regulations?",
            "How do I get a sign permit?",
            "What are the parking regulations?",
            "How do I contact the city council?",
            "What are the current ordinances?",
            "How do I get a liquor license?",
            "What are the building permit requirements?",
            "How do I report a city issue?",
            "What are the current resolutions?",
            "How do I get a street permit?",
            "What are the current executive orders?",
            "How do I get a special event permit?",
            "What are the current city policies?",
            "How do I get a construction permit?",
            "What are the current city regulations?",
            "How do I get a business permit?",
            "What are the current city laws?"
        ]
        return suggestions

    def get_analytics(self) -> Dict:
        """Get analytics about the Chicago legislation system"""
        return {
            "total_documents": len(self.documents),
            "total_chat_sessions": len(self.chat_history),
            "category_breakdown": self._get_category_breakdown(),
            "source_breakdown": self._get_source_breakdown(),
            "legislation_types": self._get_legislation_types(),
            "date_range": self._get_date_range(),
            "system_health": {
                "data_freshness": "Real-time",
                "api_status": "Active",
                "search_performance": "Optimized"
            }
        }

# Global instance
chicago_legislation_service = ChicagoLegislationService()
