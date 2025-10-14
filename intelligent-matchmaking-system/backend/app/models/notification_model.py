"""
Notification Model - For user notifications
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
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


class Notification(BaseModel):
    """User notification"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    # Recipient
    user_id: PyObjectId = Field(..., description="Recipient user ID")
    
    # Notification details
    notification_type: str = Field(
        ...,
        description="Type: meeting_request/meeting_approved/meeting_rejected/new_message/new_resource/study_group_invite"
    )
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message")
    
    # Related entity
    related_id: Optional[PyObjectId] = Field(None, description="Related entity ID (meeting, message, resource)")
    related_type: Optional[str] = Field(None, description="Related entity type")
    
    # Action link
    action_url: Optional[str] = Field(None, description="URL to navigate when clicked")
    
    # Sender info (optional)
    sender_id: Optional[PyObjectId] = Field(None, description="Sender user ID")
    sender_name: Optional[str] = Field(None, description="Sender name")
    
    # Status
    is_read: bool = Field(default=False, description="Whether notification has been read")
    read_at: Optional[datetime] = Field(None, description="When notification was read")
    
    # Additional data
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional data")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
