"""
Post Schemas for Request/Response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CreatePostRequest(BaseModel):
    content: str
    media_urls: Optional[List[str]] = []
    tags: Optional[List[str]] = []


class UpdatePostRequest(BaseModel):
    content: Optional[str] = None
    media_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class CreateCommentRequest(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    user_id: str
    user_name: str
    user_role: Optional[str] = "student"
    content: str
    created_at: datetime


class PostResponse(BaseModel):
    id: str
    user_id: str
    user_name: str
    user_role: Optional[str] = "student"
    content: str
    media_urls: Optional[List[str]] = []
    likes_count: int
    is_liked: bool
    comments: List[CommentResponse]
    tags: Optional[List[str]] = []
    created_at: datetime
    updated_at: datetime
