"""
Feedback service for processing and analyzing feedback data
"""
from typing import List, Dict, Any, Optional
from app.core.database import get_feedback_collection, get_users_collection, get_matches_collection
from app.models.feedback_model import FeedbackModel, LearningOutcome
from bson import ObjectId
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FeedbackService:
    def __init__(self):
        pass
    
    async def process_session_feedback(self, feedback_data: Dict) -> Dict[str, Any]:
        """Process and analyze session feedback"""
        try:
            feedback_collection = get_feedback_collection()
            
            # Store the feedback
            result = await feedback_collection.insert_one(feedback_data)
            
            if not result.inserted_id:
                return {"success": False, "message": "Failed to store feedback"}
            
            # Analyze feedback
            analysis = await self._analyze_feedback(feedback_data)
            
            # Update user statistics
            await self._update_user_stats_from_feedback(feedback_data)
            
            # Check for improvement opportunities
            recommendations = await self._generate_recommendations(feedback_data)
            
            return {
                "success": True,
                "feedback_id": str(result.inserted_id),
                "analysis": analysis,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Error processing session feedback: {e}")
            return {"success": False, "message": "Failed to process feedback"}
    
    async def analyze_user_progress(self, user_id: str, time_period: int = 30) -> Dict[str, Any]:
        """Analyze user's learning progress over time"""
        try:
            feedback_collection = get_feedback_collection()
            
            # Get user's feedback in the specified period
            start_date = datetime.utcnow() - timedelta(days=time_period)
            
            user_feedback = await feedback_collection.find({
                "$or": [
                    {"reviewer_id": ObjectId(user_id)},
                    {"reviewee_id": ObjectId(user_id)}
                ],
                "created_at": {"$gte": start_date}
            }).to_list(length=1000)
            
            if not user_feedback:
                return {"message": "No feedback data available for analysis"}
            
            # Analyze progress
            progress_analysis = {
                "total_sessions": len([f for f in user_feedback if f.get("session_feedback")]),
                "average_rating_received": await self._calculate_average_rating_received(user_id, user_feedback),
                "average_rating_given": await self._calculate_average_rating_given(user_id, user_feedback),
                "improvement_trends": await self._analyze_improvement_trends(user_id, user_feedback),
                "topic_performance": await self._analyze_topic_performance(user_id, user_feedback),
                "learning_outcomes": await self._get_learning_outcomes(user_id, start_date)
            }
            
            return progress_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing user progress: {e}")
            return {"error": "Failed to analyze progress"}
    
    async def generate_feedback_insights(self, match_id: str) -> Dict[str, Any]:
        """Generate insights from feedback for a specific match"""
        try:
            feedback_collection = get_feedback_collection()
            
            # Get all feedback for this match
            match_feedback = await feedback_collection.find({
                "match_id": ObjectId(match_id)
            }).to_list(length=100)
            
            if not match_feedback:
                return {"message": "No feedback available for this match"}
            
            insights = {
                "total_feedback_count": len(match_feedback),
                "average_overall_rating": self._calculate_average_rating(match_feedback),
                "session_analysis": await self._analyze_session_feedback(match_feedback),
                "improvement_areas": await self._identify_improvement_areas(match_feedback),
                "success_indicators": await self._identify_success_indicators(match_feedback),
                "recommendations": await self._generate_match_recommendations(match_feedback)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating feedback insights: {e}")
            return {"error": "Failed to generate insights"}
    
    async def get_system_feedback_analytics(self) -> Dict[str, Any]:
        """Get system-wide feedback analytics"""
        try:
            feedback_collection = get_feedback_collection()
            
            # Get recent feedback (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            recent_feedback = await feedback_collection.find({
                "created_at": {"$gte": thirty_days_ago}
            }).to_list(length=10000)
            
            analytics = {
                "total_feedback": len(recent_feedback),
                "average_system_rating": self._calculate_average_rating(recent_feedback),
                "feedback_by_type": self._categorize_feedback_by_type(recent_feedback),
                "rating_distribution": self._get_rating_distribution(recent_feedback),
                "common_improvement_areas": await self._identify_common_issues(recent_feedback),
                "system_satisfaction_trend": await self._calculate_satisfaction_trend(recent_feedback)
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting system feedback analytics: {e}")
            return {"error": "Failed to get analytics"}
    
    async def _analyze_feedback(self, feedback_data: Dict) -> Dict[str, Any]:
        """Analyze individual feedback for insights"""
        analysis = {}
        
        # Session feedback analysis
        if "session_feedback" in feedback_data and feedback_data["session_feedback"]:
            session_fb = feedback_data["session_feedback"]
            
            analysis["session_quality"] = {
                "overall_rating": session_fb.get("overall_rating", 0),
                "helpfulness": session_fb.get("helpfulness_rating", 0),
                "engagement": session_fb.get("engagement_rating", 0),
                "clarity": session_fb.get("clarity_rating", 0),
                "objectives_met": session_fb.get("learning_objectives_met", False)
            }
            
            # Identify areas for improvement
            low_scoring_areas = []
            for area, rating in analysis["session_quality"].items():
                if isinstance(rating, int) and rating < 3:
                    low_scoring_areas.append(area)
            
            analysis["improvement_areas"] = low_scoring_areas
        
        # Overall satisfaction
        overall_rating = feedback_data.get("rating", 0)
        analysis["satisfaction_level"] = self._categorize_satisfaction(overall_rating)
        
        return analysis
    
    async def _update_user_stats_from_feedback(self, feedback_data: Dict):
        """Update user statistics based on feedback"""
        # This would update gamification stats
        # Implementation would depend on the specific feedback type
        pass
    
    async def _generate_recommendations(self, feedback_data: Dict) -> List[str]:
        """Generate recommendations based on feedback"""
        recommendations = []
        
        if "session_feedback" in feedback_data:
            session_fb = feedback_data["session_feedback"]
            
            # Check for low ratings and suggest improvements
            if session_fb.get("clarity_rating", 5) < 3:
                recommendations.append("Focus on explaining concepts more clearly")
            
            if session_fb.get("engagement_rating", 5) < 3:
                recommendations.append("Try more interactive learning activities")
            
            if session_fb.get("helpfulness_rating", 5) < 3:
                recommendations.append("Align teaching methods with student's learning style")
            
            if not session_fb.get("learning_objectives_met", True):
                recommendations.append("Set clearer learning objectives before sessions")
        
        return recommendations
    
    async def _calculate_average_rating_received(self, user_id: str, feedback_data: List[Dict]) -> float:
        """Calculate average rating received by user"""
        received_ratings = [
            f["rating"] for f in feedback_data 
            if f.get("reviewee_id") == ObjectId(user_id) and "rating" in f
        ]
        
        return sum(received_ratings) / len(received_ratings) if received_ratings else 0.0
    
    async def _calculate_average_rating_given(self, user_id: str, feedback_data: List[Dict]) -> float:
        """Calculate average rating given by user"""
        given_ratings = [
            f["rating"] for f in feedback_data 
            if f.get("reviewer_id") == ObjectId(user_id) and "rating" in f
        ]
        
        return sum(given_ratings) / len(given_ratings) if given_ratings else 0.0
    
    async def _analyze_improvement_trends(self, user_id: str, feedback_data: List[Dict]) -> Dict[str, Any]:
        """Analyze improvement trends over time"""
        # Sort feedback by date
        sorted_feedback = sorted(feedback_data, key=lambda x: x.get("created_at", datetime.min))
        
        # Calculate trend (simplified)
        received_ratings = [
            f["rating"] for f in sorted_feedback 
            if f.get("reviewee_id") == ObjectId(user_id)
        ]
        
        if len(received_ratings) < 2:
            return {"trend": "insufficient_data"}
        
        # Simple trend calculation
        first_half_avg = sum(received_ratings[:len(received_ratings)//2]) / (len(received_ratings)//2)
        second_half_avg = sum(received_ratings[len(received_ratings)//2:]) / (len(received_ratings) - len(received_ratings)//2)
        
        trend_direction = "improving" if second_half_avg > first_half_avg else "declining"
        trend_magnitude = abs(second_half_avg - first_half_avg)
        
        return {
            "trend": trend_direction,
            "magnitude": round(trend_magnitude, 2),
            "first_period_avg": round(first_half_avg, 2),
            "recent_period_avg": round(second_half_avg, 2)
        }
    
    async def _analyze_topic_performance(self, user_id: str, feedback_data: List[Dict]) -> Dict[str, float]:
        """Analyze performance by topic"""
        topic_ratings = {}
        
        for feedback in feedback_data:
            if feedback.get("reviewee_id") == ObjectId(user_id) and "session_feedback" in feedback:
                session_fb = feedback["session_feedback"]
                topics_mastered = session_fb.get("topics_mastered", [])
                overall_rating = session_fb.get("overall_rating", 0)
                
                for topic in topics_mastered:
                    if topic not in topic_ratings:
                        topic_ratings[topic] = []
                    topic_ratings[topic].append(overall_rating)
        
        # Calculate average rating per topic
        topic_averages = {
            topic: sum(ratings) / len(ratings)
            for topic, ratings in topic_ratings.items()
        }
        
        return topic_averages
    
    async def _get_learning_outcomes(self, user_id: str, start_date: datetime) -> List[Dict]:
        """Get learning outcomes for user"""
        feedback_collection = get_feedback_collection()
        
        outcomes = await feedback_collection.find({
            "user_id": ObjectId(user_id),
            "assessment_date": {"$gte": start_date},
            "skill_level_before": {"$exists": True}  # Learning outcome documents
        }).to_list(length=100)
        
        processed_outcomes = []
        for outcome in outcomes:
            improvement = outcome["skill_level_after"] - outcome["skill_level_before"]
            processed_outcomes.append({
                "topic": outcome["topic"],
                "skill_improvement": improvement,
                "confidence_improvement": outcome["confidence_after"] - outcome["confidence_before"],
                "session_count": outcome["session_count"],
                "study_time": outcome["total_study_time"]
            })
        
        return processed_outcomes
    
    def _calculate_average_rating(self, feedback_data: List[Dict]) -> float:
        """Calculate average rating from feedback data"""
        ratings = [f["rating"] for f in feedback_data if "rating" in f]
        return sum(ratings) / len(ratings) if ratings else 0.0
    
    async def _analyze_session_feedback(self, feedback_data: List[Dict]) -> Dict[str, Any]:
        """Analyze session-specific feedback"""
        session_feedbacks = [
            f["session_feedback"] for f in feedback_data 
            if "session_feedback" in f and f["session_feedback"]
        ]
        
        if not session_feedbacks:
            return {"message": "No session feedback available"}
        
        return {
            "total_sessions": len(session_feedbacks),
            "avg_helpfulness": sum(sf.get("helpfulness_rating", 0) for sf in session_feedbacks) / len(session_feedbacks),
            "avg_engagement": sum(sf.get("engagement_rating", 0) for sf in session_feedbacks) / len(session_feedbacks),
            "avg_clarity": sum(sf.get("clarity_rating", 0) for sf in session_feedbacks) / len(session_feedbacks),
            "objectives_met_rate": sum(1 for sf in session_feedbacks if sf.get("learning_objectives_met", False)) / len(session_feedbacks)
        }
    
    async def _identify_improvement_areas(self, feedback_data: List[Dict]) -> List[str]:
        """Identify areas needing improvement from feedback"""
        improvement_areas = []
        
        session_feedbacks = [
            f["session_feedback"] for f in feedback_data 
            if "session_feedback" in f and f["session_feedback"]
        ]
        
        if session_feedbacks:
            avg_helpfulness = sum(sf.get("helpfulness_rating", 0) for sf in session_feedbacks) / len(session_feedbacks)
            avg_engagement = sum(sf.get("engagement_rating", 0) for sf in session_feedbacks) / len(session_feedbacks)
            avg_clarity = sum(sf.get("clarity_rating", 0) for sf in session_feedbacks) / len(session_feedbacks)
            
            if avg_helpfulness < 3.5:
                improvement_areas.append("Session helpfulness")
            if avg_engagement < 3.5:
                improvement_areas.append("Student engagement")
            if avg_clarity < 3.5:
                improvement_areas.append("Explanation clarity")
        
        return improvement_areas
    
    async def _identify_success_indicators(self, feedback_data: List[Dict]) -> List[str]:
        """Identify success indicators from feedback"""
        success_indicators = []
        
        avg_rating = self._calculate_average_rating(feedback_data)
        
        if avg_rating >= 4.0:
            success_indicators.append("High overall satisfaction")
        
        session_feedbacks = [
            f["session_feedback"] for f in feedback_data 
            if "session_feedback" in f and f["session_feedback"]
        ]
        
        if session_feedbacks:
            objectives_met_rate = sum(1 for sf in session_feedbacks if sf.get("learning_objectives_met", False)) / len(session_feedbacks)
            
            if objectives_met_rate >= 0.8:
                success_indicators.append("High learning objective achievement")
        
        return success_indicators
    
    async def _generate_match_recommendations(self, feedback_data: List[Dict]) -> List[str]:
        """Generate recommendations for the match based on feedback"""
        recommendations = []
        
        avg_rating = self._calculate_average_rating(feedback_data)
        
        if avg_rating < 3.0:
            recommendations.append("Consider reassessing match compatibility")
        elif avg_rating >= 4.5:
            recommendations.append("Excellent match - consider extending partnership")
        
        return recommendations
    
    def _categorize_feedback_by_type(self, feedback_data: List[Dict]) -> Dict[str, int]:
        """Categorize feedback by type"""
        type_counts = {}
        
        for feedback in feedback_data:
            feedback_type = feedback.get("feedback_type", "unknown")
            type_counts[feedback_type] = type_counts.get(feedback_type, 0) + 1
        
        return type_counts
    
    def _get_rating_distribution(self, feedback_data: List[Dict]) -> Dict[str, int]:
        """Get distribution of ratings"""
        distribution = {str(i): 0 for i in range(1, 6)}
        
        for feedback in feedback_data:
            rating = str(feedback.get("rating", 0))
            if rating in distribution:
                distribution[rating] += 1
        
        return distribution
    
    async def _identify_common_issues(self, feedback_data: List[Dict]) -> List[str]:
        """Identify common issues from feedback comments"""
        # This would use NLP to analyze comments
        # For now, return placeholder
        return [
            "Session scheduling conflicts",
            "Communication clarity",
            "Preparation time"
        ]
    
    async def _calculate_satisfaction_trend(self, feedback_data: List[Dict]) -> Dict[str, Any]:
        """Calculate satisfaction trend over time"""
        # Sort by date and calculate trend
        sorted_feedback = sorted(feedback_data, key=lambda x: x.get("created_at", datetime.min))
        
        if len(sorted_feedback) < 2:
            return {"trend": "insufficient_data"}
        
        # Calculate weekly averages
        weekly_averages = []
        # Implementation would group by week and calculate averages
        
        return {
            "trend": "stable",  # Placeholder
            "weekly_averages": weekly_averages
        }
    
    def _categorize_satisfaction(self, rating: int) -> str:
        """Categorize satisfaction level based on rating"""
        if rating >= 4:
            return "high"
        elif rating >= 3:
            return "medium"
        else:
            return "low"


# Global instance
feedback_service = FeedbackService()