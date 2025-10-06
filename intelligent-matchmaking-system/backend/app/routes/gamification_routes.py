"""
Gamification routes for badges, points, leaderboards
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_active_user
from app.core.database import get_gamification_collection, get_users_collection
from app.models.gamification_model import (
    GamificationModel, UserStats, Achievement, Leaderboard, AVAILABLE_BADGES
)
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/profile")
async def get_gamification_profile(
    current_user: dict = Depends(get_current_active_user)
):
    """Get current user's gamification profile"""
    gamification_collection = get_gamification_collection()
    
    # Get or create gamification profile
    profile = await gamification_collection.find_one({"user_id": current_user["_id"]})
    
    if not profile:
        # Create initial profile
        initial_stats = UserStats(user_id=ObjectId(str(current_user["_id"])))
        initial_profile = GamificationModel(
            user_id=ObjectId(str(current_user["_id"])),
            stats=initial_stats
        )
        
        result = await gamification_collection.insert_one(
            initial_profile.dict(by_alias=True, exclude={"id"})
        )
        
        if result.inserted_id:
            profile = await gamification_collection.find_one({"_id": result.inserted_id})
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create gamification profile"
            )
    
    # Convert ObjectIds to strings
    profile["id"] = str(profile.pop("_id"))
    profile["user_id"] = str(profile["user_id"])
    
    return profile


@router.get("/badges")
async def get_available_badges():
    """Get all available badges and their criteria"""
    return {
        "badges": [badge.dict() for badge in AVAILABLE_BADGES.values()],
        "total_badges": len(AVAILABLE_BADGES)
    }


@router.get("/my-badges")
async def get_my_badges(
    current_user: dict = Depends(get_current_active_user)
):
    """Get current user's earned badges"""
    gamification_collection = get_gamification_collection()
    
    profile = await gamification_collection.find_one({"user_id": current_user["_id"]})
    
    if not profile:
        return {"earned_badges": [], "total_earned": 0}
    
    earned_badge_ids = profile.get("badges_earned", [])
    earned_badges = [
        AVAILABLE_BADGES[badge_id].dict() 
        for badge_id in earned_badge_ids 
        if badge_id in AVAILABLE_BADGES
    ]
    
    return {
        "earned_badges": earned_badges,
        "total_earned": len(earned_badges),
        "total_points_from_badges": sum(badge["points_value"] for badge in earned_badges)
    }


