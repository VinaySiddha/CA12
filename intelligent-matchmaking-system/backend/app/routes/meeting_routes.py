"""
Meeting Routes - API endpoints for meeting/event management
Handles meeting creation, registration, feedback, and discussion groups
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from ..core.database import get_database
from ..core.security import get_current_user
from ..schemas.meeting_schema import MeetingCreate, MeetingUpdate, MeetingResponse, MeetingListResponse
from ..utils.logger import get_logger

router = APIRouter(prefix="/meetings", tags=["meetings"])

# Helper function to convert meeting document to response model
def convert_meeting_to_response(meeting_doc: dict, current_user_id: str) -> dict:
    """Convert MongoDB meeting document to API response format"""
    meeting_doc["id"] = str(meeting_doc["_id"])
    meeting_doc["teacher_id"] = str(meeting_doc["teacher_id"])
    meeting_doc["is_registered"] = str(current_user_id) in [str(reg["user_id"]) for reg in meeting_doc.get("registered_students", [])]
    meeting_doc["is_liked"] = str(current_user_id) in [str(like_id) for like_id in meeting_doc.get("likes", [])]
    
    # Convert ObjectIds in nested structures
    if "registered_students" in meeting_doc:
        for student in meeting_doc["registered_students"]:
            if "user_id" in student:
                student["user_id"] = str(student["user_id"])
    
    if "attendees" in meeting_doc:
        for attendee in meeting_doc["attendees"]:
            if "user_id" in attendee:
                attendee["user_id"] = str(attendee["user_id"])
    
    if "likes" in meeting_doc:
        meeting_doc["likes"] = [str(like_id) for like_id in meeting_doc["likes"]]
    
    if "discussion_group_id" in meeting_doc and meeting_doc["discussion_group_id"]:
        meeting_doc["discussion_group_id"] = str(meeting_doc["discussion_group_id"])
    
    return meeting_doc

@router.post("/", response_model=MeetingResponse)
async def create_meeting(
    meeting_data: MeetingCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Create a new meeting/event (teachers only)"""
    # Only teachers can create meetings
    if current_user.get("role") not in ["teacher", "expert"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers and experts can create meetings"
        )
    
    # Create meeting document
    meeting_doc = {
        "title": meeting_data.title,
        "description": meeting_data.description,
        "teacher_id": ObjectId(current_user["_id"]),
        "teacher_name": current_user.get("full_name", current_user.get("username", "")),
        "teacher_email": current_user.get("email", ""),
        "subject": meeting_data.subject,
        "category": meeting_data.category,
        "scheduled_date": meeting_data.scheduled_date,
        "duration_minutes": meeting_data.duration_minutes,
        "timezone": meeting_data.timezone,
        "meeting_platform": meeting_data.meeting_platform,
        "meeting_link": meeting_data.meeting_link,
        "meeting_id": meeting_data.meeting_id,
        "passcode": meeting_data.passcode,
        "max_participants": meeting_data.max_participants,
        "registered_students": [],
        "attendees": [],
        "is_recurring": meeting_data.is_recurring,
        "recurrence_pattern": meeting_data.recurrence_pattern,
        "is_recorded": meeting_data.is_recorded,
        "recording_url": None,
        "status": "scheduled",
        "is_active": True,
        "is_public": meeting_data.is_public,
        "prerequisites": meeting_data.prerequisites,
        "materials_needed": meeting_data.materials_needed,
        "agenda": meeting_data.agenda,
        "tags": meeting_data.tags,
        "difficulty_level": meeting_data.difficulty_level,
        "likes": [],
        "rating": 0.0,
        "feedback_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "discussion_group_id": None
    }
    
    result = await db.meetings.insert_one(meeting_doc)
    meeting_doc["_id"] = result.inserted_id
    
    logger.info(f"Meeting created by teacher {current_user['_id']}: {result.inserted_id}")
    
    return convert_meeting_to_response(meeting_doc, current_user["_id"])

