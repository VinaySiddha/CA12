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
    
    # Handle file upload to GridFS
    if file:
        import gridfs
        fs = gridfs.GridFS(db.client[db.name])
        
        file_content = await file.read()
        file_id = fs.put(
            file_content,
            filename=file.filename,
            content_type=file.content_type
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
    
    # Get file from GridFS
    import gridfs
    fs = gridfs.GridFS(db.client[db.name])
    
    try:
        file_id = ObjectId(resource["file_id"])
        grid_out = fs.get(file_id)
        
        # Increment download count
        await db.resources.update_one(
            {"_id": ObjectId(resource_id)},
            {"$inc": {"downloads": 1}}
        )
        
        # Return file as streaming response
        return StreamingResponse(
            io.BytesIO(grid_out.read()),
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
