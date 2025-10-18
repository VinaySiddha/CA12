"""
Meeting Routes - API endpoints for teacher-created events and student registration
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone
import logging

from app.core.database import get_database
from app.core.security import get_current_user, get_current_active_user
from app.models.meeting_model import Meeting, MeetingRegistration, MeetingFeedback, PyObjectId
from app.schemas.meeting_schema import (
    MeetingCreate, MeetingUpdate, MeetingResponse, MeetingListResponse,
    MeetingRegistrationRequest, MeetingFeedbackCreate, MeetingFeedbackResponse,
    MeetingSearchQuery
)
from app.models.user_model import UserModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/meetings", tags=["meetings"])


# Helper functions
def convert_meeting_to_response(meeting: dict, current_user_id: str = None) -> dict:
    """Convert meeting document to response format"""
    response = {
        "id": str(meeting["_id"]),
        "title": meeting["title"],
        "description": meeting.get("description", ""),
        "teacher_id": str(meeting["teacher_id"]),
        "teacher_name": meeting["teacher_name"],
        "teacher_email": meeting["teacher_email"],
        "subject": meeting["subject"],
        "category": meeting["category"],
        "scheduled_date": meeting["scheduled_date"],
        "duration_minutes": meeting["duration_minutes"],
        "timezone": meeting.get("timezone", "UTC"),
        "meeting_platform": meeting.get("meeting_platform", "google_meet"),
        "meeting_link": meeting.get("meeting_link"),
        "meeting_id": meeting.get("meeting_id"),
        "passcode": meeting.get("passcode"),
        "max_participants": meeting["max_participants"],
        "registered_count": len(meeting.get("registered_students", [])),
        "attendees_count": len(meeting.get("attendees", [])),
        "is_recurring": meeting.get("is_recurring", False),
        "is_recorded": meeting.get("is_recorded", False),
        "recording_url": meeting.get("recording_url"),
        "status": meeting.get("status", "scheduled"),
        "is_active": meeting.get("is_active", True),
        "is_public": meeting.get("is_public", True),
        "prerequisites": meeting.get("prerequisites", []),
        "materials_needed": meeting.get("materials_needed", []),
        "agenda": meeting.get("agenda", []),
        "tags": meeting.get("tags", []),
        "difficulty_level": meeting.get("difficulty_level", "intermediate"),
        "likes_count": len(meeting.get("likes", [])),
        "rating": meeting.get("rating", 0.0),
        "feedback_count": meeting.get("feedback_count", 0),
        "created_at": meeting["created_at"],
        "updated_at": meeting["updated_at"],
        "discussion_group_id": str(meeting["discussion_group_id"]) if meeting.get("discussion_group_id") else None,
    }
    
    if current_user_id:
        user_id = ObjectId(current_user_id)
        response["is_registered"] = user_id in meeting.get("registered_students", [])
        response["is_liked"] = user_id in meeting.get("likes", [])
    
    return response


@router.post("/request", status_code=status.HTTP_201_CREATED)
async def request_meeting(
    meeting_req: MeetingRequest,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Request a meeting with a teacher/expert (students only)
    """
    # Only students can request meetings
    if current_user.get("role") != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can request meetings"
        )
    
    # Validate teacher ID
    if not ObjectId.is_valid(meeting_req.teacher_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid teacher ID"
        )
    
    # Get teacher details
    teacher = await db.users.find_one({"_id": ObjectId(meeting_req.teacher_id)})
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if teacher.get("role") not in ["teacher", "expert"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a teacher or expert"
        )
    
    # Parse preferred date
    preferred_date = None
    if meeting_req.preferred_date:
        try:
            preferred_date = datetime.fromisoformat(meeting_req.preferred_date.replace('Z', '+00:00'))
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
            )
    
    # Create meeting
    meeting_data = {
        "student_id": ObjectId(current_user["_id"]),
        "student_name": current_user.get("full_name", current_user.get("username")),
        "student_email": current_user.get("email"),
        "teacher_id": ObjectId(meeting_req.teacher_id),
        "teacher_name": teacher.get("full_name", teacher.get("username")),
        "teacher_email": teacher.get("email"),
        "title": meeting_req.title,
        "description": meeting_req.description,
        "topic": meeting_req.topic,
        "preferred_date": preferred_date,
        "duration_minutes": meeting_req.duration_minutes,
        "status": "pending",
        "requested_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "teacher_notified": True,
        "student_notified": False
    }
    
    result = await db.meetings.insert_one(meeting_data)
    meeting_data["_id"] = str(result.inserted_id)
    
    # Create notification for teacher
    notification_data = {
        "user_id": ObjectId(meeting_req.teacher_id),
        "notification_type": "meeting_request",
        "title": "New Meeting Request",
        "message": f"{current_user.get('full_name', current_user.get('username'))} has requested a meeting about {meeting_req.topic}",
        "related_id": result.inserted_id,
        "related_type": "meeting",
        "action_url": f"/meetings/{result.inserted_id}",
        "sender_id": ObjectId(current_user["_id"]),
        "sender_name": current_user.get("full_name", current_user.get("username")),
        "created_at": datetime.utcnow()
    }
    
    await db.notifications.insert_one(notification_data)
    
    # Convert ObjectIds for response
    meeting_data["student_id"] = str(meeting_data["student_id"])
    meeting_data["teacher_id"] = str(meeting_data["teacher_id"])
    
    return {
        "message": "Meeting request sent successfully",
        "meeting": meeting_data
    }


