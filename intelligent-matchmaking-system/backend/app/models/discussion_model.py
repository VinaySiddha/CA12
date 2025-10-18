"""
Discussion Group Model for meeting-based conversations
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


class DiscussionGroup(BaseModel):
    """Discussion group linked to meetings"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    # Linked meeting
    meeting_id: PyObjectId = Field(..., description="Associated meeting ID")
    meeting_title: str = Field(..., description="Meeting title for reference")
    
    # Group details
    title: str = Field(..., description="Discussion group title")
    description: Optional[str] = Field(default="", description="Group description")
    
    # Participants
    moderator_id: PyObjectId = Field(..., description="Teacher/moderator ID")
    moderator_name: str = Field(..., description="Teacher/moderator name")
    participants: List[PyObjectId] = Field(default_factory=list, description="List of participant IDs")
    
    # Group settings
    is_active: bool = Field(default=True, description="Is the group active")
    is_open: bool = Field(default=True, description="Can new participants join")
    auto_add_registered: bool = Field(default=True, description="Auto-add meeting registrants")
    
    # Message count and activity
    message_count: int = Field(default=0, description="Total number of messages")
    last_activity: Optional[datetime] = Field(default=None, description="Last message timestamp")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class DiscussionMessage(BaseModel):
    """Messages in discussion groups"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    # Group association
    discussion_group_id: PyObjectId = Field(..., description="Discussion group ID")
    
    # Message details
    sender_id: PyObjectId = Field(..., description="Message sender ID")
    sender_name: str = Field(..., description="Sender's name")
    sender_role: str = Field(..., description="Sender's role (student, teacher, expert)")
    
    # Message content
    message_type: str = Field(default="text", description="Type: text, file, image, link")
    content: str = Field(..., description="Message content/text")
    formatted_content: Optional[str] = Field(default=None, description="HTML formatted content")
    
    # Attachments
    attachments: List[Dict[str, Any]] = Field(default_factory=list, description="File attachments")
    
    # Reply/thread functionality
    reply_to_id: Optional[PyObjectId] = Field(default=None, description="ID of message this replies to")
    thread_count: int = Field(default=0, description="Number of replies to this message")
    
    # Message metadata
    is_edited: bool = Field(default=False, description="Has message been edited")
    edited_at: Optional[datetime] = Field(default=None, description="When message was last edited")
    is_deleted: bool = Field(default=False, description="Is message deleted")
    deleted_at: Optional[datetime] = Field(default=None, description="When message was deleted")
    
    # Reactions and engagement
    reactions: Dict[str, List[PyObjectId]] = Field(default_factory=dict, description="Reactions to message")
    mentions: List[PyObjectId] = Field(default_factory=list, description="Users mentioned in message")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class DiscussionParticipant(BaseModel):
    """Participant information in discussion groups"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    discussion_group_id: PyObjectId = Field(..., description="Discussion group ID")
    user_id: PyObjectId = Field(..., description="User ID")
    user_name: str = Field(..., description="User name")
    user_role: str = Field(..., description="User role")
    
    # Participation details
    joined_at: datetime = Field(default_factory=datetime.utcnow, description="When user joined")
    last_seen: Optional[datetime] = Field(default=None, description="Last seen timestamp")
    message_count: int = Field(default=0, description="Messages sent by this user")
    
    # Permissions
    can_post: bool = Field(default=True, description="Can post messages")
    can_upload: bool = Field(default=True, description="Can upload files")
    is_moderator: bool = Field(default=False, description="Has moderator permissions")
    
    # Status
    is_active: bool = Field(default=True, description="Is actively participating")
    left_at: Optional[datetime] = Field(default=None, description="When user left group")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class MessageReaction(BaseModel):
    """Reactions to messages"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    message_id: PyObjectId = Field(..., description="Message ID")
    user_id: PyObjectId = Field(..., description="User who reacted")
    user_name: str = Field(..., description="User name")
    
    reaction_type: str = Field(..., description="Type of reaction (like, love, laugh, etc.)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class PinnedMessage(BaseModel):
    """Pinned messages in discussion groups"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    discussion_group_id: PyObjectId = Field(..., description="Discussion group ID")
    message_id: PyObjectId = Field(..., description="Pinned message ID")
    
    pinned_by_id: PyObjectId = Field(..., description="Who pinned the message")
    pinned_by_name: str = Field(..., description="Name of person who pinned")
    
    pin_reason: Optional[str] = Field(default="", description="Reason for pinning")
    
    pinned_at: datetime = Field(default_factory=datetime.utcnow)
    unpinned_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True, description="Is currently pinned")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}