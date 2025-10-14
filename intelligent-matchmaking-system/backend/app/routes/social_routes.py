"""
Social Feed Routes - Posts, Comments, Likes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.core.security import get_current_user
from app.core.database import get_database
from app.schemas.post_schema import (
    CreatePostRequest,
    UpdatePostRequest,
    CreateCommentRequest,
    PostResponse,
    CommentResponse
)
from app.models.post_model import PostModel, CommentModel

router = APIRouter()


def get_posts_collection():
    """Get posts collection"""
    db = get_database()
    return db.posts


@router.post("/posts", response_model=dict)
async def create_post(
    post_data: CreatePostRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new post"""
    posts_collection = get_posts_collection()
    
    post = PostModel(
        user_id=str(current_user["_id"]),
        user_name=current_user.get("full_name", current_user.get("email")),
        user_role=current_user.get("role", "student"),
        content=post_data.content,
        media_urls=post_data.media_urls or [],
        tags=post_data.tags or [],
        likes=[],
        comments=[]
    )
    
    result = await posts_collection.insert_one(post.dict(by_alias=True, exclude={"id"}))
    
    if result.inserted_id:
        return {
            "message": "Post created successfully",
            "post_id": str(result.inserted_id)
        }
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create post"
    )


@router.get("/posts", response_model=List[dict])
async def get_feed(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get feed posts"""
    posts_collection = get_posts_collection()
    
    # Get posts sorted by creation date (newest first)
    cursor = posts_collection.find().sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    
    # Format posts for response
    formatted_posts = []
    for post in posts:
        formatted_post = {
            "id": str(post["_id"]),
            "user_id": post["user_id"],
            "user_name": post["user_name"],
            "user_role": post.get("user_role", "student"),
            "content": post["content"],
            "media_urls": post.get("media_urls", []),
            "likes_count": len(post.get("likes", [])),
            "is_liked": str(current_user["_id"]) in post.get("likes", []),
            "comments": [
                {
                    "id": str(comment.get("_id", "")),
                    "user_id": comment["user_id"],
                    "user_name": comment["user_name"],
                    "user_role": comment.get("user_role", "student"),
                    "content": comment["content"],
                    "created_at": comment["created_at"].isoformat() if isinstance(comment["created_at"], datetime) else comment["created_at"]
                }
                for comment in post.get("comments", [])
            ],
            "tags": post.get("tags", []),
            "created_at": post["created_at"].isoformat() if isinstance(post["created_at"], datetime) else post["created_at"],
            "updated_at": post["updated_at"].isoformat() if isinstance(post["updated_at"], datetime) else post["updated_at"]
        }
        formatted_posts.append(formatted_post)
    
    return formatted_posts


@router.get("/posts/{post_id}", response_model=dict)
async def get_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific post"""
    posts_collection = get_posts_collection()
    
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return {
        "id": str(post["_id"]),
        "user_id": post["user_id"],
        "user_name": post["user_name"],
        "user_role": post.get("user_role", "student"),
        "content": post["content"],
        "media_urls": post.get("media_urls", []),
        "likes_count": len(post.get("likes", [])),
        "is_liked": str(current_user["_id"]) in post.get("likes", []),
        "comments": post.get("comments", []),
        "tags": post.get("tags", []),
        "created_at": post["created_at"].isoformat() if isinstance(post["created_at"], datetime) else post["created_at"],
        "updated_at": post["updated_at"].isoformat() if isinstance(post["updated_at"], datetime) else post["updated_at"]
    }


@router.post("/posts/{post_id}/like", response_model=dict)
async def toggle_like(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Toggle like on a post"""
    posts_collection = get_posts_collection()
    user_id = str(current_user["_id"])
    
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    likes = post.get("likes", [])
    
    if user_id in likes:
        # Unlike
        await posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$pull": {"likes": user_id}}
        )
        return {"message": "Post unliked", "is_liked": False, "likes_count": len(likes) - 1}
    else:
        # Like
        await posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$push": {"likes": user_id}}
        )
        return {"message": "Post liked", "is_liked": True, "likes_count": len(likes) + 1}


@router.post("/posts/{post_id}/comments", response_model=dict)
async def add_comment(
    post_id: str,
    comment_data: CreateCommentRequest,
    current_user: dict = Depends(get_current_user)
):
    """Add a comment to a post"""
    posts_collection = get_posts_collection()
    
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    comment = {
        "_id": ObjectId(),
        "user_id": str(current_user["_id"]),
        "user_name": current_user.get("full_name", current_user.get("email")),
        "user_role": current_user.get("role", "student"),
        "content": comment_data.content,
        "created_at": datetime.utcnow()
    }
    
    await posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {
            "$push": {"comments": comment},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return {
        "message": "Comment added successfully",
        "comment": {
            "id": str(comment["_id"]),
            "user_id": comment["user_id"],
            "user_name": comment["user_name"],
            "user_role": comment["user_role"],
            "content": comment["content"],
            "created_at": comment["created_at"].isoformat()
        }
    }


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a post (only by post owner)"""
    posts_collection = get_posts_collection()
    
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check if user is the post owner
    if post["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    
    await posts_collection.delete_one({"_id": ObjectId(post_id)})
    
    return {"message": "Post deleted successfully"}


@router.put("/posts/{post_id}", response_model=dict)
async def update_post(
    post_id: str,
    post_data: UpdatePostRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update a post (only by post owner)"""
    posts_collection = get_posts_collection()
    
    post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check if user is the post owner
    if post["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )
    
    update_data = {}
    if post_data.content is not None:
        update_data["content"] = post_data.content
    if post_data.media_urls is not None:
        update_data["media_urls"] = post_data.media_urls
    if post_data.tags is not None:
        update_data["tags"] = post_data.tags
    
    update_data["updated_at"] = datetime.utcnow()
    
    await posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": update_data}
    )
    
    return {"message": "Post updated successfully", "post_id": post_id}
