"""
Match schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class MatchScoreResponse(BaseModel):
    overall_score: float
    skill_compatibility: float
    schedule_compatibility: float
    learning_style_compatibility: float
    topic_relevance: float


class StudySessionCreate(BaseModel):
    scheduled_time: datetime
    duration_minutes: int = 60
    topic: str
    location: Optional[str] = "online"
    notes: Optional[str] = None


class StudySessionResponse(BaseModel):
    session_id: str
    scheduled_time: datetime
    duration_minutes: int
    topic: str
    location: Optional[str] = None
    status: str
    notes: Optional[str] = None


class MatchCreate(BaseModel):
    mentee_id: str
    topics: List[str]
    match_type: str = "mentor_mentee"
    session_duration_preference: int = 60
    max_sessions: int = 10


class MatchResponse(BaseModel):
    id: str
    mentor_id: str
    mentee_id: str
    match_type: str
    topics: List[str]
    match_score: MatchScoreResponse
    status: str
    created_at: datetime
    accepted_at: Optional[datetime] = None
    sessions: List[StudySessionResponse] = []


class MatchRequest(BaseModel):
    topics: List[str]
    preferred_learning_style: Optional[str] = None
    preferred_schedule: Optional[Dict[str, List[str]]] = None
    match_type: str = "mentor_mentee"


class StudyGroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    topic: str
    max_members: int = 6
    meeting_schedule: Optional[Dict] = None
    meeting_location: str = "online"


class StudyGroupResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    topic: str
    max_members: int
    member_count: int
    creator_id: str
    status: str
    created_at: datetime
    meeting_schedule: Optional[Dict] = None
    meeting_location: str


class StudyGroupJoinRequest(BaseModel):
    message: Optional[str] = None