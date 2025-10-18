"""
Resource Routes - API endpoints for educational resources
Supports file uploads to MongoDB GridFS and external URLs
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import io

from app.core.database import get_database
from app.core.security import get_current_user
from app.models.resource_model import Resource, ResourceComment
from app.models.user_model import UserModel

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resource(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    resource_type: str = Form(...),
    tags: str = Form(default=""),
    difficulty_level: str = Form(default="intermediate"),
    external_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Upload a new resource (file or external URL)
    Only teachers, experts, and admins can upload
    """
    # Check permissions
    if current_user.get("role") not in ["teacher", "expert", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers, experts, and admins can upload resources"
        )
    
    # Parse tags
    tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    resource_data = {
        "title": title,
        "description": description,
        "category": category,
        "resource_type": resource_type,
        "tags": tags_list,
        "difficulty_level": difficulty_level,
        "uploaded_by": ObjectId(current_user["_id"]),
        "uploader_name": current_user.get("full_name", current_user.get("username")),
        "uploader_role": current_user["role"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "views": 0,
        "downloads": 0,
        "likes": [],
        "is_active": True,
        "is_featured": False
    }
    
    # Handle file upload to GridFS using motor async
    if file:
        import motor.motor_asyncio as motor
        
        # Get the database instance for GridFS
        mongo_db = db.client[db.name] if hasattr(db, 'client') else db.get_database()
        fs = motor.AsyncIOMotorGridFSBucket(mongo_db)
        
        file_content = await file.read()
        
        # Upload file to GridFS
        file_id = await fs.upload_from_stream(
            file.filename,
            file_content,
            metadata={
                "content_type": file.content_type,
                "uploaded_by": current_user["_id"],
                "upload_date": resource_data["created_at"]
            }
        )
        
        resource_data["file_id"] = str(file_id)
        resource_data["file_name"] = file.filename
        resource_data["file_size"] = len(file_content)
        resource_data["file_type"] = file.content_type
    
    # Handle external URL
    elif external_url:
        resource_data["external_url"] = external_url
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either file or external_url must be provided"
        )
    
    # Insert resource
    result = await db.resources.insert_one(resource_data)
    resource_data["_id"] = str(result.inserted_id)
    
    # Convert ObjectIds to strings for response
    resource_data["uploaded_by"] = str(resource_data["uploaded_by"])
    
    return {
        "message": "Resource uploaded successfully",
        "resource": resource_data
    }


@router.get("/", response_model=List[dict])
async def get_resources(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db = Depends(get_database)
):
    """Get all resources with optional filters"""
    query = {"is_active": True}
    
    if category:
        query["category"] = category
    
    if difficulty:
        query["difficulty_level"] = difficulty
    
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}}
        ]
    
    resources = await db.resources.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(None)
    
    # Convert ObjectIds to strings
    for resource in resources:
        resource["_id"] = str(resource["_id"])
        resource["uploaded_by"] = str(resource["uploaded_by"])
        resource["likes"] = [str(like) for like in resource.get("likes", [])]
    
    return resources


@router.get("/categories")
async def get_resource_categories(db = Depends(get_database)):
    """Get all resource categories with counts"""
    try:
        pipeline = [
            {"$match": {"is_active": True}},
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        categories = await db.resources.aggregate(pipeline).to_list(None)
        
        # Format response
        formatted_categories = []
        for cat in categories:
            formatted_categories.append({
                "name": cat["_id"],
                "count": cat["count"]
            })
        
        return {
            "categories": formatted_categories,
            "total_categories": len(formatted_categories)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching categories: {str(e)}"
        )


@router.get("/tags")
async def get_popular_tags(limit: int = 20, db = Depends(get_database)):
    """Get most popular resource tags"""
    try:
        pipeline = [
            {"$match": {"is_active": True}},
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        
        tags = await db.resources.aggregate(pipeline).to_list(None)
        
        return {
            "tags": [{"name": tag["_id"], "count": tag["count"]} for tag in tags]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tags: {str(e)}"
        )


@router.get("/featured")
async def get_featured_resources(
    limit: int = 10,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get featured resources"""
    try:
        query = {"is_active": True, "is_featured": True}
        
        resources = await db.resources.find(query)\
            .sort("created_at", -1)\
            .limit(limit)\
            .to_list(None)
        
        # Convert ObjectIds and add user-specific data
        for resource in resources:
            resource["_id"] = str(resource["_id"])
            resource["uploaded_by"] = str(resource["uploaded_by"])
            
            # Check if current user liked this resource
            user_id_str = str(current_user["_id"])
            resource["is_liked"] = user_id_str in [str(like) for like in resource.get("likes", [])]
            resource["like_count"] = len(resource.get("likes", []))
            
            # Convert likes to strings for response
            resource["likes"] = [str(like) for like in resource.get("likes", [])]
        
        return {
            "resources": resources,
            "total": len(resources)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching featured resources: {str(e)}"
        )


@router.post("/{resource_id}/link-to-meeting/{meeting_id}")
async def link_resource_to_meeting(
    resource_id: str,
    meeting_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Link a resource to a meeting (teacher only)"""
    try:
        # Validate ObjectIds
        try:
            resource_obj_id = ObjectId(resource_id)
            meeting_obj_id = ObjectId(meeting_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid resource or meeting ID format"
            )
        
        # Check if user is teacher
        if current_user.get("role") != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only teachers can link resources to meetings"
            )
        
        # Check if resource exists and user owns it or is admin
        resource = await db.resources.find_one({"_id": resource_obj_id})
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        user_id_str = str(current_user["_id"])
        resource_owner_str = str(resource["uploaded_by"])
        
        if user_id_str != resource_owner_str and current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only link your own resources to meetings"
            )
        
        # Check if meeting exists and user is the teacher
        meeting = await db.meetings.find_one({"_id": meeting_obj_id})
        if not meeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meeting not found"
            )
        
        meeting_teacher_str = str(meeting["teacher_id"])
        if user_id_str != meeting_teacher_str and current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only link resources to your own meetings"
            )
        
        # Add resource to meeting's resources list
        await db.meetings.update_one(
            {"_id": meeting_obj_id},
            {
                "$addToSet": {"resources": resource_obj_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Add meeting reference to resource
        await db.resources.update_one(
            {"_id": resource_obj_id},
            {
                "$addToSet": {"linked_meetings": meeting_obj_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return {
            "message": "Resource linked to meeting successfully",
            "resource_id": resource_id,
            "meeting_id": meeting_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error linking resource to meeting: {str(e)}"
        )


@router.delete("/{resource_id}/unlink-from-meeting/{meeting_id}")
async def unlink_resource_from_meeting(
    resource_id: str,
    meeting_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Unlink a resource from a meeting (teacher only)"""
    try:
        # Validate ObjectIds
        try:
            resource_obj_id = ObjectId(resource_id)
            meeting_obj_id = ObjectId(meeting_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid resource or meeting ID format"
            )
        
        # Check if user is teacher
        if current_user.get("role") != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only teachers can unlink resources from meetings"
            )
        
        # Verify ownership (same logic as linking)
        resource = await db.resources.find_one({"_id": resource_obj_id})
        meeting = await db.meetings.find_one({"_id": meeting_obj_id})
        
        if not resource or not meeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource or meeting not found"
            )
        
        user_id_str = str(current_user["_id"])
        resource_owner_str = str(resource["uploaded_by"])
        meeting_teacher_str = str(meeting["teacher_id"])
        
        if (user_id_str != resource_owner_str or user_id_str != meeting_teacher_str) and current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only unlink your own resources from your own meetings"
            )
        
        # Remove resource from meeting's resources list
        await db.meetings.update_one(
            {"_id": meeting_obj_id},
            {
                "$pull": {"resources": resource_obj_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Remove meeting reference from resource
        await db.resources.update_one(
            {"_id": resource_obj_id},
            {
                "$pull": {"linked_meetings": meeting_obj_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return {
            "message": "Resource unlinked from meeting successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error unlinking resource from meeting: {str(e)}"
        )


@router.get("/meeting/{meeting_id}")
async def get_meeting_resources(
    meeting_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get all resources linked to a specific meeting"""
    try:
        # Validate ObjectId
        try:
            meeting_obj_id = ObjectId(meeting_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid meeting ID format"
            )
        
        # Get meeting with resources
        meeting = await db.meetings.find_one({"_id": meeting_obj_id})
        if not meeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meeting not found"
            )
        
        # Check if user has access to meeting resources
        user_id_str = str(current_user["_id"])
        teacher_id_str = str(meeting["teacher_id"])
        registered_students = [str(student_id) for student_id in meeting.get("registered_students", [])]
        
        # Allow access if user is teacher, registered student, or admin
        has_access = (
            user_id_str == teacher_id_str or
            user_id_str in registered_students or
            current_user.get("role") == "admin"
        )
        
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this meeting's resources"
            )
        
        # Get linked resources
        resource_ids = meeting.get("resources", [])
        if not resource_ids:
            return {
                "meeting_id": meeting_id,
                "meeting_title": meeting.get("title", ""),
                "resources": [],
                "total": 0
            }
        
        resources = await db.resources.find({
            "_id": {"$in": resource_ids},
            "is_active": True
        }).to_list(None)
        
        # Convert ObjectIds and add user-specific data
        for resource in resources:
            resource["_id"] = str(resource["_id"])
            resource["uploaded_by"] = str(resource["uploaded_by"])
            
            # Check if current user liked this resource
            resource["is_liked"] = user_id_str in [str(like) for like in resource.get("likes", [])]
            resource["like_count"] = len(resource.get("likes", []))
            
            # Convert likes to strings for response
            resource["likes"] = [str(like) for like in resource.get("likes", [])]
        
        return {
            "meeting_id": meeting_id,
            "meeting_title": meeting.get("title", ""),
            "resources": resources,
            "total": len(resources)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching meeting resources: {str(e)}"
        )


@router.get("/my-resources")
async def get_my_resources(
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get resources uploaded by current user"""
    if current_user.get("role") not in ["teacher", "expert", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers, experts, and admins have uploaded resources"
        )
    
    resources = await db.resources.find({
        "uploaded_by": ObjectId(current_user["_id"])
    }).sort("created_at", -1).to_list(None)
    
    # Convert ObjectIds to strings
    for resource in resources:
        resource["_id"] = str(resource["_id"])
        resource["uploaded_by"] = str(resource["uploaded_by"])
        resource["likes"] = [str(like) for like in resource.get("likes", [])]
    
    return resources


@router.get("/categories")
async def get_categories(db = Depends(get_database)):
    """Get all unique categories"""
    categories = await db.resources.distinct("category", {"is_active": True})
    return {"categories": categories}


@router.get("/{resource_id}")
async def get_resource(
    resource_id: str,
    db = Depends(get_database)
):
    """Get a specific resource by ID"""
    if not ObjectId.is_valid(resource_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resource ID"
        )
    
    resource = await db.resources.find_one({"_id": ObjectId(resource_id)})
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    # Increment view count
    await db.resources.update_one(
        {"_id": ObjectId(resource_id)},
        {"$inc": {"views": 1}}
    )
    
    # Convert ObjectIds to strings
    resource["_id"] = str(resource["_id"])
    resource["uploaded_by"] = str(resource["uploaded_by"])
    resource["likes"] = [str(like) for like in resource.get("likes", [])]
    
    return resource


@router.get("/{resource_id}/download")
async def download_resource(
    resource_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Download a resource file"""
    if not ObjectId.is_valid(resource_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resource ID"
        )
    
    resource = await db.resources.find_one({"_id": ObjectId(resource_id)})
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    if not resource.get("file_id"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This resource does not have a downloadable file"
        )
    
    # Get file from GridFS using motor async
    import motor.motor_asyncio as motor
    
    try:
        # Get the database instance for GridFS
        mongo_db = db.client[db.name] if hasattr(db, 'client') else db.get_database()
        fs = motor.AsyncIOMotorGridFSBucket(mongo_db)
        
        file_id = ObjectId(resource["file_id"])
        
        # Download file from GridFS
        file_data = b""
        async for chunk in fs.open_download_stream(file_id):
            file_data += chunk
        
        # Increment download count
        await db.resources.update_one(
            {"_id": ObjectId(resource_id)},
            {"$inc": {"downloads": 1}}
        )
        
        # Return file as streaming response
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type=resource.get("file_type", "application/octet-stream"),
            headers={
                "Content-Disposition": f'attachment; filename="{resource.get("file_name", "download")}"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download file: {str(e)}"
        )


@router.post("/{resource_id}/like")
async def toggle_like(
    resource_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Toggle like on a resource"""
    if not ObjectId.is_valid(resource_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resource ID"
        )
    
    resource = await db.resources.find_one({"_id": ObjectId(resource_id)})
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    user_id = ObjectId(current_user["_id"])
    likes = resource.get("likes", [])
    
    if user_id in likes:
        # Unlike
        await db.resources.update_one(
            {"_id": ObjectId(resource_id)},
            {"$pull": {"likes": user_id}}
        )
        return {"message": "Resource unliked", "liked": False}
    else:
        # Like
        await db.resources.update_one(
            {"_id": ObjectId(resource_id)},
            {"$push": {"likes": user_id}}
        )
        return {"message": "Resource liked", "liked": True}


@router.delete("/{resource_id}")
async def delete_resource(
    resource_id: str,
    current_user: UserModel = Depends(get_current_user),
    db = Depends(get_database)
):
    """Delete a resource (soft delete)"""
    if not ObjectId.is_valid(resource_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resource ID"
        )
    
    resource = await db.resources.find_one({"_id": ObjectId(resource_id)})
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    # Check permission
    if (str(resource["uploaded_by"]) != current_user["_id"] and 
        current_user.get("role") != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own resources"
        )
    
    # Soft delete
    await db.resources.update_one(
        {"_id": ObjectId(resource_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Resource deleted successfully"}
