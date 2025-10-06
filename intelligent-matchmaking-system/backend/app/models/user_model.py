"""
User data model
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any, Annotated
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x),
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def validate(cls, value):
        if isinstance(value, ObjectId):
            return value
        if isinstance(value, str):
            if ObjectId.is_valid(value):
                return ObjectId(value)
        raise ValueError("Invalid ObjectId")


class UserProfile(BaseModel):
    bio: Optional[str] = None
    academic_level: str  # "undergraduate", "graduate", "phd", "postdoc"
    field_of_study: str
    institution: str
    learning_preferences: List[str] = []  # ["visual", "auditory", "kinesthetic", "reading"]
    availability: Dict[str, List[str]] = {}  # {"monday": ["09:00-12:00"], "tuesday": [...]}
    timezone: str = "UTC"
    languages: List[str] = ["English"]


class UserSkills(BaseModel):
    strengths: List[str] = []  # Topics user is strong in
    weaknesses: List[str] = []  # Topics user needs help with
    interests: List[str] = []  # Topics user is interested in learning
    expertise_level: Dict[str, int] = {}  # {"python": 8, "mathematics": 6} (1-10 scale)


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    username: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False
    role: str = "student"  # "student", "mentor", "admin"
    profile: Optional[UserProfile] = None
    skills: Optional[UserSkills] = None
    
    # Gamification fields
    points: int = 0
    level: int = 1
    badges: List[str] = []
    
    # Tracking fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )