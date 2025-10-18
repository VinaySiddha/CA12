"""
Meeting schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class MeetingCreate(BaseModel):
    """Schema for creating a new meeting/event"""
    title: str = Field(..., min_length=1, max_length=200, description="Meeting title")
    description: Optional[str] = Field(default="", max_length=1000, description="Meeting description")
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
    
    # Meeting settings
    is_recurring: bool = Field(default=False, description="Is this a recurring meeting")
    recurrence_pattern: Optional[Dict[str, Any]] = Field(default=None, description="Recurrence pattern if recurring")
    is_recorded: bool = Field(default=False, description="Will the meeting be recorded")
    is_public: bool = Field(default=True, description="Can all students see and join this meeting")
    
    # Requirements and preparation
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites for the meeting")
    materials_needed: List[str] = Field(default_factory=list, description="Materials students should prepare")
    agenda: List[str] = Field(default_factory=list, description="Meeting agenda items")
    
    # Tags and searchability
    tags: List[str] = Field(default_factory=list, description="Tags for categorization and search")
    difficulty_level: str = Field(default="intermediate", description="Difficulty: beginner, intermediate, advanced")


class MeetingUpdate(BaseModel):
    """Schema for updating meeting details"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Meeting title")
    description: Optional[str] = Field(None, max_length=1000, description="Meeting description")
    subject: Optional[str] = Field(None, description="Subject/topic of the meeting")
    category: Optional[str] = Field(None, description="Meeting category")
    
    # Scheduling
    scheduled_date: Optional[datetime] = Field(None, description="When the meeting is scheduled")
    duration_minutes: Optional[int] = Field(None, ge=15, le=480, description="Meeting duration in minutes")
    timezone: Optional[str] = Field(None, description="Timezone for the meeting")
    
    # Meeting platform details
    meeting_platform: Optional[str] = Field(None, description="Platform (google_meet, zoom, teams)")
    meeting_link: Optional[str] = Field(None, description="Meeting URL/link")
    meeting_id: Optional[str] = Field(None, description="Platform-specific meeting ID")
    passcode: Optional[str] = Field(None, description="Meeting passcode if required")
    
    # Participants
    max_participants: Optional[int] = Field(None, ge=1, le=500, description="Maximum number of participants")
    
    # Meeting settings
    is_recurring: Optional[bool] = Field(None, description="Is this a recurring meeting")
    recurrence_pattern: Optional[Dict[str, Any]] = Field(None, description="Recurrence pattern if recurring")
    is_recorded: Optional[bool] = Field(None, description="Will the meeting be recorded")
    recording_url: Optional[str] = Field(None, description="URL to the recording")
    is_public: Optional[bool] = Field(None, description="Can all students see and join this meeting")
    status: Optional[str] = Field(None, description="Meeting status")
    
    # Requirements and preparation
    prerequisites: Optional[List[str]] = Field(None, description="Prerequisites for the meeting")
    materials_needed: Optional[List[str]] = Field(None, description="Materials students should prepare")
    agenda: Optional[List[str]] = Field(None, description="Meeting agenda items")
    
    # Tags and searchability
    tags: Optional[List[str]] = Field(None, description="Tags for categorization and search")
    difficulty_level: Optional[str] = Field(None, description="Difficulty: beginner, intermediate, advanced")


