# Deployment Guide

## Chicago Legal Document Democratization Platform

This guide provides comprehensive instructions for deploying the Chicago Legal Document Democratization Platform in various environments.

## 🚀 Quick Deployment

### Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/mgebeyehu/Black-CS-Summit.git
   cd Black-CS-Summit
   pip install -r requirements.txt
   ```

2. **Start the Server**
   ```bash
   python main.py
   ```

3. **Access the Platform**
   - Frontend: http://localhost:8000/
   - API Docs: http://localhost:8000/api/docs

## 🌐 Production Deployment

### Environment Setup

1. **System Requirements**
   - Python 3.10+
   - 2GB RAM minimum
   - 1GB disk space
   - Internet connection for API access

2. **Environment Variables**
   ```bash
   # Optional: Chicago API Token (for higher rate limits)
   export CHICAGO_API_APP_TOKEN="your_token_here"
   
   # Optional: Gemini API Key (for enhanced AI features)
   export GEMINI_API_KEY="your_gemini_key_here"
   ```

### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["python", "main.py"]
   ```

2. **Build and Run**
   ```bash
   docker build -t chicago-legal-platform .
   docker run -p 8000:8000 chicago-legal-platform
   ```

### Cloud Deployment

#### Heroku

1. **Create Procfile**
   ```
   web: python main.py
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

#### AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t3.medium or larger
   - Security group with port 8000 open

2. **Setup Server**
   ```bash
   sudo apt update
   sudo apt install python3.10 python3-pip nginx
   
   git clone https://github.com/mgebeyehu/Black-CS-Summit.git
   cd Black-CS-Summit
   pip3 install -r requirements.txt
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Start with PM2**
   ```bash
   npm install -g pm2
   pm2 start main.py --name chicago-legal-platform
   pm2 startup
   pm2 save
   ```

#### Google Cloud Platform

1. **Create App Engine Configuration**
   ```yaml
   # app.yaml
   runtime: python310
   
   env_variables:
     CHICAGO_API_APP_TOKEN: "your_token"
   
   automatic_scaling:
     min_instances: 1
     max_instances: 10
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

#### Azure

1. **Create Web App**
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myAppName --runtime "PYTHON|3.10"
   ```

2. **Deploy**
   ```bash
   az webapp deployment source config --name myAppName --resource-group myResourceGroup --repo-url https://github.com/mgebeyehu/Black-CS-Summit.git --branch main --manual-integration
   ```

## 🔧 Configuration

### Production Settings

1. **Update main.py for Production**
   ```python
   if __name__ == "__main__":
       uvicorn.run(
           "chicago_legislation_server:app",
           host="0.0.0.0",
           port=int(os.environ.get("PORT", 8000)),
           reload=False,  # Disable reload in production
           log_level="info"
       )
   ```

2. **Environment Configuration**
   ```python
   # app/core/config.py
   class Settings(BaseSettings):
       # Production settings
       DEBUG: bool = False
       LOG_LEVEL: str = "INFO"
       
       # Security
       SECRET_KEY: str = os.environ.get("SECRET_KEY", "your-secret-key")
       
       # CORS
       ALLOWED_ORIGINS: List[str] = [
           "https://yourdomain.com",
           "https://www.yourdomain.com"
       ]
   ```

### Performance Optimization

1. **GZip Compression** (Already enabled)
2. **Caching Headers**
   ```python
   @app.middleware("http")
   async def add_cache_headers(request: Request, call_next):
       response = await call_next(request)
       if request.url.path.startswith("/api/"):
           response.headers["Cache-Control"] = "public, max-age=300"
       return response
   ```

3. **Database Connection Pooling** (For future database integration)

## 📊 Monitoring

### Health Checks

1. **Basic Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Detailed Status**
   ```bash
   curl http://localhost:8000/api/v1/analytics
   ```

### Logging

1. **Structured Logging** (Already configured)
   - JSON format for easy parsing
   - Request/response logging
   - Error tracking

2. **Log Aggregation**
   - Use services like Loggly, Papertrail, or ELK stack
   - Monitor for errors and performance issues

### Metrics

1. **Application Metrics**
   - Response times
   - Request counts
   - Error rates
   - Document ingestion status

2. **System Metrics**
   - CPU usage
   - Memory consumption
   - Disk space
   - Network I/O

## 🔒 Security

### Production Security Checklist

- [ ] **HTTPS**: Use SSL/TLS certificates
- [ ] **CORS**: Configure allowed origins
- [ ] **Rate Limiting**: Implement request limits
- [ ] **Input Validation**: Validate all inputs
- [ ] **Error Handling**: Don't expose sensitive information
- [ ] **API Keys**: Secure environment variables
- [ ] **Dependencies**: Keep packages updated
- [ ] **Firewall**: Configure network security

### SSL/TLS Setup

1. **Let's Encrypt (Free)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

2. **Nginx SSL Configuration**
   ```nginx
   server {
       listen 443 ssl;
       server_name yourdomain.com;
       
       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

## 🔄 Updates and Maintenance

### Automated Updates

1. **GitHub Actions** (Recommended)
   ```yaml
   # .github/workflows/deploy.yml
   name: Deploy to Production
   
   on:
     push:
       branches: [main]
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Deploy to server
           run: |
             # Your deployment commands
   ```

2. **Manual Updates**
   ```bash
   git pull origin main
   pip install -r requirements.txt
   pm2 restart chicago-legal-platform
   ```

### Backup Strategy

1. **Code Backup**: Git repository
2. **Configuration Backup**: Environment variables
3. **Data Backup**: Document cache (if implemented)
4. **Log Backup**: Application logs

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **Permission Denied**
   ```bash
   sudo chown -R $USER:$USER /path/to/app
   chmod +x main.py
   ```

3. **Memory Issues**
   ```bash
   # Monitor memory usage
   htop
   # Restart if needed
   pm2 restart chicago-legal-platform
   ```

4. **API Connection Issues**
   - Check internet connectivity
   - Verify Chicago API is accessible
   - Check firewall settings

### Performance Issues

1. **Slow Response Times**
   - Check server resources
   - Monitor API response times
   - Consider caching strategies

2. **High Memory Usage**
   - Monitor document cache size
   - Implement cache limits
   - Restart service periodically

## 📞 Support

### Getting Help

1. **Documentation**: Check this guide and API docs
2. **Issues**: Report on GitHub
3. **Community**: Join discussions
4. **Contact**: [Your contact information]

### Emergency Procedures

1. **Service Down**
   ```bash
   pm2 restart chicago-legal-platform
   pm2 logs chicago-legal-platform
   ```

2. **Data Issues**
   ```bash
   # Re-ingest data
   curl -X POST http://localhost:8000/api/v1/ingest/legislation
   ```

3. **Security Incident**
   - Check logs for suspicious activity
   - Update security configurations
   - Notify users if necessary

---

**Last Updated**: September 28, 2025
