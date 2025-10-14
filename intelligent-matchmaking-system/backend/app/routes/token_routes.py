"""
Auth token refresh route
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from jose import jwt, JWTError
from app.core.security import create_access_token, get_current_user
from app.core.config import settings
from app.core.database import get_users_collection
from app.schemas.auth_schema import Token
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Refresh access token if the current token is still valid
    This allows extending the session without requiring re-login
    """
    try:
        # Create new access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        user_id_str = str(current_user["_id"])
        
        access_token = create_access_token(
            data={"sub": user_id_str}, expires_delta=access_token_expires
        )
        
        # Get basic user info to return with token
        user_info = {
            "id": user_id_str,
            "username": current_user.get("username"),
            "email": current_user.get("email"),
            "full_name": current_user.get("full_name"),
            "role": current_user.get("role", "student"),
            "last_login": current_user.get("last_login")
        }
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_info,
            "expires_in": settings.access_token_expire_minutes * 60
        }
    
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )