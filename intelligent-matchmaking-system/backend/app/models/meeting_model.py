"""
Meeting Model - For teacher-created events and student registration
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


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
    """Meeting/Event created by teachers for student participation"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    # Basic meeting info
    title: str = Field(..., min_length=1, max_length=200, description="Meeting title")
    description: Optional[str] = Field(default="", max_length=1000, description="Meeting description")
    
    # Meeting creator and details
    teacher_id: PyObjectId = Field(..., description="Teacher who created the meeting")
    teacher_name: str = Field(..., description="Teacher's name")
    teacher_email: str = Field(..., description="Teacher's email")
    
    subject: str = Field(..., description="Subject/topic of the meeting")
    category: str = Field(..., description="Meeting category (lecture, workshop, discussion, etc.)")
    
    # Scheduling
    scheduled_date: datetime = Field(..., description="When the meeting is scheduled")
    duration_minutes: int = Field(default=60, ge=15, le=480, description="Meeting duration in minutes")
    timezone: str = Field(default="UTC", description="Timezone for the meeting")
    
    # Meeting platform details
    meeting_platform: str = Field(default="google_meet", description="Platform (google_meet, zoom, teams)")
    meeting_link: Optional[str] = Field(default=None, description="Meeting URL/link")
    meeting_id: Optional[str] = Field(default=None, description="Platform-specific meeting ID")
    passcode: Optional[str] = Field(default=None, description="Meeting passcode if required")
    
    # Participants
    max_participants: int = Field(default=50, ge=1, le=500, description="Maximum number of participants")
    registered_students: List[PyObjectId] = Field(default_factory=list, description="List of registered student IDs")
    attendees: List[PyObjectId] = Field(default_factory=list, description="List of student IDs who attended")
    
    # Meeting settings
    is_recurring: bool = Field(default=False, description="Is this a recurring meeting")
    recurrence_pattern: Optional[Dict[str, Any]] = Field(default=None, description="Recurrence pattern if recurring")
    is_recorded: bool = Field(default=False, description="Will the meeting be recorded")
    recording_url: Optional[str] = Field(default=None, description="URL to the recording")
    
    # Status and metadata
    status: str = Field(default="scheduled", description="Meeting status: scheduled, ongoing, completed, cancelled")
    is_active: bool = Field(default=True, description="Is the meeting active/visible")
    is_public: bool = Field(default=True, description="Can all students see and join this meeting")
    
    # Requirements and preparation
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites for the meeting")
    materials_needed: List[str] = Field(default_factory=list, description="Materials students should prepare")
    agenda: List[str] = Field(default_factory=list, description="Meeting agenda items")
    
    # Tags and searchability
    tags: List[str] = Field(default_factory=list, description="Tags for categorization and search")
    difficulty_level: str = Field(default="intermediate", description="Difficulty: beginner, intermediate, advanced")
    
    # Engagement and feedback
    likes: List[PyObjectId] = Field(default_factory=list, description="List of user IDs who liked the meeting")
    rating: float = Field(default=0.0, ge=0, le=5, description="Average rating from participants")
    feedback_count: int = Field(default=0, description="Number of feedback submissions")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Discussion group and resources
    discussion_group_id: Optional[PyObjectId] = Field(default=None, description="ID of associated discussion group")
    resources: List[PyObjectId] = Field(default_factory=list, description="List of resource IDs linked to this meeting")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class MeetingRegistration(BaseModel):
    """Model for student registration to meetings"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    meeting_id: PyObjectId = Field(..., description="Meeting ID")
    student_id: PyObjectId = Field(..., description="Student ID")
    student_name: str = Field(..., description="Student name")
    student_email: str = Field(..., description="Student email")
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="registered", description="registered, attended, no-show")
    notes: Optional[str] = Field(default="", description="Student's notes or questions")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class MeetingFeedback(BaseModel):
    """Model for meeting feedback from participants"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    meeting_id: PyObjectId = Field(..., description="Meeting ID")
    participant_id: PyObjectId = Field(..., description="Participant (student) ID")
    participant_name: str = Field(..., description="Participant name")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    feedback_text: Optional[str] = Field(default="", max_length=1000, description="Written feedback")
    areas_liked: List[str] = Field(default_factory=list, description="What they liked")
    areas_for_improvement: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    would_recommend: bool = Field(default=True, description="Would recommend to others")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
