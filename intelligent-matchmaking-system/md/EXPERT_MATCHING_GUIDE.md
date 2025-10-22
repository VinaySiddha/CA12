# Expert Matching ML Model - Implementation Guide

## 🎯 Overview

The system has been updated from a **student-teacher matching model** to a **student-expert/professional matching model**. The ML recommendation algorithm now intelligently matches students with industry experts and professionals based on:

- **Interest Overlap** (40% weight) - Student interests vs Expert expertise
- **Text Similarity** (30% weight) - TF-IDF cosine similarity
- **Field Alignment** (20% weight) - Academic field compatibility
- **Experience Compatibility** (10% weight) - Expert experience level suitability

## 🏗️ Architecture

### 1. **Expert Matching Model** (`ml/expert_matching_model.py`)
   - Uses TF-IDF vectorization for text analysis
   - Implements multi-factor scoring algorithm
   - Provides match explanations and recommendations
   - Jaccard similarity for interest overlap calculation

### 2. **ML Service** (`ml/ml_service.py`)
   - Integrates expert matching model
   - Handles model training and inference
   - Provides async API for match finding

### 3. **Matchmaking Service** (`backend/app/services/matchmaking_service.py`)
   - Coordinates with ML Service
   - Fetches expert/professional users from database
   - Formats results for API responses

### 4. **API Endpoints** (`backend/app/routes/match_routes.py`)
   - `GET /matches/expert-matches` - Find expert matches for students

## 📊 ML Matching Algorithm

### Scoring Components

```python
final_score = (
    0.40 * interest_overlap_score +    # Shared interests/expertise
    0.30 * text_similarity_score +     # TF-IDF similarity
    0.20 * field_alignment_score +     # Field compatibility
    0.10 * experience_compatibility    # Experience level
)
```

### Interest Overlap Score
- Calculates Jaccard similarity between:
  - Student interests + weaknesses (learning needs)
  - Expert expertise + interests + strengths (teaching capabilities)
- Range: 0.0 to 1.0

### Text Similarity Score
- Combines all text from profiles into documents
- Uses TF-IDF vectorization
- Calculates cosine similarity
- Range: 0.0 to 1.0

### Field Alignment Score
- Exact match: 1.0
- Partial match: 0.8
- Related fields: 0.6
- No match: 0.3

### Experience Compatibility
- Maps academic levels to preferred experience ranges:
  - Undergraduate: 0-5 years (1.0)
  - Graduate: 2-10 years (1.0)
  - PhD: 5-20 years (1.0)
  - Outside range: 0.7-0.9

## 🚀 Setup Instructions

### 1. Create Demo Expert Users

```bash
cd database
python create_demo_experts.py
```

This creates 5 demo experts:
- **Dr. John Smith** - ML Engineer (Machine Learning, AI, Python)
- **Sarah Johnson** - Full Stack Developer (React, Node.js, Web Dev)
- **Michael Chen** - Data Scientist (Data Analysis, Statistics, Python)
- **Emily Rodriguez** - UX Designer (UX Design, Figma, User Research)
- **David Williams** - Cloud Architect (AWS, DevOps, Docker, Kubernetes)

Login credentials: `expert_email@example.com` / `expert123`

### 2. Update Student Profile

```bash
cd database
python create_demo_users.py
```

This updates the demo student with:
- Interests: Machine Learning, Web Development, Python, React, Data Science
- Weaknesses: Machine Learning, Data Science, Cloud Computing
- Expertise level in JavaScript, HTML, CSS, Python

### 3. Start Backend Server

```bash
cd backend
python start_server.py
```

### 4. Start Frontend

```bash
cd frontend
npm start
```

## 📱 Usage

### For Students

1. **Login** as student (`student@example.com` / `student123`)
2. **Dashboard** automatically shows expert matches in sidebar
3. **Expert cards show**:
   - Expert name and job title
   - Company
   - Match score (0-100%)
   - Expertise areas
   - Shared interests count
   - Score breakdown (hover/click for details)

### For Experts/Professionals

1. **Login** with expert credentials
2. Profile shows expertise areas and years of experience
3. Can post and interact on social feed
4. Students will see them in recommendations if interests align

## 🔧 API Reference

### Get Expert Matches

