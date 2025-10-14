"""
Notification Routes - API endpoints for user notifications
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.core.database import get_database
from app.core.security import get_current_user
from app.models.notification_model import Notification
from app.models.user_model import UserModel

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/")
async def get_notifications(
    unread_only: bool = False,
    skip: int = 0,
    limit: int = 50,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get notifications for current user"""
    query = {"user_id": ObjectId(current_user["_id"])}
    
    if unread_only:
        query["is_read"] = False
    
    notifications = await db.notifications.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(None)
    
    # Convert ObjectIds
    for notif in notifications:
        notif["_id"] = str(notif["_id"])
        notif["user_id"] = str(notif["user_id"])
        if notif.get("related_id"):
            notif["related_id"] = str(notif["related_id"])
        if notif.get("sender_id"):
            notif["sender_id"] = str(notif["sender_id"])
    
    return notifications


@router.get("/unread-count")
async def get_unread_count(
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get count of unread notifications"""
    count = await db.notifications.count_documents({
        "user_id": ObjectId(current_user["_id"]),
        "is_read": False
    })
    
    return {"unread_count": count}


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Mark a notification as read"""
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid notification ID"
        )
    
    notification = await db.notifications.find_one({"_id": ObjectId(notification_id)})
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Check permission
    if str(notification["user_id"]) != current_user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only mark your own notifications as read"
        )
    
    await db.notifications.update_one(
        {"_id": ObjectId(notification_id)},
        {
            "$set": {
                "is_read": True,
                "read_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Notification marked as read"}


@router.post("/mark-all-read")
async def mark_all_as_read(
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Mark all notifications as read"""
    result = await db.notifications.update_many(
        {
            "user_id": ObjectId(current_user["_id"]),
            "is_read": False
        },
        {
            "$set": {
                "is_read": True,
                "read_at": datetime.utcnow()
            }
        }
    )
    
    return {
        "message": "All notifications marked as read",
        "count": result.modified_count
    }


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Delete a notification"""
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid notification ID"
        )
    
    notification = await db.notifications.find_one({"_id": ObjectId(notification_id)})
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Check permission
    if str(notification["user_id"]) != current_user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own notifications"
        )
    
    await db.notifications.delete_one({"_id": ObjectId(notification_id)})
    
    return {"message": "Notification deleted"}


@router.get("/by-type/{notification_type}")
async def get_notifications_by_type(
    notification_type: str,
    skip: int = 0,
    limit: int = 50,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get notifications by type"""
    notifications = await db.notifications.find({
        "user_id": ObjectId(current_user["_id"]),
        "notification_type": notification_type
    }).sort("created_at", -1).skip(skip).limit(limit).to_list(None)
    
    # Convert ObjectIds
    for notif in notifications:
        notif["_id"] = str(notif["_id"])
        notif["user_id"] = str(notif["user_id"])
        if notif.get("related_id"):
            notif["related_id"] = str(notif["related_id"])
        if notif.get("sender_id"):
            notif["sender_id"] = str(notif["sender_id"])
    
    return notifications
