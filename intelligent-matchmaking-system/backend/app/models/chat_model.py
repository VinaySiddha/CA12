"""
Chat Model - For messaging between students and teachers/experts
"""
from pydantic import BaseModel, Field
from typing import Optional, List
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


class ChatMessage(BaseModel):
    """Individual chat message"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    conversation_id: PyObjectId = Field(..., description="Conversation ID")
    
    # Sender info
    sender_id: PyObjectId = Field(..., description="Sender user ID")
    sender_name: str = Field(..., description="Sender name")
    sender_role: str = Field(..., description="Sender role (student/teacher/expert)")
    
    # Message content
    content: str = Field(..., description="Message text")
    message_type: str = Field(default="text", description="Message type (text/image/file)")
    
    # File attachment (optional)
    attachment_url: Optional[str] = Field(None, description="Attachment URL if any")
    attachment_name: Optional[str] = Field(None, description="Attachment filename")
    
    # Status
    is_read: bool = Field(default=False, description="Whether message has been read")
    read_at: Optional[datetime] = Field(None, description="When message was read")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    edited_at: Optional[datetime] = Field(None)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class Conversation(BaseModel):
    """Conversation between student and teacher/expert"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    # Participants
    student_id: PyObjectId = Field(..., description="Student user ID")
    student_name: str = Field(..., description="Student name")
    
    teacher_id: PyObjectId = Field(..., description="Teacher/Expert user ID")
    teacher_name: str = Field(..., description="Teacher/Expert name")
    
    # Participants list (for queries)
    participant_ids: List[PyObjectId] = Field(..., description="List of participant IDs")
    
    # Conversation metadata
    title: Optional[str] = Field(None, description="Conversation title/subject")
    last_message: Optional[str] = Field(None, description="Last message preview")
    last_message_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Status
    is_active: bool = Field(default=True, description="Whether conversation is active")
    is_archived: bool = Field(default=False, description="Whether archived")
    
    # Unread counts
    student_unread_count: int = Field(default=0)
    teacher_unread_count: int = Field(default=0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
