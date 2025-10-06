"""
Matchmaking service with intelligent algorithms
"""
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.database import get_users_collection, get_matches_collection
from app.models.match_model import MatchScore
from app.services.ml_service import ml_service
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class MatchmakingService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    
    async def find_potential_matches(self, user_id: str, match_type: str = "mentor_mentee", limit: int = 10) -> List[Dict]:
        """Find potential matches for a user"""
        users_collection = get_users_collection()
        
        # Get the requesting user
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []
        
        # Define search criteria based on match type
        if match_type == "mentor_mentee":
            return await self._find_mentors(user, limit)
        elif match_type == "peer":
            return await self._find_peers(user, limit)
        else:
            return await self._find_study_partners(user, limit)
    
    async def _find_mentors(self, user: Dict, limit: int) -> List[Dict]:
        """Find suitable mentors for a user"""
        users_collection = get_users_collection()
        
        # Get user's weak topics
        user_weaknesses = user.get("skills", {}).get("weaknesses", [])
        if not user_weaknesses:
            return []
        
        # Find users who are strong in user's weak areas
        potential_mentors = []
        async for mentor in users_collection.find({
            "_id": {"$ne": user["_id"]},
            "is_active": True,
            "$or": [
                {"role": "mentor"},
                {"role": "admin"},
                {"skills.strengths": {"$in": user_weaknesses}}
            ]
        }):
            score = await self._calculate_match_score(user, mentor, "mentor_mentee")
            if score.overall_score > 0.3:  # Minimum threshold
                mentor["match_score"] = score
                mentor["id"] = str(mentor.pop("_id"))
                potential_mentors.append(mentor)
        
        # Sort by match score and return top matches
        potential_mentors.sort(key=lambda x: x["match_score"].overall_score, reverse=True)
        return potential_mentors[:limit]
    
    async def _find_peers(self, user: Dict, limit: int) -> List[Dict]:
        """Find peer study partners"""
        users_collection = get_users_collection()
        
        user_interests = user.get("skills", {}).get("interests", [])
        user_level = user.get("profile", {}).get("academic_level", "")
        
        potential_peers = []
        async for peer in users_collection.find({
            "_id": {"$ne": user["_id"]},
            "is_active": True,
            "profile.academic_level": user_level,
            "$or": [
                {"skills.interests": {"$in": user_interests}},
                {"skills.strengths": {"$in": user.get("skills", {}).get("weaknesses", [])}},
                {"skills.weaknesses": {"$in": user.get("skills", {}).get("strengths", [])}}
            ]
        }):
            score = await self._calculate_match_score(user, peer, "peer")
            if score.overall_score > 0.4:
                peer["match_score"] = score
                peer["id"] = str(peer.pop("_id"))
                potential_peers.append(peer)
        
        potential_peers.sort(key=lambda x: x["match_score"].overall_score, reverse=True)
        return potential_peers[:limit]
    
    async def _find_study_partners(self, user: Dict, limit: int) -> List[Dict]:
        """Find general study partners"""
        users_collection = get_users_collection()
        
        user_field = user.get("profile", {}).get("field_of_study", "")
        
        potential_partners = []
        async for partner in users_collection.find({
            "_id": {"$ne": user["_id"]},
            "is_active": True,
            "profile.field_of_study": {"$regex": user_field, "$options": "i"}
        }):
            score = await self._calculate_match_score(user, partner, "study_partner")
            if score.overall_score > 0.3:
                partner["match_score"] = score
                partner["id"] = str(partner.pop("_id"))
                potential_partners.append(partner)
        
        potential_partners.sort(key=lambda x: x["match_score"].overall_score, reverse=True)
        return potential_partners[:limit]
    
    async def _calculate_match_score(self, user1: Dict, user2: Dict, match_type: str) -> MatchScore:
        """Calculate compatibility score between two users"""
        
        # Skill compatibility
        skill_score = self._calculate_skill_compatibility(user1, user2, match_type)
        
        # Schedule compatibility
        schedule_score = self._calculate_schedule_compatibility(user1, user2)
        
        # Learning style compatibility
        learning_style_score = self._calculate_learning_style_compatibility(user1, user2)
        
        # Topic relevance
        topic_score = self._calculate_topic_relevance(user1, user2)
        
        # Overall score (weighted average)
        weights = {
            "mentor_mentee": [0.4, 0.2, 0.2, 0.2],  # Skill > others
            "peer": [0.3, 0.25, 0.25, 0.2],        # More balanced
            "study_partner": [0.25, 0.3, 0.25, 0.2] # Schedule important
        }
        
        weight_set = weights.get(match_type, weights["peer"])
        overall_score = (
            skill_score * weight_set[0] +
            schedule_score * weight_set[1] +
            learning_style_score * weight_set[2] +
            topic_score * weight_set[3]
        )
        
        return MatchScore(
            overall_score=overall_score,
            skill_compatibility=skill_score,
            schedule_compatibility=schedule_score,
            learning_style_compatibility=learning_style_score,
            topic_relevance=topic_score
        )
    
    def _calculate_skill_compatibility(self, user1: Dict, user2: Dict, match_type: str) -> float:
        """Calculate skill compatibility between users"""
        user1_skills = user1.get("skills", {})
        user2_skills = user2.get("skills", {})
        
        if match_type == "mentor_mentee":
            # Check if mentor's strengths cover mentee's weaknesses
            mentor_strengths = set(user2_skills.get("strengths", []))
            mentee_weaknesses = set(user1_skills.get("weaknesses", []))
            
            if not mentee_weaknesses:
                return 0.0
            
            overlap = mentor_strengths.intersection(mentee_weaknesses)
            return len(overlap) / len(mentee_weaknesses)
        
        elif match_type == "peer":
            # Check mutual benefit potential
            user1_strengths = set(user1_skills.get("strengths", []))
            user1_weaknesses = set(user1_skills.get("weaknesses", []))
            user2_strengths = set(user2_skills.get("strengths", []))
            user2_weaknesses = set(user2_skills.get("weaknesses", []))
            
            # How much can user1 help user2
            help_score_1to2 = len(user1_strengths.intersection(user2_weaknesses))
            # How much can user2 help user1
            help_score_2to1 = len(user2_strengths.intersection(user1_weaknesses))
            
            total_needs = len(user1_weaknesses) + len(user2_weaknesses)
            if total_needs == 0:
                return 0.5
            
            return (help_score_1to2 + help_score_2to1) / total_needs
        
        else:  # study_partner
            # Check common interests
            user1_interests = set(user1_skills.get("interests", []))
            user2_interests = set(user2_skills.get("interests", []))
            
            common_interests = user1_interests.intersection(user2_interests)
            total_interests = user1_interests.union(user2_interests)
            
            if not total_interests:
                return 0.0
            
            return len(common_interests) / len(total_interests)
    
    def _calculate_schedule_compatibility(self, user1: Dict, user2: Dict) -> float:
        """Calculate schedule compatibility"""
        user1_availability = user1.get("profile", {}).get("availability", {})
        user2_availability = user2.get("profile", {}).get("availability", {})
        
        if not user1_availability or not user2_availability:
            return 0.5  # Neutral score if no schedule info
        
        overlap_score = 0
        total_days = 0
        
        for day in user1_availability:
            if day in user2_availability:
                total_days += 1
                user1_slots = set(user1_availability[day])
                user2_slots = set(user2_availability[day])
                common_slots = user1_slots.intersection(user2_slots)
                
                if common_slots:
                    overlap_score += len(common_slots) / max(len(user1_slots), len(user2_slots))
        
        return overlap_score / max(total_days, 1)
    
    def _calculate_learning_style_compatibility(self, user1: Dict, user2: Dict) -> float:
        """Calculate learning style compatibility"""
        user1_preferences = set(user1.get("profile", {}).get("learning_preferences", []))
        user2_preferences = set(user2.get("profile", {}).get("learning_preferences", []))
        
        if not user1_preferences or not user2_preferences:
            return 0.5
        
        common_preferences = user1_preferences.intersection(user2_preferences)
        total_preferences = user1_preferences.union(user2_preferences)
        
        return len(common_preferences) / len(total_preferences) if total_preferences else 0.0
    
    def _calculate_topic_relevance(self, user1: Dict, user2: Dict) -> float:
        """Calculate topic relevance using text similarity"""
        user1_field = user1.get("profile", {}).get("field_of_study", "")
        user2_field = user2.get("profile", {}).get("field_of_study", "")
        
        user1_interests = " ".join(user1.get("skills", {}).get("interests", []))
        user2_interests = " ".join(user2.get("skills", {}).get("interests", []))
        
        user1_text = f"{user1_field} {user1_interests}".strip()
        user2_text = f"{user2_field} {user2_interests}".strip()
        
        if not user1_text or not user2_text:
            return 0.5
        
        try:
            # Use TF-IDF vectorization and cosine similarity
            vectors = self.vectorizer.fit_transform([user1_text, user2_text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return float(similarity)
        except:
            return 0.5

    async def find_ml_recommendations(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Find matches using ML recommendations"""
        users_collection = get_users_collection()
        
        # Get the requesting user
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []
        
        # Get all users for training data
        all_users = []
        async for u in users_collection.find({"is_active": True}):
            all_users.append(u)
        
        # Train the ML model if not already trained
        if not ml_service.user_recommender:
            success = ml_service.train_user_recommender(all_users)
            if not success:
                return []
        
        # Get ML recommendations
        recommendations = ml_service.recommend_users(user, limit)
        
        # Convert recommendations to user data
        results = []
        for rec in recommendations:
            if rec["user_index"] < len(all_users):
                recommended_user = all_users[rec["user_index"]]
                recommended_user["id"] = str(recommended_user.pop("_id"))
                recommended_user["ml_score"] = rec["similarity_score"]
                recommended_user["rank"] = rec["rank"]
                results.append(recommended_user)
        
        return results

    async def get_topic_recommendations(self, user_id: str, limit: int = 5) -> List[str]:
        """Get topic recommendations for a user"""
        users_collection = get_users_collection()
        
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []
        
        user_preferences = user.get("skills", {}).get("interests", [])
        
        # Get topic recommendations from ML service
        recommendations = ml_service.recommend_topics(
            {"interests": user_preferences}, 
            limit
        )
        
        return recommendations


# Global instance
matchmaking_service = MatchmakingService()