```http
GET /matches/expert-matches?limit=10
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": "expert_id_123",
    "full_name": "Dr. John Smith",
    "role": "expert",
    "job_title": "Senior ML Engineer",
    "company": "Tech Corp",
    "expertise_areas": ["Machine Learning", "AI", "Python"],
    "years_experience": 10,
    "match_score": 0.85,
    "score_breakdown": {
      "interest_overlap": 0.8,
      "text_similarity": 0.9,
      "field_alignment": 0.9,
      "experience_compatibility": 1.0
    },
    "matched_interests": ["Machine Learning", "Python"],
    "explanation": {
      "match_quality": "Excellent",
      "common_interests": ["Machine Learning", "Python"],
      "expert_strengths": ["Machine Learning", "Deep Learning"],
      "field_compatibility": "High",
      "experience_level": "10 years",
      "recommendation_reason": "Excellent match! You share 2 key interests..."
    }
  }
]
```

## 🎨 Frontend Components

### Dashboard Expert Matches Section

Located in: `frontend/src/pages/Dashboard-new.js`

Features:
- **Match score visualization** with percentage
- **Expert profile cards** with avatar
- **Expertise tags** (showing top 3)
- **Shared interests indicator** with count
- **View Profile button** for each expert
- **Responsive design** for mobile/desktop

## 📚 Database Schema

### User Model Updates

New fields added to `UserModel`:

```python
# Expert/Professional-specific fields
expertise_areas: List[str] = []
years_experience: Optional[int] = None
company: Optional[str] = None
job_title: Optional[str] = None
linkedin_url: Optional[str] = None
portfolio_url: Optional[str] = None
```

Role options updated:
- `"student"` - Students seeking mentorship
- `"expert"` - Industry experts
- `"professional"` - Working professionals
- `"admin"` - System administrators

## 🧪 Testing

### Manual Testing Steps

1. **Create test data**:
   ```bash
   python database/create_demo_users.py
   python database/create_demo_experts.py
   ```

2. **Login as student** and verify:
   - Dashboard loads without errors
   - Expert matches appear in sidebar
   - Match scores are calculated correctly
   - Expertise areas are displayed

3. **Test API directly**:
   ```bash
   # Get auth token
   curl -X POST http://localhost:8000/auth/login \
     -d "username=student@example.com&password=student123"
   
   # Get expert matches
   curl -X GET http://localhost:8000/matches/expert-matches?limit=5 \
     -H "Authorization: Bearer <token>"
   ```

### Expected Results

- Student with interests in "Machine Learning" should match highly with Dr. John Smith
- Student interested in "Web Development" should match with Sarah Johnson
- Match scores should be between 0.0 and 1.0
- Shared interests should be accurately identified

## 🐛 Troubleshooting

### Issue: No expert matches found

**Solution:**
- Ensure demo experts are created: `python database/create_demo_experts.py`
- Check MongoDB connection
- Verify student has interests/skills defined in profile

### Issue: Match scores are all 0

**Solution:**
- Update student profile with interests
- Ensure experts have expertise_areas populated
- Check that ML model is trained (first request trains it)

### Issue: 403 Forbidden on /expert-matches

**Solution:**
- Only students can access this endpoint
- Verify user role in token
- Check authentication token is valid

## 🔮 Future Enhancements

1. **Real-time Matching** - WebSocket updates when new experts join
2. **Booking System** - Schedule 1-on-1 sessions with experts
3. **Rating System** - Rate experts after interactions
4. **Advanced Filters** - Filter by experience, company, location
5. **Recommendation Explanations** - Detailed breakdown in UI
6. **Expert Availability** - Show real-time availability calendar
7. **Messaging System** - Direct chat with matched experts

## 📝 Configuration

### Adjust Match Scoring Weights

Edit `ml/expert_matching_model.py`:

```python
# Line ~230
final_score = (
    0.40 * interest_score +      # Adjust these weights
    0.30 * text_score +
    0.20 * field_score +
    0.10 * experience_score
)
```

### Change Number of Recommendations

Frontend: `frontend/src/pages/Dashboard-new.js`
```javascript
axios.get('/matches/expert-matches?limit=5')  // Change limit
```

Backend default: `backend/app/routes/match_routes.py`
```python
limit: int = Query(10, ge=1, le=20)  // Change default
```

## ✅ Verification Checklist

- [ ] Demo experts created in database
- [ ] Student profile has interests defined
- [ ] Backend server running without errors
- [ ] Frontend displays expert matches
- [ ] Match scores are reasonable (0.3-0.9 range)
- [ ] Shared interests correctly identified
- [ ] Expert profiles show job title and company
- [ ] API endpoint returns proper JSON structure

---

**Implementation Status:** ✅ Complete

**Last Updated:** October 14, 2025

**Version:** 2.0 - Expert Matching System
