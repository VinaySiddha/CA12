# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB running on localhost:27017

## Setup (5 minutes)

### 1. Start MongoDB
```bash
# Make sure MongoDB is running
mongod
```

### 2. Setup Backend
```bash
cd backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start server
python start_server.py
```

Backend will run on: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

### 3. Setup Frontend
```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Start development server
npm start
```

Frontend will run on: **http://localhost:3000**

---

## 🧪 Test the System

### Login Credentials

#### **Student Account**
```
Email: student@example.com
Password: student123
```

#### **Teacher/Expert Account**
```
Email: john.expert@example.com
Password: expert123
```

#### **Other Experts**
- sarah.expert@example.com / expert123
- michael.expert@example.com / expert123
- emily.expert@example.com / expert123
- david.expert@example.com / expert123

---

## ✅ Test Checklist

### **As Student:**
1. [ ] Login → View Dashboard
2. [ ] Check "Expert Matches" sidebar (ML-powered)
3. [ ] Go to Matches page → See expert profiles
4. [ ] Click "Request Meeting" on an expert
5. [ ] Go to Resources → Browse and download
6. [ ] Go to Study Groups → Join a group
7. [ ] Create a post on dashboard
8. [ ] Like/comment on posts

### **As Teacher/Expert:**
1. [ ] Login → View Teacher Dashboard
2. [ ] See "Pending Meetings" tab
3. [ ] Approve a meeting → Enter Google Meet link
4. [ ] Go to "My Resources" tab
5. [ ] Click "Upload New Resource"
6. [ ] Upload a file or add external URL
7. [ ] View resource stats (views, downloads, likes)
8. [ ] Delete a resource

---

## 🎯 Key Features to Test

### 1. **Expert Matching (Students)**
- Dashboard shows top 5 matched experts
- Matches page shows detailed expert profiles
- Match scores displayed (0-100%)
- Shared interests highlighted

### 2. **Meeting Scheduling**
- Student requests meeting with topic/description
- Teacher sees request in dashboard
- Teacher approves with Google Meet link
- Student receives notification (future enhancement)

### 3. **Resource Management**
- Teachers upload files (stored in MongoDB GridFS)
- Or add external URLs
- Students browse by category/difficulty
- Download files
- Like resources
- Track views/downloads

### 4. **Study Groups**
- Browse existing groups
- Join groups
- Create new groups
- See member count

### 5. **Social Feed**
- Create posts
- Like posts
- Add comments
- Delete own posts

---

## 📊 API Testing

### Test with cURL or Postman

#### 1. **Login**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student@example.com&password=student123"
```

#### 2. **Get Expert Matches** (Student)
```bash
curl -X GET http://localhost:8000/matches/expert-matches \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 3. **Request Meeting** (Student)
```bash
curl -X POST http://localhost:8000/meetings/request \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "teacher_id": "TEACHER_ID",
    "title": "Doubt Clarification",
    "description": "Need help with ML concepts",
    "topic": "Machine Learning",
    "duration_minutes": 30
  }'
```

#### 4. **Get Pending Meetings** (Teacher)
```bash
curl -X GET http://localhost:8000/meetings/pending \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 5. **Approve Meeting** (Teacher)
```bash
curl -X POST http://localhost:8000/meetings/MEETING_ID/approve \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scheduled_date": "2025-01-20T15:00:00",
    "google_meet_link": "https://meet.google.com/abc-defg-hij",
    "teacher_notes": "Looking forward to our session!"
  }'
```

#### 6. **Get Resources**
```bash
curl -X GET http://localhost:8000/resources/?category=Python \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 7. **Upload Resource** (Teacher)
```bash
curl -X POST http://localhost:8000/resources/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "title=Python Basics" \
  -F "description=Introduction to Python programming" \
  -F "category=Python" \
  -F "resource_type=pdf" \
  -F "tags=python,programming,beginner" \
  -F "difficulty_level=beginner" \
  -F "file=@/path/to/file.pdf"
```

---

## 🐛 Troubleshooting

### Backend Issues

#### MongoDB Connection Error
```
Error: MongoDB connection failed
```
**Solution:** Make sure MongoDB is running:
```bash
mongod
```

#### Port Already in Use
```
Error: Address already in use (8000)
```
**Solution:** Kill the existing process:
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 PID
```

### Frontend Issues

#### Axios Network Error
```
Error: Network Error
```
**Solution:** Check backend is running on port 8000

#### Page Not Found (404)
```
Failed to load resource: 404
```
**Solution:** Check route is registered in:
- `backend/app/routes/__init__.py`
- `backend/app/main.py`

---

## 📱 Demo Data

If you need to recreate demo users:

```bash
cd database
python create_demo_users.py
python create_demo_experts.py
```

This creates:
- 1 student (student@example.com)
- 5 experts (john.expert@example.com, sarah.expert@example.com, etc.)

---

## 🔄 Reset Database (if needed)

```bash
# Connect to MongoDB
mongosh

# Switch to database
use intelligent_matchmaking

# Drop collections
db.resources.drop()
db.meetings.drop()
db.chat_messages.drop()
db.conversations.drop()
db.notifications.drop()

# Recreate demo data
exit
python database/create_demo_users.py
python database/create_demo_experts.py
```

---

## 📚 Documentation

- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Implementation Guide:** IMPLEMENTATION-COMPLETE.md
- **Production Deployment:** docs/PRODUCTION_DEPLOYMENT.md
- **Expert Matching:** docs/EXPERT_MATCHING_GUIDE.md

---

## 🎉 You're Ready!

Your intelligent matchmaking system is fully functional. Test all features and enjoy! 🚀

**Need help?** Check the API docs or implementation guide.
