"""
Feedback routes for handling user feedback and learning outcomes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_active_user
from app.core.database import get_feedback_collection, get_matches_collection
from app.schemas.feedback_schema import (
    FeedbackCreate, FeedbackResponse, LearningOutcomeCreate, LearningOutcomeResponse
)
from app.models.feedback_model import FeedbackModel, LearningOutcome
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/submit", response_model=dict)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Submit feedback for a session, match, or system"""
    feedback_collection = get_feedback_collection()
    
    # Create feedback model
    new_feedback = FeedbackModel(
        feedback_type=feedback_data.feedback_type,
        reviewer_id=ObjectId(str(current_user["_id"])),
        reviewee_id=ObjectId(feedback_data.reviewee_id) if feedback_data.reviewee_id else None,
        match_id=ObjectId(feedback_data.match_id) if feedback_data.match_id else None,
        session_feedback=feedback_data.session_feedback,
        rating=feedback_data.rating,
        comment=feedback_data.comment,
        recommendation_accuracy=feedback_data.recommendation_accuracy,
        system_suggestions=feedback_data.system_suggestions,
        is_anonymous=feedback_data.is_anonymous
    )
    
    try:
        result = await feedback_collection.insert_one(
            new_feedback.dict(by_alias=True, exclude={"id"})
        )
        
        if result.inserted_id:
            # Update match status if this is session feedback
            if feedback_data.session_feedback:
                await _update_session_status(feedback_data.session_feedback.session_id)
            
            return {
                "message": "Feedback submitted successfully",
                "feedback_id": str(result.inserted_id)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to submit feedback"
            )
    
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit feedback"
        )


@router.get("/my-feedback", response_model=List[FeedbackResponse])
async def get_my_feedback(
    feedback_type: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_active_user)
):
    """Get feedback submitted by current user"""
    feedback_collection = get_feedback_collection()
    
    # Build filter
    feedback_filter = {"reviewer_id": current_user["_id"]}
    if feedback_type:
        feedback_filter["feedback_type"] = feedback_type
    
    feedbacks = []
    async for feedback in feedback_collection.find(feedback_filter):
        feedback_data = {
            "id": str(feedback["_id"]),
            "feedback_type": feedback["feedback_type"],
            "reviewer_id": str(feedback["reviewer_id"]),
            "reviewee_id": str(feedback["reviewee_id"]) if feedback.get("reviewee_id") else None,
            "match_id": str(feedback["match_id"]) if feedback.get("match_id") else None,
            "rating": feedback["rating"],
            "comment": feedback.get("comment"),
            "created_at": feedback["created_at"],
            "is_anonymous": feedback["is_anonymous"]
        }
        feedbacks.append(feedback_data)
    
    return feedbacks


@router.get("/received", response_model=List[FeedbackResponse])
async def get_received_feedback(
    current_user: dict = Depends(get_current_active_user)
):
    """Get feedback received by current user"""
    feedback_collection = get_feedback_collection()
    
    feedbacks = []
    async for feedback in feedback_collection.find({"reviewee_id": current_user["_id"]}):
        feedback_data = {
            "id": str(feedback["_id"]),
            "feedback_type": feedback["feedback_type"],
            "reviewer_id": str(feedback["reviewer_id"]) if not feedback["is_anonymous"] else "Anonymous",
            "reviewee_id": str(feedback["reviewee_id"]),
            "match_id": str(feedback["match_id"]) if feedback.get("match_id") else None,
            "rating": feedback["rating"],
            "comment": feedback.get("comment"),
            "created_at": feedback["created_at"],
            "is_anonymous": feedback["is_anonymous"]
        }
        feedbacks.append(feedback_data)
    
    return feedbacks


