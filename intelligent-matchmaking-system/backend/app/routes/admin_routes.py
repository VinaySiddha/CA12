"""
Admin routes for system management and analytics
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from app.core.security import get_admin_user
from app.core.database import (
    get_users_collection, get_matches_collection, 
    get_feedback_collection, get_gamification_collection
)
from datetime import datetime, timedelta
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/dashboard")
async def get_admin_dashboard(
    admin_user: dict = Depends(get_admin_user)
):
    """Get admin dashboard overview"""
    users_collection = get_users_collection()
    matches_collection = get_matches_collection()
    feedback_collection = get_feedback_collection()
    
    # Get basic counts
    total_users = await users_collection.count_documents({"is_active": True})
    total_matches = await matches_collection.count_documents({})
    total_feedback = await feedback_collection.count_documents({})
    
    # Get user registrations in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users_30d = await users_collection.count_documents({
        "created_at": {"$gte": thirty_days_ago}
    })
    
    # Get active matches
    active_matches = await matches_collection.count_documents({
        "status": {"$in": ["pending", "accepted", "active"]}
    })
    
    # Get average rating
    pipeline = [
        {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
    ]
    rating_result = await feedback_collection.aggregate(pipeline).to_list(length=1)
    avg_rating = rating_result[0]["avg_rating"] if rating_result else 0
    
    return {
        "overview": {
            "total_users": total_users,
            "total_matches": total_matches,
            "active_matches": active_matches,
            "total_feedback": total_feedback,
            "new_users_30d": new_users_30d,
            "average_rating": round(avg_rating, 2)
        }
    }


@router.get("/users")
async def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    status_filter: Optional[str] = Query(None),
    role_filter: Optional[str] = Query(None),
    admin_user: dict = Depends(get_admin_user)
):
    """Get all users with pagination and filtering"""
    users_collection = get_users_collection()
    
    # Build filter
    user_filter = {}
    if status_filter:
        if status_filter == "active":
            user_filter["is_active"] = True
        elif status_filter == "inactive":
            user_filter["is_active"] = False
    
    if role_filter:
        user_filter["role"] = role_filter
    
    # Get total count
    total_users = await users_collection.count_documents(user_filter)
    
    # Get paginated users
    skip = (page - 1) * limit
    users = []
    
    async for user in users_collection.find(
        user_filter,
        {"hashed_password": 0}
    ).skip(skip).limit(limit):
        user["id"] = str(user.pop("_id"))
        users.append(user)
    
    return {
        "users": users,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total_users,
            "total_pages": (total_users + limit - 1) // limit
        }
    }


@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: str,
    is_active: bool,
    admin_user: dict = Depends(get_admin_user)
):
    """Update user active status"""
    users_collection = get_users_collection()
    
    try:
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": is_active, "updated_at": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": f"User status updated to {'active' if is_active else 'inactive'}"}
    
    except Exception as e:
        logger.error(f"Error updating user status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user status"
        )


@router.get("/analytics/matches")
async def get_match_analytics(
    period: str = Query("30d"),
    admin_user: dict = Depends(get_admin_user)
):
    """Get match analytics"""
    matches_collection = get_matches_collection()
    
    # Calculate date range
    if period == "7d":
        start_date = datetime.utcnow() - timedelta(days=7)
    elif period == "30d":
        start_date = datetime.utcnow() - timedelta(days=30)
    elif period == "90d":
        start_date = datetime.utcnow() - timedelta(days=90)
    else:
        start_date = datetime.utcnow() - timedelta(days=30)
    
    # Aggregate match statistics
    pipeline = [
        {"$match": {"created_at": {"$gte": start_date}}},
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1},
                "avg_score": {"$avg": "$match_score.overall_score"}
            }
        }
    ]
    
    match_stats = {}
    async for stat in matches_collection.aggregate(pipeline):
        match_stats[stat["_id"]] = {
            "count": stat["count"],
            "avg_score": round(stat["avg_score"], 3) if stat["avg_score"] else 0
        }
    
    # Get match type distribution
    type_pipeline = [
        {"$match": {"created_at": {"$gte": start_date}}},
        {"$group": {"_id": "$match_type", "count": {"$sum": 1}}}
    ]
    
    match_types = {}
    async for type_stat in matches_collection.aggregate(type_pipeline):
        match_types[type_stat["_id"]] = type_stat["count"]
    
    return {
        "period": period,
        "match_status_distribution": match_stats,
        "match_type_distribution": match_types
    }


@router.get("/analytics/feedback")
async def get_feedback_analytics(
    period: str = Query("30d"),
    admin_user: dict = Depends(get_admin_user)
):
    """Get feedback analytics"""
    feedback_collection = get_feedback_collection()
    
    # Calculate date range
    if period == "7d":
        start_date = datetime.utcnow() - timedelta(days=7)
    elif period == "30d":
        start_date = datetime.utcnow() - timedelta(days=30)
    elif period == "90d":
        start_date = datetime.utcnow() - timedelta(days=90)
    else:
        start_date = datetime.utcnow() - timedelta(days=30)
    
    # Rating distribution
    pipeline = [
        {"$match": {"created_at": {"$gte": start_date}}},
        {
            "$group": {
                "_id": "$rating",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    
    rating_distribution = {}
    total_feedback = 0
    
    async for rating_stat in feedback_collection.aggregate(pipeline):
        rating_distribution[str(rating_stat["_id"])] = rating_stat["count"]
        total_feedback += rating_stat["count"]
    
    # Average rating by feedback type
    type_pipeline = [
        {"$match": {"created_at": {"$gte": start_date}}},
        {
            "$group": {
                "_id": "$feedback_type",
                "avg_rating": {"$avg": "$rating"},
                "count": {"$sum": 1}
            }
        }
    ]
    
    feedback_by_type = {}
    async for type_stat in feedback_collection.aggregate(type_pipeline):
        feedback_by_type[type_stat["_id"]] = {
            "avg_rating": round(type_stat["avg_rating"], 2),
            "count": type_stat["count"]
        }
    
    return {
        "period": period,
        "total_feedback": total_feedback,
        "rating_distribution": rating_distribution,
        "feedback_by_type": feedback_by_type
    }


@router.get("/analytics/users")
async def get_user_analytics(
    admin_user: dict = Depends(get_admin_user)
):
    """Get user analytics"""
    users_collection = get_users_collection()
    gamification_collection = get_gamification_collection()
    
    # User registration trend (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    pipeline = [
        {"$match": {"created_at": {"$gte": thirty_days_ago}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$created_at"
                    }
                },
                "registrations": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    
    registration_trend = []
    async for day_stat in users_collection.aggregate(pipeline):
        registration_trend.append({
            "date": day_stat["_id"],
            "registrations": day_stat["registrations"]
        })
    
    # User role distribution
    role_pipeline = [
        {"$group": {"_id": "$role", "count": {"$sum": 1}}}
    ]
    
    role_distribution = {}
    async for role_stat in users_collection.aggregate(role_pipeline):
        role_distribution[role_stat["_id"]] = role_stat["count"]
    
    # Academic level distribution
    level_pipeline = [
        {"$match": {"profile.academic_level": {"$exists": True}}},
        {"$group": {"_id": "$profile.academic_level", "count": {"$sum": 1}}}
    ]
    
    academic_distribution = {}
    async for level_stat in users_collection.aggregate(level_pipeline):
        academic_distribution[level_stat["_id"]] = level_stat["count"]
    
    return {
        "registration_trend": registration_trend,
        "role_distribution": role_distribution,
        "academic_level_distribution": academic_distribution
    }


@router.post("/notifications/broadcast")
async def broadcast_notification(
    title: str,
    message: str,
    target_role: Optional[str] = None,
    admin_user: dict = Depends(get_admin_user)
):
    """Broadcast notification to users (placeholder for notification system)"""
    # This would integrate with a notification service
    # For now, just return success message
    
    target = target_role if target_role else "all users"
    
    return {
        "message": f"Notification '{title}' broadcasted to {target}",
        "notification": {
            "title": title,
            "message": message,
            "target": target,
            "sent_at": datetime.utcnow()
        }
    }


@router.get("/reports/export")
async def export_system_report(
    report_type: str = Query("overview"),
    format_type: str = Query("json"),
    admin_user: dict = Depends(get_admin_user)
):
    """Export system reports"""
    # This is a placeholder for report export functionality
    # In a real implementation, this would generate CSV, PDF, or other formats
    
    if report_type == "overview":
        # Get overview data
        dashboard_data = await get_admin_dashboard(admin_user)
        
        return {
            "report_type": report_type,
            "format": format_type,
            "generated_at": datetime.utcnow(),
            "data": dashboard_data
        }
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported report type"
        )