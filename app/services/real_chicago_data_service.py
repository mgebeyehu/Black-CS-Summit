"""
Real Chicago Data Integration Service
Fetches actual data from Chicago's official APIs
"""
import asyncio
import aiohttp
import requests
from typing import List, Dict, Optional, Any
import structlog
from datetime import datetime, timedelta
import json
import re

logger = structlog.get_logger()

class RealChicagoDataService:
    def __init__(self):
        self.session = None
        self.chicago_apis = {
            "building_permits": "https://data.cityofchicago.org/resource/ydr8-5enu.json",
            "business_licenses": "https://data.cityofchicago.org/resource/uupf-x98q.json",
            "city_council_meetings": "https://data.cityofchicago.org/resource/7c8c-9w7x.json",
            "crime_data": "https://data.cityofchicago.org/resource/ijzp-q8t2.json",
            "food_inspections": "https://data.cityofchicago.org/resource/4ijn-s7e5.json",
            "building_violations": "https://data.cityofchicago.org/resource/22u3-xenr.json"
        }
    
    async def initialize(self):
        """Initialize the Chicago data service"""
        self.session = aiohttp.ClientSession()
        logger.info("Real Chicago data service initialized")
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
    
    async def fetch_real_building_permits(self, limit: int = 20) -> List[Dict]:
        """Fetch real building permits from Chicago API"""
        documents = []
        
        try:
            url = self.chicago_apis["building_permits"]
            params = {
                "$limit": limit,
                "$order": "application_start_date DESC"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for record in data:
                        doc = {
                            "source": "chicago_building_permits_real",
                            "document_id": f"chicago_permits_real_{record.get('id', 'unknown')}",
                            "title": f"Building Permit - {record.get('permit_type', 'Unknown Type')}",
                            "content": self._create_building_permit_content(record),
                            "document_type": "permit",
                            "category": "construction",
                            "jurisdiction": "chicago",
                            "authority": "Chicago Department of Buildings",
                            "url": f"https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu",
                            "effective_date": record.get("application_start_date"),
                            "metadata": {
                                "permit_type": record.get("permit_type"),
                                "work_description": record.get("work_description"),
                                "total_fees": record.get("total_fees"),
                                "reported_cost": record.get("reported_cost"),
                                "community_area": record.get("community_area"),
                                "zip_code": record.get("zip_code"),
                                "latitude": record.get("latitude"),
                                "longitude": record.get("longitude")
                            }
                        }
                        documents.append(doc)
                
                logger.info(f"Fetched {len(documents)} real Chicago building permits")
                
        except Exception as e:
            logger.error("Failed to fetch real Chicago building permits", error=str(e))
        
        return documents
    
    async def fetch_real_business_licenses(self, limit: int = 20) -> List[Dict]:
        """Fetch real business licenses from Chicago API"""
        documents = []
        
        try:
            url = self.chicago_apis["business_licenses"]
            params = {
                "$limit": limit,
                "$order": "license_start_date DESC"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for record in data:
                        doc = {
                            "source": "chicago_business_licenses_real",
                            "document_id": f"chicago_license_real_{record.get('id', 'unknown')}",
                            "title": f"Business License - {record.get('business_activity', 'Unknown Activity')}",
                            "content": self._create_business_license_content(record),
                            "document_type": "license",
                            "category": "business",
                            "jurisdiction": "chicago",
                            "authority": "Chicago Department of Business Affairs and Consumer Protection",
                            "url": f"https://data.cityofchicago.org/Business-Economic-Development-Opportunity/Business-Licenses/uupf-x98q",
                            "effective_date": record.get("license_start_date"),
                            "metadata": {
                                "business_activity": record.get("business_activity"),
                                "license_description": record.get("license_description"),
                                "license_status": record.get("license_status"),
                                "zip_code": record.get("zip_code"),
                                "ward": record.get("ward"),
                                "latitude": record.get("latitude"),
                                "longitude": record.get("longitude")
                            }
                        }
                        documents.append(doc)
                
                logger.info(f"Fetched {len(documents)} real Chicago business licenses")
                
        except Exception as e:
            logger.error("Failed to fetch real Chicago business licenses", error=str(e))
        
        return documents
    
    async def fetch_real_city_council_meetings(self, limit: int = 10) -> List[Dict]:
        """Fetch real city council meetings from Chicago API"""
        documents = []
        
        try:
            url = self.chicago_apis["city_council_meetings"]
            params = {
                "$limit": limit,
                "$order": "meeting_date DESC"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for record in data:
                        doc = {
                            "source": "chicago_city_council_real",
                            "document_id": f"chicago_meeting_real_{record.get('id', 'unknown')}",
                            "title": f"City Council Meeting - {record.get('meeting_date', 'Unknown Date')}",
                            "content": self._create_city_council_content(record),
                            "document_type": "meeting_record",
                            "category": "governance",
                            "jurisdiction": "chicago",
                            "authority": "Chicago City Council",
                            "url": f"https://data.cityofchicago.org/City-Government/City-Council-Meetings/7c8c-9w7x",
                            "effective_date": record.get("meeting_date"),
                            "metadata": {
                                "meeting_type": record.get("meeting_type"),
                                "agenda_items": record.get("agenda_items"),
                                "attendance": record.get("attendance"),
                                "location": record.get("location")
                            }
                        }
                        documents.append(doc)
                
                logger.info(f"Fetched {len(documents)} real Chicago City Council meetings")
                
        except Exception as e:
            logger.error("Failed to fetch real Chicago City Council meetings", error=str(e))
        
        return documents
    
    async def fetch_real_food_inspections(self, limit: int = 15) -> List[Dict]:
        """Fetch real food inspection data from Chicago API"""
        documents = []
        
        try:
            url = self.chicago_apis["food_inspections"]
            params = {
                "$limit": limit,
                "$order": "inspection_date DESC"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for record in data:
                        doc = {
                            "source": "chicago_food_inspections_real",
                            "document_id": f"chicago_food_real_{record.get('inspection_id', 'unknown')}",
                            "title": f"Food Inspection - {record.get('dba_name', 'Unknown Restaurant')}",
                            "content": self._create_food_inspection_content(record),
                            "document_type": "inspection_report",
                            "category": "healthcare",
                            "jurisdiction": "chicago",
                            "authority": "Chicago Department of Public Health",
                            "url": f"https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5",
                            "effective_date": record.get("inspection_date"),
                            "metadata": {
                                "dba_name": record.get("dba_name"),
                                "inspection_type": record.get("inspection_type"),
                                "results": record.get("results"),
                                "violations": record.get("violations"),
                                "zip_code": record.get("zip"),
                                "latitude": record.get("latitude"),
                                "longitude": record.get("longitude")
                            }
                        }
                        documents.append(doc)
                
                logger.info(f"Fetched {len(documents)} real Chicago food inspections")
                
        except Exception as e:
            logger.error("Failed to fetch real Chicago food inspections", error=str(e))
        
        return documents
    
    async def fetch_real_building_violations(self, limit: int = 15) -> List[Dict]:
        """Fetch real building violations from Chicago API"""
        documents = []
        
        try:
            url = self.chicago_apis["building_violations"]
            params = {
                "$limit": limit,
                "$order": "violation_date DESC"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for record in data:
                        doc = {
                            "source": "chicago_building_violations_real",
                            "document_id": f"chicago_violation_real_{record.get('id', 'unknown')}",
                            "title": f"Building Violation - {record.get('violation_code', 'Unknown Code')}",
                            "content": self._create_building_violation_content(record),
                            "document_type": "violation_notice",
                            "category": "construction",
                            "jurisdiction": "chicago",
                            "authority": "Chicago Department of Buildings",
                            "url": f"https://data.cityofchicago.org/Buildings/Building-Violations/22u3-xenr",
                            "effective_date": record.get("violation_date"),
                            "metadata": {
                                "violation_code": record.get("violation_code"),
                                "violation_description": record.get("violation_description"),
                                "violation_status": record.get("violation_status"),
                                "zip_code": record.get("zip_code"),
                                "latitude": record.get("latitude"),
                                "longitude": record.get("longitude")
                            }
                        }
                        documents.append(doc)
                
                logger.info(f"Fetched {len(documents)} real Chicago building violations")
                
        except Exception as e:
            logger.error("Failed to fetch real Chicago building violations", error=str(e))
        
        return documents
    
    def _create_building_permit_content(self, record: Dict) -> str:
        """Create content for building permit document"""
        content = f"Building Permit Application for {record.get('permit_type', 'Unknown Type')}. "
        content += f"Work Description: {record.get('work_description', 'Not specified')}. "
        content += f"Total Fees: ${record.get('total_fees', '0')}. "
        content += f"Reported Cost: ${record.get('reported_cost', '0')}. "
        content += f"Community Area: {record.get('community_area', 'Not specified')}. "
        content += f"Zip Code: {record.get('zip_code', 'Not specified')}. "
        content += f"Application Start Date: {record.get('application_start_date', 'Not specified')}."
        return content
    
    def _create_business_license_content(self, record: Dict) -> str:
        """Create content for business license document"""
        content = f"Business License for {record.get('business_activity', 'Unknown Activity')}. "
        content += f"License Description: {record.get('license_description', 'Not specified')}. "
        content += f"License Status: {record.get('license_status', 'Unknown')}. "
        content += f"Zip Code: {record.get('zip_code', 'Not specified')}. "
        content += f"Ward: {record.get('ward', 'Not specified')}. "
        content += f"License Start Date: {record.get('license_start_date', 'Not specified')}."
        return content
    
    def _create_city_council_content(self, record: Dict) -> str:
        """Create content for city council meeting document"""
        content = f"City Council Meeting on {record.get('meeting_date', 'Unknown Date')}. "
        content += f"Meeting Type: {record.get('meeting_type', 'Not specified')}. "
        content += f"Agenda Items: {record.get('agenda_items', 'Not specified')}. "
        content += f"Attendance: {record.get('attendance', 'Not specified')}. "
        content += f"Location: {record.get('location', 'Not specified')}."
        return content
    
    def _create_food_inspection_content(self, record: Dict) -> str:
        """Create content for food inspection document"""
        content = f"Food Inspection for {record.get('dba_name', 'Unknown Restaurant')}. "
        content += f"Inspection Type: {record.get('inspection_type', 'Not specified')}. "
        content += f"Results: {record.get('results', 'Not specified')}. "
        content += f"Violations: {record.get('violations', 'None')}. "
        content += f"Zip Code: {record.get('zip', 'Not specified')}. "
        content += f"Inspection Date: {record.get('inspection_date', 'Not specified')}."
        return content
    
    def _create_building_violation_content(self, record: Dict) -> str:
        """Create content for building violation document"""
        content = f"Building Violation Code: {record.get('violation_code', 'Unknown')}. "
        content += f"Violation Description: {record.get('violation_description', 'Not specified')}. "
        content += f"Violation Status: {record.get('violation_status', 'Unknown')}. "
        content += f"Zip Code: {record.get('zip_code', 'Not specified')}. "
        content += f"Violation Date: {record.get('violation_date', 'Not specified')}."
        return content
    
    async def fetch_all_real_chicago_data(self, limit_per_source: int = 10) -> List[Dict]:
        """Fetch all real Chicago data sources"""
        all_documents = []
        
        # Fetch from all sources concurrently
        tasks = [
            self.fetch_real_building_permits(limit_per_source),
            self.fetch_real_business_licenses(limit_per_source),
            self.fetch_real_city_council_meetings(limit_per_source),
            self.fetch_real_food_inspections(limit_per_source),
            self.fetch_real_building_violations(limit_per_source)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_documents.extend(result)
            else:
                logger.error(f"Error fetching real Chicago data: {result}")
        
        logger.info(f"Total real Chicago documents fetched: {len(all_documents)}")
        return all_documents

# Global real Chicago data service instance
real_chicago_data_service = RealChicagoDataService()
