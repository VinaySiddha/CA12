"""
Feedback data model
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List
from datetime import datetime
from bson import ObjectId
from .user_model import PyObjectId


class SessionFeedback(BaseModel):
    session_id: PyObjectId
    helpfulness_rating: int = Field(..., ge=1, le=5)  # 1-5 scale
    engagement_rating: int = Field(..., ge=1, le=5)
    clarity_rating: int = Field(..., ge=1, le=5)
    overall_rating: int = Field(..., ge=1, le=5)
    
    # Qualitative feedback
    what_went_well: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    additional_comments: Optional[str] = None
    
    # Learning outcomes
    learning_objectives_met: bool = False
    topics_mastered: List[str] = []
    topics_need_more_work: List[str] = []


class FeedbackModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    # Feedback context
    feedback_type: str  # "session", "match", "peer", "system"
    reviewer_id: PyObjectId
    reviewee_id: Optional[PyObjectId] = None  # For peer feedback
    match_id: Optional[PyObjectId] = None
    
    # Session-specific feedback
    session_feedback: Optional[SessionFeedback] = None
    
    # General feedback
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    
    # System feedback (for ML improvement)
    recommendation_accuracy: Optional[int] = None  # 1-5 scale
    system_suggestions: Optional[List[str]] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_anonymous: bool = False
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class LearningOutcome(BaseModel):
    user_id: PyObjectId
    topic: str
    skill_level_before: int = Field(..., ge=1, le=10)
    skill_level_after: int = Field(..., ge=1, le=10)
    confidence_before: int = Field(..., ge=1, le=10)
    confidence_after: int = Field(..., ge=1, le=10)
    session_count: int
    total_study_time: int  # in minutes
    assessment_date: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}