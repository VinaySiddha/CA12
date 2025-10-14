"""
Chat Routes - API endpoints for messaging between students and teachers
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.database import get_database
from app.core.security import get_current_user
from app.models.chat_model import ChatMessage, Conversation
from app.models.user_model import UserModel

router = APIRouter(prefix="/chat", tags=["chat"])


class MessageCreate(BaseModel):
    """Request schema for sending a message"""
    receiver_id: str = Field(..., description="Receiver user ID")
    content: str = Field(..., description="Message content", min_length=1, max_length=2000)


class ConversationResponse(BaseModel):
    """Response with conversation and unread count"""
    conversation: dict
    unread_count: int


@router.post("/send", status_code=status.HTTP_201_CREATED)
async def send_message(
    message_data: MessageCreate,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Send a message to another user"""
    if not ObjectId.is_valid(message_data.receiver_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid receiver ID"
        )
    
    receiver = await db.users.find_one({"_id": ObjectId(message_data.receiver_id)})
    
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    
    sender_id = ObjectId(current_user["_id"])
    receiver_id = ObjectId(message_data.receiver_id)
    
    # Determine participants (ordered for consistent conversation lookup)
    participant_ids = sorted([sender_id, receiver_id], key=lambda x: str(x))
    
    # Find or create conversation
    conversation = await db.conversations.find_one({
        "participant_ids": participant_ids
    })
    
    if not conversation:
        # Determine who is student and who is teacher
        sender_role = current_user.get("role")
        receiver_role = receiver.get("role")
        
        if sender_role == "student":
            student_id = sender_id
            student_name = current_user.get("full_name", current_user.get("username"))
            teacher_id = receiver_id
            teacher_name = receiver.get("full_name", receiver.get("username"))
        else:
            student_id = receiver_id
            student_name = receiver.get("full_name", receiver.get("username"))
            teacher_id = sender_id
            teacher_name = current_user.get("full_name", current_user.get("username"))
        
        # Create new conversation
        conversation_data = {
            "student_id": student_id,
            "student_name": student_name,
            "teacher_id": teacher_id,
            "teacher_name": teacher_name,
            "participant_ids": participant_ids,
            "last_message": message_data.content[:100],
            "last_message_at": datetime.utcnow(),
            "is_active": True,
            "is_archived": False,
            "student_unread_count": 1 if sender_role != "student" else 0,
            "teacher_unread_count": 1 if sender_role == "student" else 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.conversations.insert_one(conversation_data)
        conversation_id = result.inserted_id
    else:
        conversation_id = conversation["_id"]
        
        # Update conversation
        update_data = {
            "last_message": message_data.content[:100],
            "last_message_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Increment unread count for receiver
        if current_user.get("role") == "student":
            update_data["teacher_unread_count"] = conversation.get("teacher_unread_count", 0) + 1
        else:
            update_data["student_unread_count"] = conversation.get("student_unread_count", 0) + 1
        
        await db.conversations.update_one(
            {"_id": conversation_id},
            {"$set": update_data}
        )
    
    # Create message
    message = {
        "conversation_id": conversation_id,
        "sender_id": sender_id,
        "sender_name": current_user.get("full_name", current_user.get("username")),
        "sender_role": current_user.get("role"),
        "content": message_data.content,
        "message_type": "text",
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    
    result = await db.chat_messages.insert_one(message)
    message["_id"] = str(result.inserted_id)
    
    # Create notification for receiver
    notification_data = {
        "user_id": receiver_id,
        "notification_type": "new_message",
        "title": "New Message",
        "message": f"{current_user.get('full_name', current_user.get('username'))}: {message_data.content[:50]}{'...' if len(message_data.content) > 50 else ''}",
        "related_id": conversation_id,
        "related_type": "conversation",
        "action_url": f"/chat/{conversation_id}",
        "sender_id": sender_id,
        "sender_name": current_user.get("full_name", current_user.get("username")),
        "created_at": datetime.utcnow()
    }
    
    await db.notifications.insert_one(notification_data)
    
    # Convert ObjectIds for response
    message["conversation_id"] = str(message["conversation_id"])
    message["sender_id"] = str(message["sender_id"])
    
    return {
        "message": "Message sent successfully",
        "data": message
    }


@router.get("/conversations")
async def get_conversations(
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get all conversations for current user"""
    user_id = ObjectId(current_user["_id"])
    
    conversations = await db.conversations.find({
        "participant_ids": user_id,
        "is_active": True
    }).sort("last_message_at", -1).to_list(None)
    
    # Add unread count for each conversation
    result = []
    for conv in conversations:
        conv["_id"] = str(conv["_id"])
        conv["student_id"] = str(conv["student_id"])
        conv["teacher_id"] = str(conv["teacher_id"])
        conv["participant_ids"] = [str(pid) for pid in conv["participant_ids"]]
        
        # Get unread count for current user
        if current_user.get("role") == "student":
            conv["my_unread_count"] = conv.get("student_unread_count", 0)
        else:
            conv["my_unread_count"] = conv.get("teacher_unread_count", 0)
        
        result.append(conv)
    
    return result


@router.get("/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    skip: int = 0,
    limit: int = 50,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get messages in a conversation"""
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID"
        )
    
    conversation = await db.conversations.find_one({"_id": ObjectId(conversation_id)})
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Check permission
    user_id = ObjectId(current_user["_id"])
    if user_id not in conversation["participant_ids"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this conversation"
        )
    
    # Get messages
    messages = await db.chat_messages.find({
        "conversation_id": ObjectId(conversation_id)
    }).sort("created_at", -1).skip(skip).limit(limit).to_list(None)
    
    # Mark messages as read
    await db.chat_messages.update_many(
        {
            "conversation_id": ObjectId(conversation_id),
            "sender_id": {"$ne": user_id},
            "is_read": False
        },
        {
            "$set": {
                "is_read": True,
                "read_at": datetime.utcnow()
            }
        }
    )
    
    # Reset unread count
    if current_user.get("role") == "student":
        await db.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"student_unread_count": 0}}
        )
    else:
        await db.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"teacher_unread_count": 0}}
        )
    
    # Convert ObjectIds
    for msg in messages:
        msg["_id"] = str(msg["_id"])
        msg["conversation_id"] = str(msg["conversation_id"])
        msg["sender_id"] = str(msg["sender_id"])
    
    # Reverse to show oldest first
    messages.reverse()
    
    return messages


@router.get("/with/{user_id}")
async def get_conversation_with_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get or create conversation with a specific user"""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    other_user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    sender_id = ObjectId(current_user["_id"])
    receiver_id = ObjectId(user_id)
    
    # Ordered participant IDs
    participant_ids = sorted([sender_id, receiver_id], key=lambda x: str(x))
    
    # Find conversation
    conversation = await db.conversations.find_one({
        "participant_ids": participant_ids
    })
    
    if conversation:
        conversation["_id"] = str(conversation["_id"])
        conversation["student_id"] = str(conversation["student_id"])
        conversation["teacher_id"] = str(conversation["teacher_id"])
        conversation["participant_ids"] = [str(pid) for pid in conversation["participant_ids"]]
        
        return {
            "conversation": conversation,
            "exists": True
        }
    else:
        return {
            "conversation": None,
            "exists": False,
            "other_user": {
                "id": str(other_user["_id"]),
                "name": other_user.get("full_name", other_user.get("username")),
                "role": other_user.get("role")
            }
        }