@router.get("/my-requests")
async def get_my_meetings(
    status_filter: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get meetings for current user (student sees their requests, teacher sees incoming requests)"""
    query = {}
    
    if current_user.get("role") == "student":
        query["student_id"] = ObjectId(current_user["_id"])
    elif current_user.get("role") in ["teacher", "expert"]:
        query["teacher_id"] = ObjectId(current_user["_id"])
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid role for meetings"
        )
    
    if status_filter:
        query["status"] = status_filter
    
    meetings = await db.meetings.find(query).sort("requested_at", -1).to_list(None)
    
    # Convert ObjectIds
    for meeting in meetings:
        meeting["_id"] = str(meeting["_id"])
        meeting["student_id"] = str(meeting["student_id"])
        meeting["teacher_id"] = str(meeting["teacher_id"])
    
    return meetings


@router.get("/pending")
async def get_pending_meetings(
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get pending meeting requests for teachers/experts"""
    if current_user.get("role") not in ["teacher", "expert"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers and experts can view pending meetings"
        )
    
    meetings = await db.meetings.find({
        "teacher_id": ObjectId(current_user["_id"]),
        "status": "pending"
    }).sort("requested_at", -1).to_list(None)
    
    # Convert ObjectIds
    for meeting in meetings:
        meeting["_id"] = str(meeting["_id"])
        meeting["student_id"] = str(meeting["student_id"])
        meeting["teacher_id"] = str(meeting["teacher_id"])
    
    return meetings


@router.post("/{meeting_id}/approve")
async def approve_meeting(
    meeting_id: str,
    approval: MeetingApproval,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Approve a meeting request and provide Google Meet link"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id)})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Only the assigned teacher can approve
    if str(meeting["teacher_id"]) != current_user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only approve your own meeting requests"
        )
    
    if meeting["status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve meeting with status: {meeting['status']}"
        )
    
    # Parse scheduled date
    try:
        scheduled_date = datetime.fromisoformat(approval.scheduled_date.replace('Z', '+00:00'))
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
        )
    
    # Update meeting
    await db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {
            "$set": {
                "status": "approved",
                "scheduled_date": scheduled_date,
                "google_meet_link": approval.google_meet_link,
                "teacher_notes": approval.teacher_notes,
                "updated_at": datetime.utcnow(),
                "student_notified": True
            }
        }
    )
    
    # Create notification for student
    notification_data = {
        "user_id": meeting["student_id"],
        "notification_type": "meeting_approved",
        "title": "Meeting Approved",
        "message": f"Your meeting with {meeting['teacher_name']} has been approved for {scheduled_date.strftime('%B %d, %Y at %I:%M %p')}",
        "related_id": ObjectId(meeting_id),
        "related_type": "meeting",
        "action_url": f"/meetings/{meeting_id}",
        "sender_id": ObjectId(current_user["_id"]),
        "sender_name": current_user.get("full_name", current_user.get("username")),
        "metadata": {"google_meet_link": approval.google_meet_link},
        "created_at": datetime.utcnow()
    }
    
    await db.notifications.insert_one(notification_data)
    
    return {
        "message": "Meeting approved successfully",
        "google_meet_link": approval.google_meet_link
    }


@router.post("/{meeting_id}/reject")
async def reject_meeting(
    meeting_id: str,
    rejection: MeetingRejection,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Reject a meeting request"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id)})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Only the assigned teacher can reject
    if str(meeting["teacher_id"]) != current_user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only reject your own meeting requests"
        )
    
    if meeting["status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reject meeting with status: {meeting['status']}"
        )
    
    # Update meeting
    await db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {
            "$set": {
                "status": "rejected",
                "teacher_notes": rejection.teacher_notes,
                "updated_at": datetime.utcnow(),
                "student_notified": True
            }
        }
    )
    
    # Create notification for student
    notification_data = {
        "user_id": meeting["student_id"],
        "notification_type": "meeting_rejected",
        "title": "Meeting Request Declined",
        "message": f"Your meeting request with {meeting['teacher_name']} was declined",
        "related_id": ObjectId(meeting_id),
        "related_type": "meeting",
        "action_url": f"/meetings/{meeting_id}",
        "sender_id": ObjectId(current_user["_id"]),
        "sender_name": current_user.get("full_name", current_user.get("username")),
        "created_at": datetime.utcnow()
    }
    
    await db.notifications.insert_one(notification_data)
    
    return {"message": "Meeting rejected"}


@router.get("/{meeting_id}")
async def get_meeting_details(
    meeting_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get meeting details"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id)})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Check permission
    user_id = current_user["_id"]
    if str(meeting["student_id"]) != user_id and str(meeting["teacher_id"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this meeting"
        )
    
    # Convert ObjectIds
    meeting["_id"] = str(meeting["_id"])
    meeting["student_id"] = str(meeting["student_id"])
    meeting["teacher_id"] = str(meeting["teacher_id"])
    
    return meeting
