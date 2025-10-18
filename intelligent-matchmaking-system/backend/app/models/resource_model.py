"""
Resource Model - For educational resources uploaded by teachers/experts/admins
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


class Resource(BaseModel):
    """Educational resource uploaded by teachers/experts"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., description="Resource title")
    description: str = Field(..., description="Resource description")
    category: str = Field(..., description="Resource category (e.g., 'Python', 'Machine Learning', 'Web Development')")
    resource_type: str = Field(..., description="Type of resource ('pdf', 'video', 'article', 'code', 'document')")
    
    # File information
    file_id: Optional[str] = Field(None, description="GridFS file ID if file uploaded")
    file_name: Optional[str] = Field(None, description="Original filename")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    file_type: Optional[str] = Field(None, description="MIME type")
    
    # External link (alternative to file upload)
    external_url: Optional[str] = Field(None, description="External URL if not uploading file")
    
    # Metadata
    uploaded_by: PyObjectId = Field(..., description="User ID of uploader (teacher/expert/admin)")
    uploader_name: str = Field(..., description="Name of uploader")
    uploader_role: str = Field(..., description="Role of uploader")
    
    tags: List[str] = Field(default_factory=list, description="Tags for searching")
    difficulty_level: str = Field(default="intermediate", description="Difficulty level (beginner/intermediate/advanced)")
    
    # Engagement
    views: int = Field(default=0, description="Number of views")
    downloads: int = Field(default=0, description="Number of downloads")
    likes: List[PyObjectId] = Field(default_factory=list, description="User IDs who liked")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Visibility and connections
    is_active: bool = Field(default=True, description="Whether resource is visible")
    is_featured: bool = Field(default=False, description="Featured resource")
    linked_meetings: List[PyObjectId] = Field(default_factory=list, description="Meeting IDs this resource is linked to")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class ResourceComment(BaseModel):
    """Comments on resources"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    resource_id: PyObjectId = Field(..., description="Resource ID")
    user_id: PyObjectId = Field(..., description="Commenter user ID")
    user_name: str = Field(..., description="Commenter name")
    content: str = Field(..., description="Comment text")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
