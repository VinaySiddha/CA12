"""
Discussion Group Routes - API endpoints for meeting-based discussions
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, WebSocket, WebSocketDisconnect
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime, timezone, timedelta
import logging
import json

from app.core.database import get_database
from app.core.security import get_current_user, get_current_active_user
from app.models.discussion_model import (
    DiscussionGroup, DiscussionMessage, DiscussionParticipant, 
    MessageReaction, PinnedMessage, PyObjectId
)
from app.schemas.discussion_schema import (
    DiscussionGroupCreate, DiscussionGroupUpdate, DiscussionGroupResponse,
    MessageCreate, MessageUpdate, MessageResponse, MessageListResponse,
    ParticipantResponse, ReactionCreate, PinMessageRequest,
    DiscussionGroupListResponse, MessageSearchQuery, GroupStats
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/discussions", tags=["discussions"])

# WebSocket connection manager for real-time messaging
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, group_id: str):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = []
        self.active_connections[group_id].append(websocket)

    def disconnect(self, websocket: WebSocket, group_id: str):
        if group_id in self.active_connections:
            self.active_connections[group_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_group(self, message: str, group_id: str):
        if group_id in self.active_connections:
            for connection in self.active_connections[group_id]:
                try:
                    await connection.send_text(message)
                except:
                    # Remove dead connections
                    self.active_connections[group_id].remove(connection)

manager = ConnectionManager()


# Helper functions
def convert_group_to_response(group: dict, current_user_id: str = None) -> dict:
    """Convert group document to response format"""
    response = {
        "id": str(group["_id"]),
        "meeting_id": str(group["meeting_id"]),
        "meeting_title": group["meeting_title"],
        "title": group["title"],
        "description": group.get("description", ""),
        "moderator_id": str(group["moderator_id"]),
        "moderator_name": group["moderator_name"],
        "participant_count": len(group.get("participants", [])),
        "message_count": group.get("message_count", 0),
        "is_active": group.get("is_active", True),
        "is_open": group.get("is_open", True),
        "auto_add_registered": group.get("auto_add_registered", True),
        "last_activity": group.get("last_activity"),
        "created_at": group["created_at"],
        "updated_at": group["updated_at"]
    }
    
    if current_user_id:
        user_id = ObjectId(current_user_id)
        response["is_participant"] = user_id in group.get("participants", [])
        response["is_moderator"] = user_id == group.get("moderator_id")
        # TODO: Calculate unread count
        response["unread_count"] = 0
    
    return response


def convert_message_to_response(message: dict, current_user_id: str = None) -> dict:
    """Convert message document to response format"""
    response = {
        "id": str(message["_id"]),
        "discussion_group_id": str(message["discussion_group_id"]),
        "sender_id": str(message["sender_id"]),
        "sender_name": message["sender_name"],
        "sender_role": message["sender_role"],
        "message_type": message.get("message_type", "text"),
        "content": message["content"],
        "formatted_content": message.get("formatted_content"),
        "attachments": message.get("attachments", []),
        "reply_to_id": str(message["reply_to_id"]) if message.get("reply_to_id") else None,
        "thread_count": message.get("thread_count", 0),
        "is_edited": message.get("is_edited", False),
        "edited_at": message.get("edited_at"),
        "reactions": {},
        "reaction_counts": {},
        "mentions": [str(uid) for uid in message.get("mentions", [])],
        "created_at": message["created_at"],
        "updated_at": message["updated_at"]
    }
    
    # Process reactions
    reactions = message.get("reactions", {})
    for reaction_type, user_ids in reactions.items():
        response["reactions"][reaction_type] = [{"user_id": str(uid), "user_name": ""} for uid in user_ids]
        response["reaction_counts"][reaction_type] = len(user_ids)
    
    if current_user_id:
        user_id = ObjectId(current_user_id)
        response["can_edit"] = user_id == message.get("sender_id")
        response["can_delete"] = user_id == message.get("sender_id") or current_user_id  # TODO: Check if moderator
        
        # Check user's reaction
        for reaction_type, user_ids in reactions.items():
            if user_id in user_ids:
                response["user_reaction"] = reaction_type
                break
    
    return response


@router.post("/{meeting_id}/group", status_code=status.HTTP_201_CREATED, response_model=DiscussionGroupResponse)
async def create_discussion_group(
    meeting_id: str,
    group_data: DiscussionGroupCreate,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Create a discussion group for a meeting (teachers only)"""
    if not ObjectId.is_valid(meeting_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting ID"
        )
    
    # Get meeting details
    meeting = await db.meetings.find_one({"_id": ObjectId(meeting_id)})
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    # Only the teacher who created the meeting can create discussion group
    if str(meeting["teacher_id"]) != current_user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the meeting creator can create discussion groups"
        )
    
    # Check if discussion group already exists
    existing_group = await db.discussion_groups.find_one({"meeting_id": ObjectId(meeting_id)})
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discussion group already exists for this meeting"
        )
    
    # Create discussion group
    group_doc = {
        "meeting_id": ObjectId(meeting_id),
        "meeting_title": meeting["title"],
        "title": group_data.title,
        "description": group_data.description,
        "moderator_id": ObjectId(current_user["_id"]),
        "moderator_name": current_user.get("full_name", current_user.get("username", "")),
        "participants": [ObjectId(current_user["_id"])],  # Moderator is automatically a participant
        "is_active": True,
        "is_open": group_data.is_open,
        "auto_add_registered": group_data.auto_add_registered,
        "message_count": 0,
        "last_activity": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # If auto_add_registered is True, add all registered students
    if group_data.auto_add_registered:
        registered_students = meeting.get("registered_students", [])
        for student_id in registered_students:
            if student_id not in group_doc["participants"]:
                group_doc["participants"].append(student_id)
    
    result = await db.discussion_groups.insert_one(group_doc)
    group_doc["_id"] = result.inserted_id
    
    # Update meeting with discussion group ID
    await db.meetings.update_one(
        {"_id": ObjectId(meeting_id)},
        {"$set": {"discussion_group_id": result.inserted_id}}
    )
    
    # Create participant records
    for participant_id in group_doc["participants"]:
        participant_doc = {
            "discussion_group_id": result.inserted_id,
            "user_id": participant_id,
            "user_name": "",  # Will be filled when we get user details
            "user_role": "teacher" if participant_id == ObjectId(current_user["_id"]) else "student",
            "joined_at": datetime.utcnow(),
            "last_seen": None,
            "message_count": 0,
            "can_post": True,
            "can_upload": True,
            "is_moderator": participant_id == ObjectId(current_user["_id"]),
            "is_active": True
        }
        await db.discussion_participants.insert_one(participant_doc)
    
    logger.info(f"Discussion group created for meeting {meeting_id} by {current_user['_id']}")
    
    return convert_group_to_response(group_doc, current_user["_id"])


@router.get("/{group_id}", response_model=DiscussionGroupResponse)
async def get_discussion_group(
    group_id: str,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get discussion group details"""
    if not ObjectId.is_valid(group_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid group ID"
        )
    
    group = await db.discussion_groups.find_one({"_id": ObjectId(group_id)})
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion group not found"
        )
    
    # Check if user is a participant
    user_id = ObjectId(current_user["_id"])
    if user_id not in group.get("participants", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this discussion group"
        )
    
    return convert_group_to_response(group, current_user["_id"])


@router.post("/{group_id}/join")
async def join_discussion_group(
    group_id: str,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Join a discussion group"""
    if not ObjectId.is_valid(group_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid group ID"
        )
    
    group = await db.discussion_groups.find_one({"_id": ObjectId(group_id)})
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion group not found"
        )
    
    if not group.get("is_open", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This discussion group is closed to new participants"
        )
    
    user_id = ObjectId(current_user["_id"])
    
    # Check if already a participant
    if user_id in group.get("participants", []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already a participant in this group"
        )
    
    # Check if user is registered for the associated meeting (for students)
    if current_user.get("role") == "student":
        meeting = await db.meetings.find_one({"_id": group["meeting_id"]})
        if user_id not in meeting.get("registered_students", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be registered for the meeting to join its discussion group"
            )
    
    # Add user to participants
    await db.discussion_groups.update_one(
        {"_id": ObjectId(group_id)},
        {"$push": {"participants": user_id}}
    )
    
    # Create participant record
    participant_doc = {
        "discussion_group_id": ObjectId(group_id),
        "user_id": user_id,
        "user_name": current_user.get("full_name", current_user.get("username", "")),
        "user_role": current_user.get("role", "student"),
        "joined_at": datetime.utcnow(),
        "last_seen": None,
        "message_count": 0,
        "can_post": True,
        "can_upload": True,
        "is_moderator": False,
        "is_active": True
    }
    await db.discussion_participants.insert_one(participant_doc)
    
    logger.info(f"User {current_user['_id']} joined discussion group {group_id}")
    
    return {"message": "Successfully joined discussion group"}


@router.post("/{group_id}/messages", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def post_message(
    group_id: str,
    message_data: MessageCreate,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Post a message to discussion group"""
    if not ObjectId.is_valid(group_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid group ID"
        )
    
    group = await db.discussion_groups.find_one({"_id": ObjectId(group_id)})
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion group not found"
        )
    
    user_id = ObjectId(current_user["_id"])
    
    # Check if user is a participant
    if user_id not in group.get("participants", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this discussion group"
        )
    
    # Check participant permissions
    participant = await db.discussion_participants.find_one({
        "discussion_group_id": ObjectId(group_id),
        "user_id": user_id
    })
    
    if not participant or not participant.get("can_post", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to post messages"
        )
    
    # Validate reply_to_id if provided
    reply_to_message = None
    if message_data.reply_to_id:
        if not ObjectId.is_valid(message_data.reply_to_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reply message ID"
            )
        
        reply_to_message = await db.discussion_messages.find_one({
            "_id": ObjectId(message_data.reply_to_id),
            "discussion_group_id": ObjectId(group_id)
        })
        
        if not reply_to_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reply message not found"
            )
    
    # Create message
    message_doc = {
        "discussion_group_id": ObjectId(group_id),
        "sender_id": user_id,
        "sender_name": current_user.get("full_name", current_user.get("username", "")),
        "sender_role": current_user.get("role", "student"),
        "message_type": message_data.message_type,
        "content": message_data.content,
        "formatted_content": None,  # TODO: Add text formatting
        "attachments": [],
        "reply_to_id": ObjectId(message_data.reply_to_id) if message_data.reply_to_id else None,
        "thread_count": 0,
        "is_edited": False,
        "edited_at": None,
        "is_deleted": False,
        "deleted_at": None,
        "reactions": {},
        "mentions": [ObjectId(mid) for mid in message_data.mentions if ObjectId.is_valid(mid)],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.discussion_messages.insert_one(message_doc)
    message_doc["_id"] = result.inserted_id
    
    # Update group message count and last activity
    await db.discussion_groups.update_one(
        {"_id": ObjectId(group_id)},
        {
            "$inc": {"message_count": 1},
            "$set": {"last_activity": datetime.utcnow()}
        }
    )
    
    # Update participant message count and last seen
    await db.discussion_participants.update_one(
        {"discussion_group_id": ObjectId(group_id), "user_id": user_id},
        {
            "$inc": {"message_count": 1},
            "$set": {"last_seen": datetime.utcnow()}
        }
    )
    
    # If this is a reply, increment thread count
    if reply_to_message:
        await db.discussion_messages.update_one(
            {"_id": ObjectId(message_data.reply_to_id)},
            {"$inc": {"thread_count": 1}}
        )
    
    # Broadcast message to WebSocket connections
    message_response = convert_message_to_response(message_doc, current_user["_id"])
    await manager.broadcast_to_group(
        json.dumps({
            "type": "new_message",
            "data": message_response
        }),
        group_id
    )
    
    logger.info(f"Message posted to group {group_id} by {current_user['_id']}")
    
    return message_response


@router.get("/{group_id}/messages", response_model=MessageListResponse)
async def get_messages(
    group_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Messages per page"),
    before: Optional[str] = Query(None, description="Get messages before this message ID"),
    after: Optional[str] = Query(None, description="Get messages after this message ID"),
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get messages from discussion group with pagination"""
    if not ObjectId.is_valid(group_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid group ID"
        )
    
    # Check if user is a participant
    group = await db.discussion_groups.find_one({"_id": ObjectId(group_id)})
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion group not found"
        )
    
    user_id = ObjectId(current_user["_id"])
    if user_id not in group.get("participants", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this discussion group"
        )
    
    # Build query
    query = {"discussion_group_id": ObjectId(group_id), "is_deleted": False}
    
    if before and ObjectId.is_valid(before):
        query["_id"] = {"$lt": ObjectId(before)}
    elif after and ObjectId.is_valid(after):
        query["_id"] = {"$gt": ObjectId(after)}
    
    # Count total messages
    total_count = await db.discussion_messages.count_documents(query)
    
    # Calculate pagination
    skip = (page - 1) * per_page
    total_pages = (total_count + per_page - 1) // per_page
    
    # Get messages (newest first by default)
    sort_order = [("created_at", -1)]
    if after:  # When getting newer messages, sort ascending
        sort_order = [("created_at", 1)]
    
    messages = await db.discussion_messages.find(query).sort(sort_order).skip(skip).limit(per_page).to_list(None)
    
    # Convert to response format
    message_responses = [convert_message_to_response(msg, current_user["_id"]) for msg in messages]
    
    # If we got messages with 'after' parameter, reverse to maintain chronological order
    if after:
        message_responses.reverse()
    
    return MessageListResponse(
        messages=message_responses,
        total_count=total_count,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        has_more=skip + per_page < total_count
    )


@router.post("/{group_id}/messages/{message_id}/react")
async def react_to_message(
    group_id: str,
    message_id: str,
    reaction_data: ReactionCreate,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """React to a message"""
    if not ObjectId.is_valid(group_id) or not ObjectId.is_valid(message_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid group or message ID"
        )
    
    # Check permissions
    group = await db.discussion_groups.find_one({"_id": ObjectId(group_id)})
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    
    user_id = ObjectId(current_user["_id"])
    if user_id not in group.get("participants", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this discussion group"
        )
    
    # Get message
    message = await db.discussion_messages.find_one({
        "_id": ObjectId(message_id),
        "discussion_group_id": ObjectId(group_id)
    })
    
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
    reactions = message.get("reactions", {})
    reaction_type = reaction_data.reaction_type
    
    # Toggle reaction
    if reaction_type in reactions:
        if user_id in reactions[reaction_type]:
            # Remove reaction
            await db.discussion_messages.update_one(
                {"_id": ObjectId(message_id)},
                {"$pull": {f"reactions.{reaction_type}": user_id}}
            )
            action = "removed"
        else:
            # Add reaction
            await db.discussion_messages.update_one(
                {"_id": ObjectId(message_id)},
                {"$push": {f"reactions.{reaction_type}": user_id}}
            )
            action = "added"
    else:
        # Create new reaction type
        await db.discussion_messages.update_one(
            {"_id": ObjectId(message_id)},
            {"$push": {f"reactions.{reaction_type}": user_id}}
        )
        action = "added"
    
    # Broadcast reaction to WebSocket connections
    await manager.broadcast_to_group(
        json.dumps({
            "type": "message_reaction",
            "data": {
                "message_id": message_id,
                "reaction_type": reaction_type,
                "user_id": current_user["_id"],
                "user_name": current_user.get("full_name", current_user.get("username", "")),
                "action": action
            }
        }),
        group_id
    )
    
    return {"message": f"Reaction {action}"}


@router.get("/my/groups", response_model=DiscussionGroupListResponse)
async def get_my_discussion_groups(
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get discussion groups where current user is a participant"""
    user_id = ObjectId(current_user["_id"])
    
    groups = await db.discussion_groups.find({
        "participants": user_id,
        "is_active": True
    }).sort("last_activity", -1).to_list(None)
    
    group_responses = [convert_group_to_response(group, current_user["_id"]) for group in groups]
    
    return DiscussionGroupListResponse(
        groups=group_responses,
        total_count=len(group_responses)
    )


# WebSocket endpoint for real-time messaging
@router.websocket("/{group_id}/ws")
async def websocket_endpoint(websocket: WebSocket, group_id: str):
    await manager.connect(websocket, group_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle typing indicators, presence, etc.
            message_data = json.loads(data)
            if message_data.get("type") == "typing":
                await manager.broadcast_to_group(data, group_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, group_id)