@router.get("/", response_model=MeetingListResponse)
async def list_meetings(
    search: Optional[str] = Query(None, description="Search term"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    category: Optional[str] = Query(None, description="Filter by category"),
    teacher_id: Optional[str] = Query(None, description="Filter by teacher ID"),
    difficulty_level: Optional[str] = Query(None, description="Filter by difficulty level"),
    status: Optional[str] = Query(None, description="Filter by status"),
    date_from: Optional[datetime] = Query(None, description="Filter meetings from this date"),
    date_to: Optional[datetime] = Query(None, description="Filter meetings to this date"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("scheduled_date", description="Sort by field"),
    sort_order: int = Query(1, description="Sort order (1 for asc, -1 for desc)"),
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """List meetings with filtering and pagination"""
    try:
        # Build query
        query = {"is_active": True}
        
        # Role-based filtering
        if current_user.get("role") == "student":
            # Students can only see public meetings or meetings they're registered for
            query["is_public"] = True
        
        # Search functionality
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"subject": {"$regex": search, "$options": "i"}},
                {"teacher_name": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [{"$regex": search, "$options": "i"}]}}
            ]
        
        # Subject filter
        if subject:
            query["subject"] = {"$regex": subject, "$options": "i"}
        
        # Category filter
        if category:
            query["category"] = category
        
        # Teacher filter
        if teacher_id and ObjectId.is_valid(teacher_id):
            query["teacher_id"] = ObjectId(teacher_id)
        
        # Difficulty level filter
        if difficulty_level:
            query["difficulty_level"] = difficulty_level
        
        # Status filter
        if status:
            query["status"] = status
        
        # Date range filter
        if date_from or date_to:
            date_query = {}
            if date_from:
                date_query["$gte"] = date_from
            if date_to:
                date_query["$lte"] = date_to
            query["scheduled_date"] = date_query
        
        # Count total documents
        total = await db.meetings.count_documents(query)
        
        # Calculate pagination
        skip = (page - 1) * limit
        total_pages = (total + limit - 1) // limit
        
        # Build sort
        sort_criteria = [(sort_by, sort_order)]
        
        # Execute query
        cursor = db.meetings.find(query).sort(sort_criteria).skip(skip).limit(limit)
        meetings = await cursor.to_list(length=limit)
        
        # Convert to response format
        meeting_responses = []
        for meeting in meetings:
            meeting_response = convert_meeting_to_response(meeting, current_user["_id"])
            meeting_responses.append(meeting_response)
        
        return {
            "meetings": meeting_responses,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    
    except Exception as e:
        logger.error(f"Error listing meetings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve meetings"
        )

@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get a specific meeting by ID"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID format"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id), "is_active": True})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Check if user has permission to view this meeting
    if (current_user.get("role") == "student" and 
        not meeting.get("is_public", True) and 
        str(current_user["_id"]) not in [str(reg["user_id"]) for reg in meeting.get("registered_students", [])]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this meeting"
        )
    
    return convert_meeting_to_response(meeting, current_user["_id"])

@router.put("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: str,
    meeting_data: MeetingUpdate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Update a meeting (teachers only)"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID format"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id), "is_active": True})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Only the teacher who created the meeting can update it
    if str(meeting["teacher_id"]) != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the meeting creator can update this meeting"
        )
    
    # Build update document
    update_doc = {"updated_at": datetime.utcnow()}
    
    # Update fields that are provided
    update_fields = meeting_data.dict(exclude_unset=True)
    update_doc.update(update_fields)
    
    # Update the meeting
    result = await db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {"$set": update_doc}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No changes were made to the meeting"
        )
    
    # Fetch updated meeting
    updated_meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id)})
    
    logger.info(f"Meeting {meeting_id} updated by teacher {current_user['_id']}")
    
    return convert_meeting_to_response(updated_meeting, current_user["_id"])

