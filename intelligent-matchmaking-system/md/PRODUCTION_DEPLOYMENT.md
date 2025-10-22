# 🚀 Production Deployment Guide

## ✅ Pre-Deployment Checklist

### Database Setup
- [ ] MongoDB installed and running
- [ ] Database name configured: `intelligent_matchmaking`
- [ ] Demo users created
- [ ] Demo experts created
- [ ] Indexes created for performance

### Backend Configuration
- [ ] Environment variables set
- [ ] CORS origins configured
- [ ] JWT secret key set
- [ ] MongoDB URI configured
- [ ] All dependencies installed

### Frontend Configuration
- [ ] API base URL configured
- [ ] All mock data removed
- [ ] Production build tested
- [ ] Environment variables set

---

## 🗄️ Database Setup

### 1. Create Database and Collections

```bash
# Connect to MongoDB
mongosh

# Use database
use intelligent_matchmaking

# Create collections with validation
db.createCollection("users")
db.createCollection("posts")
db.createCollection("matches")
db.createCollection("study_groups")
```

### 2. Create Indexes for Performance

```bash
cd database
python create_indexes.py
```

Or manually:
```javascript
// In mongosh
use intelligent_matchmaking

// User indexes
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "username": 1 }, { unique: true })
db.users.createIndex({ "role": 1 })
db.users.createIndex({ "skills.interests": 1 })
db.users.createIndex({ "expertise_areas": 1 })

// Post indexes
db.posts.createIndex({ "user_id": 1 })
db.posts.createIndex({ "created_at": -1 })
db.posts.createIndex({ "tags": 1 })

// Match indexes
db.matches.createIndex({ "mentor_id": 1 })
db.matches.createIndex({ "mentee_id": 1 })
db.matches.createIndex({ "status": 1 })

// Study group indexes
db.study_groups.createIndex({ "topics": 1 })
db.study_groups.createIndex({ "created_by": 1 })
db.study_groups.createIndex({ "members.user_id": 1 })
```

### 3. Create Demo Data

```bash
cd database

# Create demo users
python create_demo_users.py

# Create demo experts
python create_demo_experts.py
```

---

## 🔧 Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in `backend/` directory:

```env
# Application
APP_NAME="Intelligent Matchmaking System"
APP_ENV=production
DEBUG=False

# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=intelligent_matchmaking

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 3. Start Backend Server

**Development:**
```bash
python start_server.py
```

**Production (with Gunicorn):**
```bash
pip install gunicorn uvicorn[standard]
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 💻 Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env` file in `frontend/` directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=production
```

### 3. Remove Mock Data

All mock data has been removed from:
- ✅ `Dashboard-new.js` - Uses real API
- ✅ `StudyGroups-production.js` - Uses real API
- ✅ `Matches-production.js` - Uses real API
- ✅ `Resources.js` - Needs backend implementation

Update imports in `App.js`:

```javascript
import StudyGroups from './pages/StudyGroups-production';
import Matches from './pages/Matches-production';
```

### 4. Build for Production

```bash
npm run build
```

### 5. Serve Production Build

**Option 1: Using serve**
```bash
npm install -g serve
serve -s build -l 3000
```

**Option 2: Using nginx**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /path/to/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 🎯 Production Checklist

### Security
- [ ] Change default SECRET_KEY in backend
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS properly
- [ ] Set secure cookie settings
- [ ] Enable rate limiting
- [ ] Add input validation
- [ ] Sanitize user inputs

### Performance
- [ ] Enable MongoDB indexes
- [ ] Configure caching (Redis)
- [ ] Enable gzip compression
- [ ] Optimize images
- [ ] Minify JavaScript/CSS
- [ ] Use CDN for static assets

### Monitoring
- [ ] Set up error logging (Sentry)
- [ ] Configure application monitoring
- [ ] Set up database monitoring
- [ ] Enable health check endpoints
- [ ] Configure alerts

### Backup
- [ ] Set up MongoDB backups
- [ ] Configure automated backups
- [ ] Test backup restoration
- [ ] Document backup procedures

---

## 🐳 Docker Deployment

### 1. Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### 2. Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3. Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7
    container_name: matchmaking-mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: intelligent_matchmaking

  backend:
    build: ./backend
    container_name: matchmaking-backend
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      MONGODB_URI: mongodb://mongodb:27017
      MONGODB_DB_NAME: intelligent_matchmaking
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    container_name: matchmaking-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      REACT_APP_API_URL: http://localhost:8000

volumes:
  mongodb_data:
```

### 4. Deploy with Docker

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🔍 Testing Production Build

### 1. Smoke Tests

```bash
# Test backend health
curl http://localhost:8000/health

# Test authentication
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student@example.com&password=student123"

# Test expert matches
curl -X GET http://localhost:8000/matches/expert-matches \
  -H "Authorization: Bearer <token>"

# Test posts
curl -X GET http://localhost:8000/social/posts?limit=10 \
  -H "Authorization: Bearer <token>"
```

### 2. Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test endpoint
ab -n 1000 -c 10 http://localhost:8000/health
```

---

## 📊 Monitoring Endpoints

### Backend Health Check

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if db else "disconnected"
    }
```

### Metrics Endpoint (Optional)

```python
@app.get("/metrics")
async def metrics():
    return {
        "total_users": await db.users.count_documents({}),
        "total_posts": await db.posts.count_documents({}),
        "total_experts": await db.users.count_documents({"role": {"$in": ["expert", "professional"]}}),
        "active_users": await db.users.count_documents({"is_active": True})
    }
```

---

## 🚨 Troubleshooting

### Backend Issues

**MongoDB Connection Failed:**
```bash
# Check MongoDB is running
sudo systemctl status mongod

# Check connection string
echo $MONGODB_URI
```

**Import Errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
echo $PYTHONPATH
```

### Frontend Issues

**API Calls Failing:**
- Check CORS configuration in backend
- Verify API_URL environment variable
- Check network tab in browser DevTools

**Build Errors:**
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📝 Post-Deployment

### 1. Create Admin User

```python
# In Python shell
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.intelligent_matchmaking

# Create admin
await db.users.insert_one({
    "email": "admin@yourdomain.com",
    "username": "admin",
    "full_name": "System Administrator",
    "hashed_password": pwd_context.hash("secure_password_here"),
    "role": "admin",
    "is_active": True,
    "is_verified": True
})
```

### 2. Configure Email Notifications

Update `backend/app/utils/email_helper.py` with your SMTP settings.

### 3. Set Up SSL/TLS

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com
```

---

## 🎉 Your Application is Production-Ready!

Access your application:
- **Frontend:** http://localhost:3000 or https://yourdomain.com
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

**Demo Credentials:**
- Student: `student@example.com` / `student123`
- Expert: `john.expert@example.com` / `expert123`
- Admin: `admin@example.com` / `admin123`

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
