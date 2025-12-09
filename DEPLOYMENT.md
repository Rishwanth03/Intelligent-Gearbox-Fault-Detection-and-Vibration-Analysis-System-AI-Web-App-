# Deployment Guide

This guide provides instructions for deploying the Gearbox Fault Detection System in various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)

## Local Development

For local development and testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python app.py
```

The application will be available at `http://localhost:5000`

## Production Deployment

### Using Gunicorn (Recommended)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Using uWSGI

1. **Install uWSGI**
   ```bash
   pip install uwsgi
   ```

2. **Create uwsgi.ini**
   ```ini
   [uwsgi]
   module = app:app
   master = true
   processes = 4
   socket = 0.0.0.0:5000
   chmod-socket = 660
   vacuum = true
   die-on-term = true
   ```

3. **Run uWSGI**
   ```bash
   uwsgi --ini uwsgi.ini
   ```

### Nginx Configuration

Create `/etc/nginx/sites-available/gearbox-detector`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Increase timeout for large file uploads
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # Increase max file upload size
    client_max_body_size 20M;
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/gearbox-detector /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads data models

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Build and Run

```bash
# Build image
docker build -t gearbox-detector .

# Run container
docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/models:/app/models \
  --name gearbox-detector \
  gearbox-detector
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./models:/app/models
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## Cloud Deployment

### Heroku

1. **Create Procfile**
   ```
   web: gunicorn app:app
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy**
   ```bash
   eb init -p python-3.11 gearbox-detector
   eb create gearbox-detector-env
   eb deploy
   ```

### Google Cloud Platform (App Engine)

1. **Create app.yaml**
   ```yaml
   runtime: python311
   entrypoint: gunicorn -b :$PORT app:app

   handlers:
   - url: /.*
     script: auto

   automatic_scaling:
     min_instances: 1
     max_instances: 10
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

### Azure App Service

```bash
# Create resource group
az group create --name gearbox-rg --location eastus

# Create App Service plan
az appservice plan create --name gearbox-plan --resource-group gearbox-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group gearbox-rg --plan gearbox-plan --name gearbox-detector --runtime "PYTHON:3.11"

# Deploy
az webapp up --name gearbox-detector --resource-group gearbox-rg
```

## Environment Variables

Set these environment variables in production:

- `SECRET_KEY`: A secure random string for Flask sessions
- `FLASK_ENV`: Set to `production`
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)
- `UPLOAD_FOLDER`: Path to upload directory
- `MODEL_FOLDER`: Path to ML models directory

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Secret Key**: Use a strong, random secret key
3. **File Upload**: Validate and sanitize uploaded files
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Authentication**: Add user authentication for production use
6. **CORS**: Configure CORS appropriately
7. **Input Validation**: Validate all user inputs
8. **Error Handling**: Don't expose sensitive error information

## Performance Optimization

1. **Caching**: Implement caching for frequently accessed data
2. **Async Processing**: Use Celery for long-running analysis tasks
3. **Load Balancing**: Use multiple workers behind a load balancer
4. **CDN**: Serve static assets via CDN
5. **Database**: Use a database for storing analysis history

## Monitoring and Logging

1. **Application Logs**: Configure proper logging
2. **Error Tracking**: Use services like Sentry
3. **Performance Monitoring**: Use APM tools
4. **Uptime Monitoring**: Set up health check endpoints

## Backup and Recovery

1. **Database Backups**: Regular automated backups
2. **Model Versioning**: Keep versioned copies of ML models
3. **Configuration Backups**: Backup configuration files
4. **Disaster Recovery Plan**: Document recovery procedures

## Maintenance

1. **Updates**: Keep dependencies updated
2. **Security Patches**: Apply security patches promptly
3. **Performance Monitoring**: Regular performance reviews
4. **Log Analysis**: Review logs for issues
5. **User Feedback**: Monitor and respond to user issues

## Support

For deployment issues or questions, please open an issue on GitHub.
