# Chicago Legal Document Democratization Platform

A hackathon-winning backend platform that democratizes access to Chicago's legal documents using real data from the city's official APIs.

## 🏆 **What Makes This Special**

- **Real Chicago Data**: Live data from Chicago's official open data portal
- **5 Data Sources**: Building permits, business licenses, city council meetings, food inspections, building violations
- **AI-Powered Search**: Intelligent semantic search and chat
- **Source Attribution**: Always cites Chicago authorities
- **No Dependencies Issues**: Simple, reliable implementation

## 🚀 **Quick Start**

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python real_chicago_api_server.py
```

### 3. Test the Platform
```bash
python test_real_chicago_api.py
```

### 4. Access the API
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Data Sources**: http://localhost:8000/api/v1/data-sources

## 📊 **Real Chicago Data Sources**

```
✅ Building Permits: https://data.cityofchicago.org/resource/ydr8-5enu.json
✅ Business Licenses: https://data.cityofchicago.org/resource/uupf-x98q.json
✅ City Council Meetings: https://data.cityofchicago.org/resource/7c8c-9w7x.json
✅ Food Inspections: https://data.cityofchicago.org/resource/4ijn-s7e5.json
✅ Building Violations: https://data.cityofchicago.org/resource/22u3-xenr.json
```

## 🔧 **API Endpoints**

### Core Endpoints
- `GET /health` - Health check
- `GET /api/v1/data-sources` - Available data sources
- `POST /api/v1/ingest/real-chicago` - Trigger data ingestion
- `GET /api/v1/documents/stats/overview` - Document statistics

### Search & Chat
- `POST /api/v1/search/semantic` - Semantic document search
- `POST /api/v1/chat/ask` - AI chat with document context
- `GET /api/v1/chat/history` - Conversation history
- `POST /api/v1/chat/clear` - Clear chat history

### Documents
- `GET /api/v1/documents/` - Get all documents
- `GET /api/v1/documents/{id}` - Get specific document

## 🏗️ **Architecture**

### Clean Structure
```
├── app/
│   ├── core/
│   │   └── config.py          # Configuration
│   ├── services/
│   │   └── real_chicago_data_service.py  # Real data integration
│   └── main.py               # Main FastAPI app
├── real_chicago_api_server.py # Production server
├── test_real_chicago_api.py   # Test script
├── requirements.txt           # Dependencies
└── README.md                 # This file
```

### Key Features
- **Real Data Integration**: Fetches live data from Chicago's APIs
- **Simple Architecture**: No complex ML dependencies
- **Fast Performance**: Efficient data processing
- **Error Handling**: Robust error handling for API failures

## 📈 **Data Examples**

### Real Building Permits
- **Cost**: $140,000 (Dominican Fest mobile stage)
- **Location**: Community Area 24 (Humboldt Park)
- **Work**: 32' x 24' mobile stage with wings

### Real Business Licenses
- **Hair Services**: Active license in Zip 60614, Ward 44
- **Hotel License**: 7+ sleeping rooms in Zip 60610, Ward 27
- **Delivery Device Program**: Emerging business pilot program

### Real Food Inspections
- **Perfect Beginnings Child Development Center**: Pass with minor violations
- **Family Dollar #2668**: Pass with no violations
- **Bon Bon Sandwiches**: Pass with no violations

### Real Building Violations
- **CN107035**: MAINTAIN EXIT SIGN ILLUMINATED (Status: OPEN)
- **CN065014**: REPAIR LINTELS (Status: OPEN)
- **CN104025**: MAINTAIN WINDOW SASH (Status: OPEN)

## 🎯 **Hackathon Features**

### Technical Excellence
- ✅ **Real API Integration**: Live data from Chicago's official APIs
- ✅ **No Dependencies Issues**: Simple, reliable implementation
- ✅ **Fast Performance**: Efficient data fetching and processing
- ✅ **Error Handling**: Robust error handling for API failures

### User Value
- ✅ **Real Information**: Users get actual Chicago legal information
- ✅ **Source Credibility**: Always cites Chicago authorities
- ✅ **Practical Guidance**: Real permit costs, license requirements, inspection results
- ✅ **Location Data**: Real addresses, coordinates, community areas

### Demo Ready
- ✅ **Working API**: All endpoints functional with real data
- ✅ **Live Data**: Fresh data from Chicago's APIs
- ✅ **AI Responses**: Context-aware responses using real documents
- ✅ **Source Attribution**: Always cites real Chicago authorities

## 🏆 **Why This Wins Hackathons**

1. **Real Data**: Not mock data - actual Chicago permit applications, licenses, inspections
2. **Technical Competence**: Real API integration with proper error handling
3. **User Value**: Actionable information from real Chicago legal data
4. **Source Credibility**: Always cites Chicago authorities
5. **Practical Utility**: Users get real permit costs, license requirements, inspection results
6. **No Dependencies Issues**: Simple, reliable implementation that works out of the box

## 📝 **Environment Variables**

Create a `.env` file with:
```
# Optional: Chicago API App Token (for higher rate limits)
CHICAGO_API_APP_TOKEN=your_app_token_here
```

## 🤝 **Contributing**

This is a hackathon project focused on demonstrating real Chicago data integration. The platform successfully democratizes access to Chicago's legal information through a working, reliable backend.

## 📄 **License**

This project is part of a hackathon submission for democratizing access to legal documents.

---

**Ready to win hackathons with real Chicago data integration! 🚀**