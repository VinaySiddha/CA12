"""
Feedback schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SessionFeedbackCreate(BaseModel):
    session_id: str
    helpfulness_rating: int = Field(..., ge=1, le=5)
    engagement_rating: int = Field(..., ge=1, le=5)
    clarity_rating: int = Field(..., ge=1, le=5)
    overall_rating: int = Field(..., ge=1, le=5)
    what_went_well: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    additional_comments: Optional[str] = None
    learning_objectives_met: bool = False
    topics_mastered: List[str] = []
    topics_need_more_work: List[str] = []


class FeedbackCreate(BaseModel):
    feedback_type: str
    reviewee_id: Optional[str] = None
    match_id: Optional[str] = None
    session_feedback: Optional[SessionFeedbackCreate] = None
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    recommendation_accuracy: Optional[int] = Field(None, ge=1, le=5)
    system_suggestions: Optional[List[str]] = None
    is_anonymous: bool = False


class FeedbackResponse(BaseModel):
    id: str
    feedback_type: str
    reviewer_id: str
    reviewee_id: Optional[str] = None
    match_id: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    is_anonymous: bool


class LearningOutcomeCreate(BaseModel):
    topic: str
    skill_level_before: int = Field(..., ge=1, le=10)
    skill_level_after: int = Field(..., ge=1, le=10)
    confidence_before: int = Field(..., ge=1, le=10)
    confidence_after: int = Field(..., ge=1, le=10)
    session_count: int
    total_study_time: int


class LearningOutcomeResponse(BaseModel):
    user_id: str
    topic: str
    skill_level_before: int
    skill_level_after: int
    confidence_before: int
    confidence_after: int
    improvement_score: float
    session_count: int
    total_study_time: int
    assessment_date: datetime