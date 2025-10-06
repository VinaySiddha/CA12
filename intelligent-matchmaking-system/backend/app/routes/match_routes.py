"""
Match routes for handling matchmaking requests
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_active_user
from app.core.database import get_matches_collection, get_users_collection
from app.schemas.match_schema import (
    MatchRequest, MatchResponse, MatchCreate, StudySessionCreate,
    StudyGroupCreate, StudyGroupResponse, StudyGroupJoinRequest
)
from app.services.matchmaking_service import matchmaking_service
from app.models.match_model import MatchModel, StudyGroupModel
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/find-matches", response_model=List[dict])
async def find_matches(
    match_request: MatchRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """Find potential matches based on user preferences"""
    try:
        matches = await matchmaking_service.find_potential_matches(
            user_id=str(current_user["_id"]),
            match_type=match_request.match_type,
            limit=10
        )
        return matches
    except Exception as e:
        logger.error(f"Error finding matches: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to find matches"
        )


@router.post("/create", response_model=dict)
async def create_match(
    match_data: MatchCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new match request"""
    matches_collection = get_matches_collection()
    users_collection = get_users_collection()
    
    # Verify mentee exists
    try:
        mentee = await users_collection.find_one({"_id": ObjectId(match_data.mentee_id)})
        if not mentee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mentee not found"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid mentee ID"
        )
    
    # Calculate match score
    mentor = current_user
    match_score = await matchmaking_service._calculate_match_score(
        mentee, mentor, match_data.match_type
    )
    
    # Create match
    new_match = MatchModel(
        mentor_id=ObjectId(str(current_user["_id"])),
        mentee_id=ObjectId(match_data.mentee_id),
        match_type=match_data.match_type,
        topics=match_data.topics,
        match_score=match_score,
        max_sessions=match_data.max_sessions,
        session_duration_preference=match_data.session_duration_preference
    )
    
    result = await matches_collection.insert_one(new_match.dict(by_alias=True, exclude={"id"}))
    
    if result.inserted_id:
        return {"message": "Match created successfully", "match_id": str(result.inserted_id)}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create match"
        )


@router.get("/my-matches", response_model=List[MatchResponse])
async def get_my_matches(
    status_filter: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_active_user)
):
    """Get current user's matches"""
    matches_collection = get_matches_collection()
    users_collection = get_users_collection()
    
    # Build filter
    match_filter = {
        "$or": [
            {"mentor_id": current_user["_id"]},
            {"mentee_id": current_user["_id"]}
        ]
    }
    
    if status_filter:
        match_filter["status"] = status_filter
    
    # Get matches
    matches = []
    async for match in matches_collection.find(match_filter):
        # Get partner information
        partner_id = match["mentee_id"] if match["mentor_id"] == current_user["_id"] else match["mentor_id"]
        partner = await users_collection.find_one(
            {"_id": partner_id},
            {"username": 1, "full_name": 1, "profile": 1}
        )
        
        match_data = {
            "id": str(match["_id"]),
            "mentor_id": str(match["mentor_id"]),
            "mentee_id": str(match["mentee_id"]),
            "match_type": match["match_type"],
            "topics": match["topics"],
            "match_score": match["match_score"],
            "status": match["status"],
            "created_at": match["created_at"],
            "accepted_at": match.get("accepted_at"),
            "sessions": [
                {
                    "session_id": str(session["session_id"]),
                    "scheduled_time": session["scheduled_time"],
                    "duration_minutes": session["duration_minutes"],
                    "topic": session["topic"],
                    "location": session.get("location"),
                    "status": session["status"],
                    "notes": session.get("notes")
                }
                for session in match.get("sessions", [])
            ],
            "partner": {
                "id": str(partner["_id"]),
                "username": partner["username"],
                "full_name": partner["full_name"]
            } if partner else None
        }
        matches.append(match_data)
    
    return matches


