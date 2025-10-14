"""
ML routes for handling machine learning model operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_active_user, get_current_superuser
from app.core.database import get_users_collection
from app.services.ml_service import ml_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/train", status_code=status.HTTP_202_ACCEPTED)
async def train_ml_models(
    current_user: dict = Depends(get_current_superuser)
):
    """Train all ML models (admin only)"""
    try:
        users_collection = get_users_collection()
        
        # Get all active users
        users = []
        async for user in users_collection.find({"is_active": True}):
            user["_id"] = str(user["_id"])  # Convert ObjectId to string
            users.append(user)
        
        # Train the recommendation model
        success = False
        if ml_service.recommendation_model:
            success = ml_service.recommendation_model.train_user_similarity_model(users)
        
        # Train the simple model as fallback
        simple_success = ml_service.train_user_recommender(users)
        
        return {
            "success": success or simple_success,
            "message": "ML models training initiated",
            "models_trained": {
                "advanced_recommendation": success,
                "simple_recommendation": simple_success
            }
        }
    except Exception as e:
        logger.error(f"Error training ML models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to train ML models"
        )


@router.get("/status")
async def get_ml_status(
    current_user: dict = Depends(get_current_active_user)
):
    """Get status of ML models"""
    try:
        status = {
            "simple_recommender": ml_service.user_recommender is not None,
            "advanced_recommender": False,
        }
        
        # Check advanced recommender if available
        if ml_service.recommendation_model:
            status["advanced_recommender"] = ml_service.recommendation_model.user_similarity_model is not None
            if hasattr(ml_service.recommendation_model, "get_model_stats"):
                status["advanced_stats"] = ml_service.recommendation_model.get_model_stats()
                
        return status
    except Exception as e:
        logger.error(f"Error getting ML status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get ML status"
        )