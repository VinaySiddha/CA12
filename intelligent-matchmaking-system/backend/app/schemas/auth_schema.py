"""
Authentication schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List


class UserInfo(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str
    last_login: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserInfo] = None
    expires_in: Optional[int] = None


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (maximum 72 bytes)')
        return v


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
    confirm_password: str
    role: str = "student"  # "student" or "teacher"
    teaching_subjects: Optional[List[str]] = None
    years_experience: Optional[int] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (maximum 72 bytes)')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (maximum 72 bytes)')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class EmailVerificationRequest(BaseModel):
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    token: str