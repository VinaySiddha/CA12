"""
Authentication routes
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user
)
from app.core.database import get_users_collection
from app.core.config import settings
from app.schemas.auth_schema import Token, RegisterRequest
from app.models.user_model import UserModel
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=dict)
async def register(user_data: RegisterRequest):
    """Register a new user"""
    users_collection = get_users_collection()
    
    # Check if passwords match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Check if user already exists
    existing_user = await users_collection.find_one({
        "$or": [
            {"email": user_data.email},
            {"username": user_data.username}
        ]
    })
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    # Basic user data
    user_dict = {
        "email": user_data.email,
        "username": user_data.username,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password,
        "role": user_data.role
    }
    
    # Add teacher-specific fields if applicable
    if user_data.role == "teacher" and user_data.teaching_subjects:
        user_dict["teaching_subjects"] = user_data.teaching_subjects
        if user_data.years_experience:
            user_dict["years_experience"] = user_data.years_experience
    
    new_user = UserModel(**user_dict)
    
    # Insert user into database
    result = await users_collection.insert_one(new_user.dict(by_alias=True, exclude={"id"}))
    
    if result.inserted_id:
        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return access token"""
    users_collection = get_users_collection()
    
    # Find user by username or email
    user = await users_collection.find_one({
        "$or": [
            {"username": form_data.username},
            {"email": form_data.username}
        ]
    })
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    
    # Handle both ObjectId and string IDs
    user_id = user["_id"]
    if isinstance(user_id, ObjectId):
        user_id_str = str(user_id)
    else:
        user_id_str = user_id
    
    access_token = create_access_token(
        data={"sub": user_id_str}, expires_delta=access_token_expires
    )
    
    # Update last login with current datetime
    from datetime import datetime
    current_time = datetime.utcnow()
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": current_time}}
    )
    
    # Get basic user info to return with token
    user_info = {
        "id": user_id_str,
        "username": user.get("username"),
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "role": user.get("role", "student"),
        "last_login": current_time
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_info,
        "expires_in": settings.access_token_expire_minutes * 60
    }


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user (client should discard token)"""
    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    user_data = current_user.copy()
    user_data["id"] = str(user_data.pop("_id"))
    return user_data


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user)
):
    """Change user password"""
    users_collection = get_users_collection()
    
    # Verify current password
    if not verify_password(current_password, current_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    hashed_new_password = get_password_hash(new_password)
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"hashed_password": hashed_new_password}}
    )
    
    return {"message": "Password changed successfully"}