@router.put("/{match_id}/accept")
async def accept_match(
    match_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Accept a match request"""
    matches_collection = get_matches_collection()
    
    try:
        result = await matches_collection.update_one(
            {
                "_id": ObjectId(match_id),
                "$or": [
                    {"mentor_id": current_user["_id"]},
                    {"mentee_id": current_user["_id"]}
                ],
                "status": "pending"
            },
            {
                "$set": {
                    "status": "accepted",
                    "accepted_at": "2025-01-01T00:00:00Z"
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match not found or already processed"
            )
        
        return {"message": "Match accepted successfully"}
    
    except Exception as e:
        logger.error(f"Error accepting match: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to accept match"
        )


@router.put("/{match_id}/decline")
async def decline_match(
    match_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Decline a match request"""
    matches_collection = get_matches_collection()
    
    try:
        result = await matches_collection.update_one(
            {
                "_id": ObjectId(match_id),
                "$or": [
                    {"mentor_id": current_user["_id"]},
                    {"mentee_id": current_user["_id"]}
                ],
                "status": "pending"
            },
            {"$set": {"status": "declined"}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match not found or already processed"
            )
        
        return {"message": "Match declined"}
    
    except Exception as e:
        logger.error(f"Error declining match: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to decline match"
        )


@router.post("/{match_id}/sessions")
async def schedule_session(
    match_id: str,
    session_data: StudySessionCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Schedule a new study session"""
    matches_collection = get_matches_collection()
    
    try:
        # Verify match exists and user is part of it
        match = await matches_collection.find_one({
            "_id": ObjectId(match_id),
            "$or": [
                {"mentor_id": current_user["_id"]},
                {"mentee_id": current_user["_id"]}
            ],
            "status": "accepted"
        })
        
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match not found or not accessible"
            )
        
        # Create new session
        new_session = {
            "session_id": ObjectId(),
            "scheduled_time": session_data.scheduled_time,
            "duration_minutes": session_data.duration_minutes,
            "topic": session_data.topic,
            "location": session_data.location,
            "status": "scheduled",
            "notes": session_data.notes
        }
        
        result = await matches_collection.update_one(
            {"_id": ObjectId(match_id)},
            {"$push": {"sessions": new_session}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to schedule session"
            )
        
        return {
            "message": "Session scheduled successfully",
            "session_id": str(new_session["session_id"])
        }
    
    except Exception as e:
        logger.error(f"Error scheduling session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to schedule session"
        )


# Study Groups
@router.post("/study-groups", response_model=dict)
async def create_study_group(
    group_data: StudyGroupCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new study group"""
    matches_collection = get_matches_collection()
    
    new_group = StudyGroupModel(
        name=group_data.name,
        description=group_data.description,
        topic=group_data.topic,
        max_members=group_data.max_members,
        creator_id=ObjectId(str(current_user["_id"])),
        member_ids=[ObjectId(str(current_user["_id"]))],
        meeting_schedule=group_data.meeting_schedule,
        meeting_location=group_data.meeting_location
    )
    
    result = await matches_collection.insert_one(new_group.dict(by_alias=True, exclude={"id"}))
    
    if result.inserted_id:
        return {"message": "Study group created successfully", "group_id": str(result.inserted_id)}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create study group"
        )


@router.get("/study-groups", response_model=List[StudyGroupResponse])
async def get_study_groups(
    topic: Optional[str] = Query(None),
    limit: int = Query(10, le=50)
):
    """Get available study groups"""
    matches_collection = get_matches_collection()
    
    # Build filter
    group_filter = {"status": "active"}
    if topic:
        group_filter["topic"] = {"$regex": topic, "$options": "i"}
    
    groups = []
    async for group in matches_collection.find(group_filter).limit(limit):
        group_data = {
            "id": str(group["_id"]),
            "name": group["name"],
            "description": group.get("description"),
            "topic": group["topic"],
            "max_members": group["max_members"],
            "member_count": len(group.get("member_ids", [])),
            "creator_id": str(group["creator_id"]),
            "status": group["status"],
            "created_at": group["created_at"],
            "meeting_schedule": group.get("meeting_schedule"),
            "meeting_location": group["meeting_location"]
        }
        groups.append(group_data)
    
    return groups


@router.post("/study-groups/{group_id}/join")
async def join_study_group(
    group_id: str,
    join_request: StudyGroupJoinRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """Join a study group"""
    matches_collection = get_matches_collection()
    
    try:
        # Check if group exists and has space
        group = await matches_collection.find_one({"_id": ObjectId(group_id)})
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study group not found"
            )
        
        if len(group.get("member_ids", [])) >= group["max_members"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Study group is full"
            )
        
        if current_user["_id"] in group.get("member_ids", []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already a member of this group"
            )
        
        # Add user to group
        result = await matches_collection.update_one(
            {"_id": ObjectId(group_id)},
            {"$push": {"member_ids": current_user["_id"]}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to join group"
            )
        
        return {"message": "Successfully joined study group"}
    
    except Exception as e:
        logger.error(f"Error joining study group: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to join study group"
        )


@router.get("/ml-recommendations", response_model=List[dict])
async def get_ml_recommendations(
    limit: int = Query(5, ge=1, le=20),
    current_user: dict = Depends(get_current_active_user)
):
    """Get ML-based user recommendations"""
    try:
        recommendations = await matchmaking_service.find_ml_recommendations(
            user_id=str(current_user["_id"]),
            limit=limit
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error getting ML recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get ML recommendations"
        )


@router.get("/topic-recommendations", response_model=List[str])
async def get_topic_recommendations(
    limit: int = Query(5, ge=1, le=20),
    current_user: dict = Depends(get_current_active_user)
):
    """Get ML-based topic recommendations"""
    try:
        recommendations = await matchmaking_service.get_topic_recommendations(
            user_id=str(current_user["_id"]),
            limit=limit
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error getting topic recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get topic recommendations"
        )