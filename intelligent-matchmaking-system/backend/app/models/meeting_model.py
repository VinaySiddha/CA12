"""
Meeting Model - For scheduling meetings between students and teachers/experts
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2"""
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.no_info_plain_validator_function(cls.validate),
        ])

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


class Meeting(BaseModel):
    """Meeting request between student and teacher/expert"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    # Participants
    student_id: PyObjectId = Field(..., description="Student user ID")
    student_name: str = Field(..., description="Student name")
    student_email: str = Field(..., description="Student email")
    
    teacher_id: PyObjectId = Field(..., description="Teacher/Expert user ID")
    teacher_name: str = Field(..., description="Teacher/Expert name")
    teacher_email: str = Field(..., description="Teacher/Expert email")
    
    # Meeting details
    title: str = Field(..., description="Meeting title/subject")
    description: str = Field(..., description="Purpose of meeting")
    topic: str = Field(..., description="Topic to discuss")
    
    # Scheduling
    preferred_date: Optional[datetime] = Field(None, description="Student's preferred date/time")
    scheduled_date: Optional[datetime] = Field(None, description="Confirmed meeting date/time")
    duration_minutes: int = Field(default=30, description="Meeting duration in minutes")
    
    # Status
    status: str = Field(
        default="pending",
        description="Meeting status (pending/approved/rejected/completed/cancelled)"
    )
    
    # Google Meet integration
    google_meet_link: Optional[str] = Field(None, description="Google Meet URL")
    meeting_id: Optional[str] = Field(None, description="Meeting platform ID")
    
    # Additional info
    teacher_notes: Optional[str] = Field(None, description="Teacher's notes about the meeting")
    student_notes: Optional[str] = Field(None, description="Student's notes after meeting")
    
    # Timestamps
    requested_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(None)
    
    # Notification flags
    student_notified: bool = Field(default=False)
    teacher_notified: bool = Field(default=True, description="Teacher gets notification on creation")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class MeetingFeedback(BaseModel):
    """Feedback after meeting completion"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    meeting_id: PyObjectId = Field(..., description="Meeting ID")
    
    # Feedback from student
    student_rating: Optional[int] = Field(None, ge=1, le=5, description="Student rating (1-5)")
    student_feedback: Optional[str] = Field(None, description="Student's feedback text")
    
    # Feedback from teacher
    teacher_rating: Optional[int] = Field(None, ge=1, le=5, description="Teacher rating (1-5)")
    teacher_feedback: Optional[str] = Field(None, description="Teacher's feedback text")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