class MeetingResponse(BaseModel):
    """Schema for meeting response"""
    id: str = Field(..., description="Meeting ID")
    title: str = Field(..., description="Meeting title")
    description: Optional[str] = Field(default="", description="Meeting description")
    
    # Meeting creator and details
    teacher_id: str = Field(..., description="Teacher who created the meeting")
    teacher_name: str = Field(..., description="Teacher's name")
    teacher_email: str = Field(..., description="Teacher's email")
    
    subject: str = Field(..., description="Subject/topic of the meeting")
    category: str = Field(..., description="Meeting category")
    
    # Scheduling
    scheduled_date: datetime = Field(..., description="When the meeting is scheduled")
    duration_minutes: int = Field(..., description="Meeting duration in minutes")
    timezone: str = Field(..., description="Timezone for the meeting")
    
    # Meeting platform details
    meeting_platform: str = Field(..., description="Platform")
    meeting_link: Optional[str] = Field(default=None, description="Meeting URL/link")
    meeting_id: Optional[str] = Field(default=None, description="Platform-specific meeting ID")
    passcode: Optional[str] = Field(default=None, description="Meeting passcode if required")
    
    # Participants
    max_participants: int = Field(..., description="Maximum number of participants")
    registered_count: int = Field(..., description="Number of registered students")
    attendees_count: int = Field(..., description="Number of attendees")
    
    # Meeting settings
    is_recurring: bool = Field(..., description="Is this a recurring meeting")
    is_recorded: bool = Field(..., description="Will the meeting be recorded")
    recording_url: Optional[str] = Field(default=None, description="URL to the recording")
    
    # Status and metadata
    status: str = Field(..., description="Meeting status")
    is_active: bool = Field(..., description="Is the meeting active/visible")
    is_public: bool = Field(..., description="Can all students see and join this meeting")
    
    # Requirements and preparation
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites for the meeting")
    materials_needed: List[str] = Field(default_factory=list, description="Materials students should prepare")
    agenda: List[str] = Field(default_factory=list, description="Meeting agenda items")
    
    # Tags and searchability
    tags: List[str] = Field(default_factory=list, description="Tags for categorization and search")
    difficulty_level: str = Field(..., description="Difficulty level")
    
    # Engagement and feedback
    likes_count: int = Field(..., description="Number of likes")
    rating: float = Field(..., description="Average rating from participants")
    feedback_count: int = Field(..., description="Number of feedback submissions")
    
    # User-specific info (filled when user is known)
    is_registered: Optional[bool] = Field(default=None, description="Is current user registered")
    is_liked: Optional[bool] = Field(default=None, description="Has current user liked this meeting")
    
    # Timestamps
    created_at: datetime = Field(..., description="When meeting was created")
    updated_at: datetime = Field(..., description="When meeting was last updated")
    
    # Discussion group
    discussion_group_id: Optional[str] = Field(default=None, description="ID of associated discussion group")


class MeetingRegistrationRequest(BaseModel):
    """Schema for student registration request"""
    notes: Optional[str] = Field(default="", max_length=500, description="Student's notes or questions")


class MeetingFeedbackCreate(BaseModel):
    """Schema for creating meeting feedback"""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    feedback_text: Optional[str] = Field(default="", max_length=1000, description="Written feedback")
    areas_liked: List[str] = Field(default_factory=list, description="What they liked")
    areas_for_improvement: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    would_recommend: bool = Field(default=True, description="Would recommend to others")


class MeetingFeedbackResponse(BaseModel):
    """Schema for meeting feedback response"""
    id: str = Field(..., description="Feedback ID")
    meeting_id: str = Field(..., description="Meeting ID")
    participant_id: str = Field(..., description="Participant ID")
    participant_name: str = Field(..., description="Participant name")
    rating: int = Field(..., description="Rating from 1-5")
    feedback_text: str = Field(..., description="Written feedback")
    areas_liked: List[str] = Field(..., description="What they liked")
    areas_for_improvement: List[str] = Field(..., description="Suggestions for improvement")
    would_recommend: bool = Field(..., description="Would recommend to others")
    created_at: datetime = Field(..., description="When feedback was created")


class MeetingListResponse(BaseModel):
    """Schema for meeting list with pagination"""
    meetings: List[MeetingResponse] = Field(..., description="List of meetings")
    total_count: int = Field(..., description="Total number of meetings")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")


class MeetingSearchQuery(BaseModel):
    """Schema for meeting search parameters"""
    search: Optional[str] = Field(None, description="Search term for title, description, or tags")
    subject: Optional[str] = Field(None, description="Filter by subject")
    category: Optional[str] = Field(None, description="Filter by category")
    teacher_id: Optional[str] = Field(None, description="Filter by teacher ID")
    difficulty_level: Optional[str] = Field(None, description="Filter by difficulty level")
    status: Optional[str] = Field(None, description="Filter by status")
    date_from: Optional[datetime] = Field(None, description="Filter meetings from this date")
    date_to: Optional[datetime] = Field(None, description="Filter meetings to this date")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    is_public: Optional[bool] = Field(None, description="Filter by public/private")
    has_recording: Optional[bool] = Field(None, description="Filter meetings with recordings")
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(20, ge=1, le=100, description="Items per page")
    sort_by: str = Field("scheduled_date", description="Sort field")
    sort_order: str = Field("asc", description="Sort order (asc/desc)")