@router.post("/award-points")
async def award_points(
    points: int,
    reason: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Award points to current user (typically called by other services)"""
    gamification_collection = get_gamification_collection()
    users_collection = get_users_collection()
    
    # Update gamification profile
    result = await gamification_collection.update_one(
        {"user_id": current_user["_id"]},
        {
            "$inc": {
                "total_points": points,
                "experience_points": points
            },
            "$set": {"updated_at": "2025-01-01T00:00:00Z"}
        },
        upsert=True
    )
    
    # Update user points
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {"points": points}}
    )
    
    # Check for level up
    await _check_level_up(current_user["_id"])
    
    # Check for new badges
    await _check_badge_eligibility(current_user["_id"])
    
    return {
        "message": f"Awarded {points} points for: {reason}",
        "points_awarded": points
    }


@router.get("/leaderboard")
async def get_leaderboard(
    category: str = Query("overall"),
    period: str = Query("all_time"),
    limit: int = Query(10, le=100)
):
    """Get leaderboard rankings"""
    users_collection = get_users_collection()
    
    # Build aggregation pipeline
    pipeline = [
        {"$match": {"is_active": True}},
        {"$sort": {"points": -1}},
        {"$limit": limit},
        {
            "$project": {
                "username": 1,
                "full_name": 1,
                "points": 1,
                "level": 1
            }
        }
    ]
    
    leaderboard_data = []
    rank = 1
    
    async for user in users_collection.aggregate(pipeline):
        leaderboard_entry = {
            "rank": rank,
            "user_id": str(user["_id"]),
            "username": user["username"],
            "full_name": user["full_name"],
            "total_points": user.get("points", 0),
            "level": user.get("level", 1)
        }
        leaderboard_data.append(leaderboard_entry)
        rank += 1
    
    return {
        "leaderboard": leaderboard_data,
        "category": category,
        "period": period,
        "total_participants": len(leaderboard_data)
    }


@router.get("/stats")
async def get_user_stats(
    current_user: dict = Depends(get_current_active_user)
):
    """Get detailed user statistics"""
    gamification_collection = get_gamification_collection()
    
    profile = await gamification_collection.find_one({"user_id": current_user["_id"]})
    
    if not profile:
        return {"message": "No statistics available"}
    
    stats = profile.get("stats", {})
    
    return {
        "learning_stats": {
            "total_study_sessions": stats.get("total_study_sessions", 0),
            "total_study_hours": stats.get("total_study_hours", 0),
            "topics_mastered": stats.get("topics_mastered", []),
            "current_streak": stats.get("current_streak", 0),
            "longest_streak": stats.get("longest_streak", 0)
        },
        "mentoring_stats": {
            "sessions_as_mentor": stats.get("sessions_as_mentor", 0),
            "sessions_as_mentee": stats.get("sessions_as_mentee", 0),
            "mentees_helped": stats.get("mentees_helped", 0),
            "average_rating_as_mentor": stats.get("average_rating_as_mentor", 0.0)
        },
        "engagement_stats": {
            "logins_this_month": stats.get("logins_this_month", 0),
            "feedback_given": stats.get("feedback_given", 0),
            "study_groups_joined": stats.get("study_groups_joined", 0),
            "study_groups_created": stats.get("study_groups_created", 0)
        }
    }


@router.post("/update-stats")
async def update_user_stats(
    stat_type: str,
    increment: int = 1,
    current_user: dict = Depends(get_current_active_user)
):
    """Update user statistics (called by other services)"""
    gamification_collection = get_gamification_collection()
    
    # Map stat types to database fields
    stat_mapping = {
        "study_session": "stats.total_study_sessions",
        "mentor_session": "stats.sessions_as_mentor",
        "mentee_session": "stats.sessions_as_mentee",
        "feedback_given": "stats.feedback_given",
        "study_group_joined": "stats.study_groups_joined",
        "study_group_created": "stats.study_groups_created",
        "login": "stats.logins_this_month"
    }
    
    if stat_type not in stat_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid stat type"
        )
    
    update_field = stat_mapping[stat_type]
    
    result = await gamification_collection.update_one(
        {"user_id": current_user["_id"]},
        {
            "$inc": {update_field: increment},
            "$set": {"stats.last_calculated": "2025-01-01T00:00:00Z"}
        },
        upsert=True
    )
    
    # Check for badge eligibility after stat update
    await _check_badge_eligibility(current_user["_id"])
    
    return {"message": f"Updated {stat_type} by {increment}"}


async def _check_level_up(user_id: ObjectId):
    """Check if user should level up based on experience points"""
    gamification_collection = get_gamification_collection()
    users_collection = get_users_collection()
    
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return
    
    current_level = profile.get("level", 1)
    experience_points = profile.get("experience_points", 0)
    
    # Calculate required points for next level (exponential growth)
    points_for_next_level = 100 * (current_level ** 1.5)
    
    if experience_points >= points_for_next_level:
        new_level = current_level + 1
        points_to_next = 100 * (new_level ** 1.5)
        
        # Update level
        await gamification_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "level": new_level,
                    "points_to_next_level": points_to_next - experience_points
                }
            }
        )
        
        await users_collection.update_one(
            {"_id": user_id},
            {"$set": {"level": new_level}}
        )
        
        # Award level up bonus
        level_bonus = new_level * 50
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"total_points": level_bonus}}
        )


async def _check_badge_eligibility(user_id: ObjectId):
    """Check if user is eligible for any new badges"""
    gamification_collection = get_gamification_collection()
    users_collection = get_users_collection()
    
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return
    
    current_badges = set(profile.get("badges_earned", []))
    stats = profile.get("stats", {})
    
    # Check each badge criteria
    for badge_id, badge in AVAILABLE_BADGES.items():
        if badge_id in current_badges:
            continue  # Already earned
        
        criteria = badge.criteria
        eligible = True
        
        # Check criteria
        for criterion, required_value in criteria.items():
            if criterion == "sessions_completed":
                total_sessions = stats.get("total_study_sessions", 0)
                if total_sessions < required_value:
                    eligible = False
                    break
            elif criterion == "positive_mentor_ratings":
                # This would need to be calculated from feedback
                pass
            elif criterion == "mentee_sessions":
                mentee_sessions = stats.get("sessions_as_mentee", 0)
                if mentee_sessions < required_value:
                    eligible = False
                    break
            elif criterion == "study_streak":
                current_streak = stats.get("current_streak", 0)
                if current_streak < required_value:
                    eligible = False
                    break
            elif criterion == "topics_mastered":
                topics_count = len(stats.get("topics_mastered", []))
                if topics_count < required_value:
                    eligible = False
                    break
            elif criterion == "study_groups_created":
                groups_created = stats.get("study_groups_created", 0)
                if groups_created < required_value:
                    eligible = False
                    break
        
        if eligible:
            # Award badge
            await gamification_collection.update_one(
                {"user_id": user_id},
                {
                    "$push": {"badges_earned": badge_id},
                    "$inc": {"total_points": badge.points_value}
                }
            )
            
            await users_collection.update_one(
                {"_id": user_id},
                {
                    "$push": {"badges": badge_id},
                    "$inc": {"points": badge.points_value}
                }
            )