@router.delete("/{meeting_id}")
async def delete_meeting(
    meeting_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Delete (soft delete) a meeting (teachers only)"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID format"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id), "is_active": True})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Only the teacher who created the meeting can delete it
    if str(meeting["teacher_id"]) != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the meeting creator can delete this meeting"
        )
    
    # Soft delete the meeting
    result = await db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete meeting"
        )
    
    logger.info(f"Meeting {meeting_id} deleted by teacher {current_user['_id']}")
    
    return {"message": "Meeting deleted successfully"}

@router.post("/{meeting_id}/register")
async def register_for_meeting(
    meeting_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Register for a meeting (students only)"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID format"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id), "is_active": True})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Check if meeting is open for registration
    if meeting["status"] != "scheduled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Meeting is not open for registration"
        )
    
    # Check if student is already registered
    user_id = str(current_user["_id"])
    if user_id in [str(reg["user_id"]) for reg in meeting.get("registered_students", [])]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already registered for this meeting"
        )
    
    # Check max participants limit
    max_participants = meeting.get("max_participants", 0)
    current_registrations = len(meeting.get("registered_students", []))
    
    if max_participants > 0 and current_registrations >= max_participants:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Meeting has reached maximum participants limit"
        )
    
    # Register the student
    registration_data = {
        "user_id": ObjectId(current_user["_id"]),
        "username": current_user.get("username", ""),
        "full_name": current_user.get("full_name", ""),
        "email": current_user.get("email", ""),
        "registered_at": datetime.utcnow(),
        "status": "registered"
    }
    
    result = await db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {
            "$push": {"registered_students": registration_data},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register for meeting"
        )
    
    logger.info(f"Student {current_user['_id']} registered for meeting {meeting_id}")
    
    return {"message": "Successfully registered for meeting"}

@router.delete("/{meeting_id}/register")
async def unregister_from_meeting(
    meeting_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Unregister from a meeting"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID format"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id), "is_active": True})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Check if student is registered
    user_id = str(current_user["_id"])
    if user_id not in [str(reg["user_id"]) for reg in meeting.get("registered_students", [])]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not registered for this meeting"
        )
    
    # Unregister the student
    result = await db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {
            "$pull": {"registered_students": {"user_id": ObjectId(current_user["_id"])}},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to unregister from meeting"
        )
    
    logger.info(f"Student {current_user['_id']} unregistered from meeting {meeting_id}")
    
    return {"message": "Successfully unregistered from meeting"}

@router.post("/{meeting_id}/like")
async def like_meeting(
    meeting_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Like or unlike a meeting"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID format"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id), "is_active": True})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    user_id = ObjectId(current_user["_id"])
    likes = meeting.get("likes", [])
    
    if user_id in likes:
        # Unlike the meeting
        result = await db.meetings.update_one(
            {"_id": ObjectId(meeting_id)},
            {
                "$pull": {"likes": user_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        message = "Meeting unliked successfully"
        action = "unliked"
    else:
        # Like the meeting
        result = await db.meetings.update_one(
            {"_id": ObjectId(meeting_id)},
            {
                "$addToSet": {"likes": user_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        message = "Meeting liked successfully"
        action = "liked"
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update meeting likes"
        )
    
    # Get updated like count
    updated_meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id)})
    like_count = len(updated_meeting.get("likes", []))
    
    logger.info(f"Meeting {meeting_id} {action} by user {current_user['_id']}")
    
    return {
        "message": message,
        "like_count": like_count,
        "is_liked": action == "liked"
    }

@router.get("/{meeting_id}/registrations")
async def get_meeting_registrations(
    meeting_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get meeting registrations (teachers only)"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID format"
        )
    
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id), "is_active": True})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Only the teacher who created the meeting can view registrations
    if str(meeting["teacher_id"]) != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the meeting creator can view registrations"
        )
    
    registrations = meeting.get("registered_students", [])
    
    # Convert ObjectIds to strings
    for registration in registrations:
        if "user_id" in registration:
            registration["user_id"] = str(registration["user_id"])
    
    return {
        "meeting_id": meeting_id,
        "registrations": registrations,
        "total_registrations": len(registrations),
        "max_participants": meeting.get("max_participants", 0)
    }