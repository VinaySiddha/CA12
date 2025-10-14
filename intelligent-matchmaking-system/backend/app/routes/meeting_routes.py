"""
Meeting Routes - API endpoints for scheduling meetings between students and teachers
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.database import get_database
from app.core.security import get_current_user
from app.models.meeting_model import Meeting, MeetingFeedback
from app.models.user_model import UserModel

router = APIRouter(prefix="/meetings", tags=["meetings"])


class MeetingRequest(BaseModel):
    """Request schema for creating a meeting"""
    teacher_id: str = Field(..., description="Teacher/Expert user ID")
    title: str = Field(..., description="Meeting title")
    description: str = Field(..., description="Purpose of meeting")
    topic: str = Field(..., description="Topic to discuss")
    preferred_date: Optional[str] = Field(None, description="Preferred date/time (ISO format)")
    duration_minutes: int = Field(default=30, ge=15, le=180, description="Duration (15-180 minutes)")


class MeetingApproval(BaseModel):
    """Request schema for approving a meeting"""
    scheduled_date: str = Field(..., description="Confirmed date/time (ISO format)")
    google_meet_link: str = Field(..., description="Google Meet URL")
    teacher_notes: Optional[str] = Field(None, description="Notes for student")


class MeetingRejection(BaseModel):
    """Request schema for rejecting a meeting"""
    teacher_notes: str = Field(..., description="Reason for rejection")


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
