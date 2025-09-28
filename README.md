# 🏛️ Chicago Legal Document Democratization Platform

> **Democratizing access to Chicago legal documents through intelligent search and AI-powered assistance**
> **Deployed link**: https://legal-info-democrati-t5dq.bolt.host/

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

The Chicago Legal Document Democratization Platform is a comprehensive web application that makes Chicago's legal documents, policies, and legislation accessible to all residents. By combining real-time data from the Chicago City Clerk API with intelligent search capabilities and AI-powered chat assistance, we're breaking down barriers to legal information access.

### 🌟 Key Features

- **📊 Real-Time Data Integration**: Live connection to Chicago City Clerk API with 600+ current legislation documents
- **🔍 Intelligent Search**: Advanced semantic search across zoning permits, business licenses, city council resolutions, and more
- **🤖 AI-Powered Chat**: Context-aware legal document assistance using Google Gemini AI
- **📱 Modern Web Interface**: Responsive React frontend with intuitive user experience
- **📈 Comprehensive Analytics**: Real-time insights into document categories, search patterns, and user engagement
- **🏗️ Scalable Architecture**: Production-ready FastAPI backend with modular design

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mgebeyehu/Black-CS-Summit.git
   cd Black-CS-Summit
   ```

2. **Backend Setup**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Start the backend server
   python main.py
   ```

3. **Frontend Setup** (Optional - already built)
   ```bash
   cd project
   npm install
   npm run build
   ```

4. **Access the Platform**
   - 🌐 **Frontend**: http://localhost:8000/
   - 📖 **API Documentation**: http://localhost:8000/api/docs
   - ❤️ **Health Check**: http://localhost:8000/health

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **Real-time Data Service**: Fetches live Chicago legislation from City Clerk API
- **Intelligent Search Engine**: Multi-algorithm semantic search with keyword matching
- **AI Chat Integration**: Google Gemini API for context-aware legal assistance
- **RESTful API**: Comprehensive endpoints for search, chat, analytics, and document management

### Frontend (React + TypeScript)
- **Modern UI/UX**: Clean, responsive design with Tailwind CSS
- **Interactive Questionnaire**: Personalized policy recommendations based on user profile
- **Real-time Chat**: AI-powered legal document assistance
- **Policy Discovery**: Advanced search and filtering capabilities

### Data Sources
- **Chicago City Clerk API**: Official legislation, ordinances, and resolutions
- **Real-time Updates**: Live data synchronization with Chicago's legislative system
- **Comprehensive Coverage**: Zoning, business, transportation, governance, and general policies

## 📊 Data & Analytics

### Current Dataset
- **600+ Real Documents**: Live Chicago legislation and policies
- **4 Categories**: Construction, General, Transportation, Governance
- **Multiple Document Types**: Ordinances, Resolutions, Executive Orders, Claims
- **Real-time Updates**: Automatic synchronization with Chicago's legislative system

### Search Capabilities
- **Semantic Search**: Intelligent matching based on document content and context
- **Category Filtering**: Targeted search within specific policy areas
- **Relevance Scoring**: Advanced algorithms for result ranking
- **Context-Aware Results**: Personalized recommendations based on user profile

## 🔧 API Endpoints

### Core Endpoints
- `GET /health` - System health check
- `GET /api/v1/documents/stats/legislation` - Document statistics
- `POST /api/v1/search/semantic` - Advanced semantic search
- `POST /api/v1/chat/ask` - AI-powered legal assistance
- `GET /api/v1/analytics` - System analytics and insights

### Data Management
- `POST /api/v1/ingest/legislation` - Trigger data ingestion
- `GET /api/v1/documents/` - Retrieve documents with filtering
- `GET /api/v1/search/suggestions` - Get search suggestions

## 🎨 User Experience

### Personalized Policy Discovery
1. **User Questionnaire**: Comprehensive profile assessment
2. **Intelligent Matching**: AI-powered policy recommendations
3. **Category Diversity**: Ensures representation across all policy areas
4. **Relevance Scoring**: Prioritizes most relevant documents

### AI-Powered Assistance
- **Context-Aware Chat**: Uses recommended documents as context
- **Source Attribution**: Provides links to official documents
- **Confidence Scoring**: Transparent AI response confidence levels
- **Conversation History**: Maintains chat context across sessions

## 🛠️ Development

### Project Structure
```
├── main.py                          # Main server entry point
├── chicago_legislation_server.py    # FastAPI application
├── app/
│   ├── core/
│   │   └── config.py               # Configuration management
│   └── services/
│       └── chicago_legislation_service.py  # Data service layer
├── project/                        # React frontend
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── services/              # API client
│   │   └── types/                 # TypeScript definitions
│   └── dist/                      # Built frontend
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

### Key Technologies
- **Backend**: FastAPI, Python 3.10+, aiohttp, structlog
- **Frontend**: React 18, TypeScript, Tailwind CSS, Vite
- **AI Integration**: Google Gemini API
- **Data Source**: Chicago City Clerk API
- **Deployment**: Production-ready with GZip compression and CORS support

## 🌟 Hackathon Highlights

### Innovation
- **Real-time Legal Data**: First platform to integrate live Chicago legislation
- **AI-Powered Legal Assistance**: Context-aware chat with official document sources
- **Democratized Access**: Makes complex legal documents accessible to all residents
- **Personalized Recommendations**: Tailored policy suggestions based on user profiles

### Technical Excellence
- **Scalable Architecture**: Modular design for easy expansion
- **Production Ready**: Comprehensive error handling and logging
- **Modern Stack**: Latest technologies for optimal performance
- **Real-time Updates**: Live synchronization with official data sources

### Social Impact
- **Accessibility**: Breaks down barriers to legal information
- **Transparency**: Promotes government transparency and civic engagement
- **Education**: Helps residents understand their rights and obligations
- **Community**: Fosters informed civic participation

## 📈 Future Enhancements

- **Multi-Jurisdiction Support**: Expand to other cities and states
- **Advanced AI Features**: Document summarization and legal advice
- **Mobile Application**: Native iOS and Android apps
- **Community Features**: User reviews and policy discussions
- **Analytics Dashboard**: Advanced insights for policymakers

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Chicago City Clerk**: For providing open access to legislative data
- **Google Gemini**: For AI-powered chat capabilities
- **FastAPI & React Communities**: For excellent frameworks and documentation
- **Black CS Summit**: For the opportunity to build something meaningful

## 📞 Contact

- **Project Lead**: [Your Name]
- **GitHub**: [mgebeyehu/Black-CS-Summit](https://github.com/mgebeyehu/Black-CS-Summit)
- **Email**: [your.email@example.com]

---

**Built with ❤️ for the Chicago community and the Black CS Summit Hackathon**
