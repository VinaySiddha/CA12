"""
User management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_user, get_current_active_user
from app.core.database import get_users_collection
from app.schemas.user_schema import UserUpdate, UserResponse, UserPublicProfile
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: dict = Depends(get_current_active_user)):
    """Get current user's profile"""
    user_data = current_user.copy()
    user_data["id"] = str(user_data.pop("_id"))
    return user_data


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """Update current user's profile"""
    users_collection = get_users_collection()
    
    # Prepare update data
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = "2025-01-01T00:00:00Z"
        
        result = await users_collection.update_one(
            {"_id": current_user["_id"]},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No changes made to profile"
            )
    
    # Get updated user
    updated_user = await users_collection.find_one({"_id": current_user["_id"]})
    updated_user["id"] = str(updated_user.pop("_id"))
    return updated_user


@router.get("/public/{user_id}", response_model=UserPublicProfile)
async def get_public_profile(user_id: str):
    """Get public profile of a user"""
    users_collection = get_users_collection()
    
    try:
        user = await users_collection.find_one(
            {"_id": ObjectId(user_id)},
            {"hashed_password": 0, "email": 0, "is_active": 0, "is_verified": 0}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user["id"] = str(user.pop("_id"))
    return user


@router.get("/search", response_model=List[UserPublicProfile])
async def search_users(
    query: str = Query(..., min_length=2),
    field_of_study: Optional[str] = None,
    academic_level: Optional[str] = None,
    skills: Optional[List[str]] = Query(None),
    limit: int = Query(10, le=50),
    current_user: dict = Depends(get_current_active_user)
):
    """Search for users based on various criteria"""
    users_collection = get_users_collection()
    
    # Build search query
    search_filter = {
        "_id": {"$ne": current_user["_id"]},  # Exclude current user
        "is_active": True,
        "$or": [
            {"username": {"$regex": query, "$options": "i"}},
            {"full_name": {"$regex": query, "$options": "i"}},
            {"profile.field_of_study": {"$regex": query, "$options": "i"}},
            {"skills.interests": {"$in": [query]}},
            {"skills.strengths": {"$in": [query]}}
        ]
    }
    
    # Add additional filters
    if field_of_study:
        search_filter["profile.field_of_study"] = {"$regex": field_of_study, "$options": "i"}
    
    if academic_level:
        search_filter["profile.academic_level"] = academic_level
    
    if skills:
        search_filter["$or"].extend([
            {"skills.interests": {"$in": skills}},
            {"skills.strengths": {"$in": skills}}
        ])
    
    # Execute search
    cursor = users_collection.find(
        search_filter,
        {"hashed_password": 0, "email": 0, "is_active": 0, "is_verified": 0}
    ).limit(limit)
    
    users = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for user in users:
        user["id"] = str(user.pop("_id"))
    
    return users


@router.get("/mentors", response_model=List[UserPublicProfile])
async def get_available_mentors(
    topic: Optional[str] = None,
    academic_level: Optional[str] = None,
    limit: int = Query(10, le=50),
    current_user: dict = Depends(get_current_active_user)
):
    """Get list of available mentors"""
    users_collection = get_users_collection()
    
    # Build filter for mentors
    mentor_filter = {
        "_id": {"$ne": current_user["_id"]},
        "is_active": True,
        "$or": [
            {"role": "mentor"},
            {"role": "admin"}
        ]
    }
    
    # Add topic filter
    if topic:
        mentor_filter["skills.strengths"] = {"$in": [topic]}
    
    # Add academic level filter (mentors should be same or higher level)
    if academic_level:
        level_hierarchy = ["undergraduate", "graduate", "phd", "postdoc"]
        if academic_level in level_hierarchy:
            current_level_index = level_hierarchy.index(academic_level)
            eligible_levels = level_hierarchy[current_level_index:]
            mentor_filter["profile.academic_level"] = {"$in": eligible_levels}
    
    # Execute query
    cursor = users_collection.find(
        mentor_filter,
        {"hashed_password": 0, "email": 0, "is_active": 0, "is_verified": 0}
    ).limit(limit)
    
    mentors = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for mentor in mentors:
        mentor["id"] = str(mentor.pop("_id"))
    
    return mentors


@router.delete("/profile")
async def delete_user_account(current_user: dict = Depends(get_current_active_user)):
    """Delete current user's account"""
    users_collection = get_users_collection()
    
    # Soft delete by deactivating account
    result = await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"is_active": False, "updated_at": "2025-01-01T00:00:00Z"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete account"
        )
    
    return {"message": "Account deleted successfully"}