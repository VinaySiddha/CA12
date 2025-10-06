"""
Match data model
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from .user_model import PyObjectId


class MatchScore(BaseModel):
    overall_score: float = Field(..., ge=0, le=1)  # 0-1 compatibility score
    skill_compatibility: float = Field(..., ge=0, le=1)
    schedule_compatibility: float = Field(..., ge=0, le=1)
    learning_style_compatibility: float = Field(..., ge=0, le=1)
    topic_relevance: float = Field(..., ge=0, le=1)


class StudySession(BaseModel):
    session_id: PyObjectId = Field(default_factory=PyObjectId)
    scheduled_time: datetime
    duration_minutes: int
    topic: str
    location: Optional[str] = None  # "online", "library", etc.
    status: str = "scheduled"  # "scheduled", "completed", "cancelled"
    notes: Optional[str] = None


class MatchModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    # Match participants
    mentor_id: PyObjectId
    mentee_id: PyObjectId
    
    # Match details
    match_type: str  # "peer", "mentor_mentee", "study_group"
    topics: List[str]  # Common topics of interest
    match_score: MatchScore
    
    # Match status
    status: str = "pending"  # "pending", "accepted", "declined", "active", "completed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Study sessions
    sessions: List[StudySession] = []
    
    # Match settings
    max_sessions: int = 10
    session_duration_preference: int = 60  # minutes
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class StudyGroupModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    # Group details
    name: str
    description: Optional[str] = None
    topic: str
    max_members: int = 6
    member_ids: List[PyObjectId] = []
    creator_id: PyObjectId
    
    # Group status
    status: str = "active"  # "active", "full", "disbanded"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Meeting information
    meeting_schedule: Optional[Dict] = None  # {"day": "monday", "time": "14:00", "duration": 120}
    meeting_location: str = "online"
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )