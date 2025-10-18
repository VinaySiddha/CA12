"""
Discussion Group schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class DiscussionGroupCreate(BaseModel):
    """Schema for creating a discussion group"""
    title: str = Field(..., min_length=1, max_length=200, description="Group title")
    description: Optional[str] = Field(default="", max_length=1000, description="Group description")
    is_open: bool = Field(default=True, description="Can new participants join")
    auto_add_registered: bool = Field(default=True, description="Auto-add meeting registrants")


class DiscussionGroupUpdate(BaseModel):
    """Schema for updating discussion group"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Group title")
    description: Optional[str] = Field(None, max_length=1000, description="Group description")
    is_open: Optional[bool] = Field(None, description="Can new participants join")
    auto_add_registered: Optional[bool] = Field(None, description="Auto-add meeting registrants")


class DiscussionGroupResponse(BaseModel):
    """Schema for discussion group response"""
    id: str = Field(..., description="Group ID")
    meeting_id: str = Field(..., description="Associated meeting ID")
    meeting_title: str = Field(..., description="Meeting title")
    title: str = Field(..., description="Group title")
    description: str = Field(..., description="Group description")
    
    moderator_id: str = Field(..., description="Moderator ID")
    moderator_name: str = Field(..., description="Moderator name")
    
    participant_count: int = Field(..., description="Number of participants")
    message_count: int = Field(..., description="Total messages")
    
    is_active: bool = Field(..., description="Is group active")
    is_open: bool = Field(..., description="Can new participants join")
    auto_add_registered: bool = Field(..., description="Auto-add meeting registrants")
    
    last_activity: Optional[datetime] = Field(None, description="Last message timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    # User-specific info
    is_participant: Optional[bool] = Field(None, description="Is current user a participant")
    is_moderator: Optional[bool] = Field(None, description="Is current user a moderator")
    unread_count: Optional[int] = Field(None, description="Unread messages for current user")


class MessageCreate(BaseModel):
    """Schema for creating a message"""
    content: str = Field(..., min_length=1, max_length=2000, description="Message content")
    message_type: str = Field(default="text", description="Message type")
    reply_to_id: Optional[str] = Field(None, description="ID of message this replies to")
    mentions: List[str] = Field(default_factory=list, description="User IDs mentioned")


class MessageUpdate(BaseModel):
    """Schema for updating a message"""
    content: str = Field(..., min_length=1, max_length=2000, description="Updated message content")


class MessageResponse(BaseModel):
    """Schema for message response"""
    id: str = Field(..., description="Message ID")
    discussion_group_id: str = Field(..., description="Discussion group ID")
    
    sender_id: str = Field(..., description="Sender ID")
    sender_name: str = Field(..., description="Sender name")
    sender_role: str = Field(..., description="Sender role")
    
    message_type: str = Field(..., description="Message type")
    content: str = Field(..., description="Message content")
    formatted_content: Optional[str] = Field(None, description="HTML formatted content")
    
    attachments: List[Dict[str, Any]] = Field(default_factory=list, description="Attachments")
    
    reply_to_id: Optional[str] = Field(None, description="Replied message ID")
    reply_to_content: Optional[str] = Field(None, description="Content of replied message")
    reply_to_sender: Optional[str] = Field(None, description="Name of replied message sender")
    thread_count: int = Field(default=0, description="Number of replies")
    
    is_edited: bool = Field(default=False, description="Is message edited")
    edited_at: Optional[datetime] = Field(None, description="Edit timestamp")
    
    reactions: Dict[str, List[Dict[str, str]]] = Field(default_factory=dict, description="Reactions")
    reaction_counts: Dict[str, int] = Field(default_factory=dict, description="Reaction counts")
    mentions: List[str] = Field(default_factory=list, description="Mentioned users")
    
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    
    # User-specific info
    can_edit: Optional[bool] = Field(None, description="Can current user edit this message")
    can_delete: Optional[bool] = Field(None, description="Can current user delete this message")
    user_reaction: Optional[str] = Field(None, description="Current user's reaction")


class ParticipantResponse(BaseModel):
    """Schema for participant response"""
    user_id: str = Field(..., description="User ID")
    user_name: str = Field(..., description="User name")
    user_role: str = Field(..., description="User role")
    
    joined_at: datetime = Field(..., description="Join timestamp")
    last_seen: Optional[datetime] = Field(None, description="Last seen timestamp")
    message_count: int = Field(default=0, description="Message count")
    
    can_post: bool = Field(default=True, description="Can post messages")
    can_upload: bool = Field(default=True, description="Can upload files")
    is_moderator: bool = Field(default=False, description="Is moderator")
    is_active: bool = Field(default=True, description="Is active participant")


class MessageListResponse(BaseModel):
    """Schema for message list with pagination"""
    messages: List[MessageResponse] = Field(..., description="List of messages")
    total_count: int = Field(..., description="Total message count")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total pages")
    has_more: bool = Field(..., description="Are there more messages")


class ReactionCreate(BaseModel):
    """Schema for creating a reaction"""
    reaction_type: str = Field(..., description="Reaction type (like, love, laugh, etc.)")


class PinMessageRequest(BaseModel):
    """Schema for pinning a message"""
    pin_reason: Optional[str] = Field(default="", max_length=200, description="Reason for pinning")


class DiscussionGroupListResponse(BaseModel):
    """Schema for discussion group list"""
    groups: List[DiscussionGroupResponse] = Field(..., description="List of groups")
    total_count: int = Field(..., description="Total group count")


class MessageSearchQuery(BaseModel):
    """Schema for message search parameters"""
    search: Optional[str] = Field(None, description="Search term")
    sender_id: Optional[str] = Field(None, description="Filter by sender")
    message_type: Optional[str] = Field(None, description="Filter by message type")
    date_from: Optional[datetime] = Field(None, description="Filter from date")
    date_to: Optional[datetime] = Field(None, description="Filter to date")
    has_attachments: Optional[bool] = Field(None, description="Filter messages with attachments")
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(50, ge=1, le=100, description="Items per page")
    sort_order: str = Field("desc", description="Sort order (asc/desc)")


class NotificationSettings(BaseModel):
    """Schema for discussion notification settings"""
    email_notifications: bool = Field(default=True, description="Receive email notifications")
    push_notifications: bool = Field(default=True, description="Receive push notifications")
    mention_notifications: bool = Field(default=True, description="Notifications when mentioned")
    new_message_notifications: bool = Field(default=False, description="Notifications for all messages")
    digest_frequency: str = Field(default="daily", description="Digest frequency (none, daily, weekly)")


class TypingIndicator(BaseModel):
    """Schema for typing indicators"""
    user_id: str = Field(..., description="User who is typing")
    user_name: str = Field(..., description="User name")
    started_typing_at: datetime = Field(..., description="When user started typing")


class OnlineStatus(BaseModel):
    """Schema for online status"""
    user_id: str = Field(..., description="User ID")
    user_name: str = Field(..., description="User name")
    is_online: bool = Field(..., description="Is user online")
    last_seen: Optional[datetime] = Field(None, description="Last seen timestamp")


class GroupStats(BaseModel):
    """Schema for group statistics"""
    total_messages: int = Field(..., description="Total messages")
    total_participants: int = Field(..., description="Total participants")
    active_participants: int = Field(..., description="Active participants")
    messages_today: int = Field(..., description="Messages sent today")
    messages_this_week: int = Field(..., description="Messages sent this week")
    top_contributors: List[Dict[str, Any]] = Field(..., description="Most active participants")
    activity_timeline: List[Dict[str, Any]] = Field(..., description="Activity over time")
    popular_reactions: Dict[str, int] = Field(..., description="Most used reactions")