@router.post("/learning-outcome", response_model=dict)
async def record_learning_outcome(
    outcome_data: LearningOutcomeCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Record learning outcome for a topic"""
    feedback_collection = get_feedback_collection()
    
    # Calculate improvement score
    skill_improvement = outcome_data.skill_level_after - outcome_data.skill_level_before
    confidence_improvement = outcome_data.confidence_after - outcome_data.confidence_before
    improvement_score = (skill_improvement + confidence_improvement) / 2
    
    new_outcome = LearningOutcome(
        user_id=ObjectId(str(current_user["_id"])),
        topic=outcome_data.topic,
        skill_level_before=outcome_data.skill_level_before,
        skill_level_after=outcome_data.skill_level_after,
        confidence_before=outcome_data.confidence_before,
        confidence_after=outcome_data.confidence_after,
        session_count=outcome_data.session_count,
        total_study_time=outcome_data.total_study_time
    )
    
    try:
        result = await feedback_collection.insert_one(
            new_outcome.dict(by_alias=True)
        )
        
        if result.inserted_id:
            return {
                "message": "Learning outcome recorded successfully",
                "improvement_score": improvement_score,
                "outcome_id": str(result.inserted_id)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to record learning outcome"
            )
    
    except Exception as e:
        logger.error(f"Error recording learning outcome: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record learning outcome"
        )


@router.get("/learning-outcomes", response_model=List[LearningOutcomeResponse])
async def get_learning_outcomes(
    topic: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_active_user)
):
    """Get learning outcomes for current user"""
    feedback_collection = get_feedback_collection()
    
    # Build filter
    outcome_filter = {"user_id": current_user["_id"]}
    if topic:
        outcome_filter["topic"] = {"$regex": topic, "$options": "i"}
    
    outcomes = []
    async for outcome in feedback_collection.find(outcome_filter):
        if "skill_level_before" in outcome:  # This is a learning outcome document
            skill_improvement = outcome["skill_level_after"] - outcome["skill_level_before"]
            confidence_improvement = outcome["confidence_after"] - outcome["confidence_before"]
            improvement_score = (skill_improvement + confidence_improvement) / 2
            
            outcome_data = {
                "user_id": str(outcome["user_id"]),
                "topic": outcome["topic"],
                "skill_level_before": outcome["skill_level_before"],
                "skill_level_after": outcome["skill_level_after"],
                "confidence_before": outcome["confidence_before"],
                "confidence_after": outcome["confidence_after"],
                "improvement_score": improvement_score,
                "session_count": outcome["session_count"],
                "total_study_time": outcome["total_study_time"],
                "assessment_date": outcome["assessment_date"]
            }
            outcomes.append(outcome_data)
    
    return outcomes


@router.get("/analytics/summary")
async def get_feedback_analytics(
    current_user: dict = Depends(get_current_active_user)
):
    """Get feedback analytics summary for current user"""
    feedback_collection = get_feedback_collection()
    
    # Get feedback received by user
    received_feedback = await feedback_collection.find({
        "reviewee_id": current_user["_id"]
    }).to_list(length=1000)
    
    # Get feedback given by user
    given_feedback = await feedback_collection.find({
        "reviewer_id": current_user["_id"]
    }).to_list(length=1000)
    
    # Calculate statistics
    if received_feedback:
        avg_rating_received = sum(f["rating"] for f in received_feedback) / len(received_feedback)
        total_feedback_received = len(received_feedback)
    else:
        avg_rating_received = 0
        total_feedback_received = 0
    
    total_feedback_given = len(given_feedback)
    
    # Get learning outcomes
    learning_outcomes = await feedback_collection.find({
        "user_id": current_user["_id"],
        "skill_level_before": {"$exists": True}
    }).to_list(length=1000)
    
    total_learning_outcomes = len(learning_outcomes)
    avg_improvement = 0
    if learning_outcomes:
        improvements = [
            (outcome["skill_level_after"] - outcome["skill_level_before"] +
             outcome["confidence_after"] - outcome["confidence_before"]) / 2
            for outcome in learning_outcomes
        ]
        avg_improvement = sum(improvements) / len(improvements)
    
    return {
        "average_rating_received": round(avg_rating_received, 2),
        "total_feedback_received": total_feedback_received,
        "total_feedback_given": total_feedback_given,
        "total_learning_outcomes": total_learning_outcomes,
        "average_improvement_score": round(avg_improvement, 2),
        "feedback_response_rate": total_feedback_given / max(total_feedback_received, 1)
    }


async def _update_session_status(session_id: str):
    """Helper function to update session status after feedback"""
    matches_collection = get_matches_collection()
    
    try:
        await matches_collection.update_one(
            {"sessions.session_id": ObjectId(session_id)},
            {"$set": {"sessions.$.status": "completed"}}
        )
    except Exception as e:
        logger.error(f"Error updating session status: {e}")