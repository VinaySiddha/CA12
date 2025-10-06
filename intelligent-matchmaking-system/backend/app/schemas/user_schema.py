"""
User schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime


class UserProfileCreate(BaseModel):
    bio: Optional[str] = None
    academic_level: str
    field_of_study: str
    institution: str
    learning_preferences: List[str] = []
    availability: Dict[str, List[str]] = {}
    timezone: str = "UTC"
    languages: List[str] = ["English"]


class UserSkillsCreate(BaseModel):
    strengths: List[str] = []
    weaknesses: List[str] = []
    interests: List[str] = []
    expertise_level: Dict[str, int] = {}


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
    role: str = "student"
    profile: Optional[UserProfileCreate] = None
    skills: Optional[UserSkillsCreate] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    profile: Optional[UserProfileCreate] = None
    skills: Optional[UserSkillsCreate] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: str
    is_active: bool
    is_verified: bool
    role: str
    profile: Optional[UserProfileCreate] = None
    skills: Optional[UserSkillsCreate] = None
    points: int
    level: int
    badges: List[str]
    created_at: datetime
    last_login: Optional[datetime] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str


class UserPublicProfile(BaseModel):
    id: str
    username: str
    full_name: str
    profile: Optional[UserProfileCreate] = None
    skills: Optional[UserSkillsCreate] = None
    points: int
    level: int
    badges: List[str]