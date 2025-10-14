"""
Authentication schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
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


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
    confirm_password: str
    role: str = "student"  # "student" or "teacher"
    teaching_subjects: Optional[List[str]] = None
    years_experience: Optional[int] = None


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class EmailVerificationRequest(BaseModel):
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    token: str