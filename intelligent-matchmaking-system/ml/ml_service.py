"""
Machine Learning service integrating all ML models for the intelligent matchmaking system
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

from .topic_nlp_model import topic_classifier
from .recommendation_model import recommendation_model
from .feedback_predictor import feedback_predictor

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self):
        self.topic_classifier = topic_classifier
        self.recommendation_model = recommendation_model
        self.feedback_predictor = feedback_predictor
        
        self.model_status = {
            "topic_classifier": False,
            "recommendation_model": False,
            "feedback_predictor": False,
            "last_training_update": None
        }
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all ML models"""
        
        try:
            # Topic classifier should already be trained on import
            self.model_status["topic_classifier"] = True
            
            # Feedback predictor should already be trained on import
            self.model_status["feedback_predictor"] = self.feedback_predictor.is_trained
            
            # Recommendation model needs data to be trained
            self.model_status["recommendation_model"] = False
            
            logger.info("ML Service initialized")
            
        except Exception as e:
            logger.error(f"Error initializing ML models: {e}")
    
    async def analyze_user_topics(self, user_text: str) -> Dict[str, Any]:
        """Analyze user interests and topics from text"""
        
        try:
            if not user_text or not user_text.strip():
                return {"topics": [], "keywords": [], "confidence": 0.0}
            
            # Get topic predictions
            prediction_result = self.topic_classifier.predict_topic(user_text)
            
            # Get keywords
            keywords = self.topic_classifier.extract_keywords(user_text)
            
            return {
                "topics": prediction_result.get("predicted_topics", []),
                "keywords": keywords,
                "confidence": prediction_result.get("confidence", 0.0),
                "topic_distribution": prediction_result.get("probabilities", {}),
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing user topics: {e}")
            return {"topics": [], "keywords": [], "confidence": 0.0, "error": str(e)}
    
    async def train_recommendation_model(self, users_data: List[Dict], 
                                       interaction_data: List[Dict] = None) -> bool:
        """Train recommendation model with current user data"""
        
        try:
            # Train user similarity model
            user_success = self.recommendation_model.train_user_similarity_model(users_data)
            
            # Train collaborative filtering if interaction data available
            collab_success = True
            if interaction_data and len(interaction_data) > 10:
                collab_success = self.recommendation_model.train_collaborative_filtering(interaction_data)
            
            # Update model status
            self.model_status["recommendation_model"] = user_success
            self.model_status["last_training_update"] = datetime.utcnow().isoformat()
            
            if user_success:
                logger.info(f"Recommendation model trained successfully with {len(users_data)} users")
            
            return user_success and collab_success
            
        except Exception as e:
            logger.error(f"Error training recommendation model: {e}")
            return False
    
    async def get_user_recommendations(self, user_profile: Dict, 
                                     available_users: List[Dict],
                                     n_recommendations: int = 5) -> List[Dict]:
        """Get personalized user recommendations"""
        
        try:
            if not self.model_status["recommendation_model"]:
                # Try to train model with available data
                if len(available_users) >= 3:
                    await self.train_recommendation_model(available_users + [user_profile])
                else:
                    # Fallback to rule-based matching
                    return await self._rule_based_user_matching(user_profile, available_users, n_recommendations)
            
            # Get ML-based recommendations
            recommendations = self.recommendation_model.recommend_users(
                user_profile, n_recommendations
            )
            
            # Enrich recommendations with additional data
            enriched_recommendations = []
            for rec in recommendations:
                # Find user data
                user_data = next(
                    (u for u in available_users if str(u.get('_id', u.get('id'))) == rec['user_id']), 
                    None
                )
                
                if user_data:
                    enriched_rec = {
                        **rec,
                        "user_data": {
                            "name": user_data.get("profile", {}).get("full_name", "Unknown"),
                            "field_of_study": user_data.get("profile", {}).get("field_of_study", ""),
                            "academic_level": user_data.get("profile", {}).get("academic_level", ""),
                            "interests": user_data.get("skills", {}).get("interests", []),
                            "points": user_data.get("points", 0),
                            "level": user_data.get("level", 1)
                        },
                        "match_reasons": await self._generate_match_reasons(user_profile, user_data)
                    }
                    enriched_recommendations.append(enriched_rec)
            
            return enriched_recommendations
            
        except Exception as e:
            logger.error(f"Error getting user recommendations: {e}")
            return []
    
    async def _rule_based_user_matching(self, user_profile: Dict, 
                                      available_users: List[Dict],
                                      n_recommendations: int) -> List[Dict]:
        """Fallback rule-based matching when ML model isn't available"""
        
        try:
            user_interests = set(user_profile.get('skills', {}).get('interests', []))
            user_field = user_profile.get('profile', {}).get('field_of_study', '').lower()
            user_level = user_profile.get('profile', {}).get('academic_level', '')
            user_id = str(user_profile.get('_id', user_profile.get('id', '')))
            
            matches = []
            
            for other_user in available_users:
                other_id = str(other_user.get('_id', other_user.get('id', '')))
                if other_id == user_id:
                    continue
                
                score = 0
                
                # Interest overlap
                other_interests = set(other_user.get('skills', {}).get('interests', []))
                interest_overlap = len(user_interests & other_interests)
                score += interest_overlap * 0.4
                
                # Field similarity
                other_field = other_user.get('profile', {}).get('field_of_study', '').lower()
                if user_field and other_field and user_field in other_field:
                    score += 0.3
                
                # Level compatibility
                other_level = other_user.get('profile', {}).get('academic_level', '')
                if user_level == other_level:
                    score += 0.2
                elif abs(self._level_to_number(user_level) - self._level_to_number(other_level)) == 1:
                    score += 0.1
                
                # Activity level
                other_points = other_user.get('points', 0)
                if other_points > 100:  # Active user
                    score += 0.1
                
                if score > 0:
                    matches.append({
                        'user_id': other_id,
                        'similarity_score': score,
                        'recommendation_type': 'rule_based',
                        'user_data': {
                            "name": other_user.get("profile", {}).get("full_name", "Unknown"),
                            "field_of_study": other_user.get("profile", {}).get("field_of_study", ""),
                            "academic_level": other_user.get("profile", {}).get("academic_level", ""),
                            "interests": other_user.get("skills", {}).get("interests", []),
                            "points": other_user.get("points", 0),
                            "level": other_user.get("level", 1)
                        },
                        "match_reasons": await self._generate_match_reasons(user_profile, other_user)
                    })
            
            # Sort by score and return top matches
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            return matches[:n_recommendations]
            
        except Exception as e:
            logger.error(f"Error in rule-based matching: {e}")
            return []
    
    async def _generate_match_reasons(self, user1: Dict, user2: Dict) -> List[str]:
        """Generate human-readable reasons for the match"""
        
        reasons = []
        
        try:
            # Interest overlap
            interests1 = set(user1.get('skills', {}).get('interests', []))
            interests2 = set(user2.get('skills', {}).get('interests', []))
            common_interests = interests1 & interests2
            
            if common_interests:
                if len(common_interests) == 1:
                    reasons.append(f"Shared interest in {list(common_interests)[0]}")
                else:
                    reasons.append(f"Multiple shared interests: {', '.join(list(common_interests)[:3])}")
            
            # Field similarity
            field1 = user1.get('profile', {}).get('field_of_study', '')
            field2 = user2.get('profile', {}).get('field_of_study', '')
            if field1 and field2 and field1.lower() == field2.lower():
                reasons.append(f"Same field of study: {field1}")
            
            # Level compatibility
            level1 = user1.get('profile', {}).get('academic_level', '')
            level2 = user2.get('profile', {}).get('academic_level', '')
            if level1 == level2:
                reasons.append(f"Same academic level: {level1}")
            
            # Complementary strengths/weaknesses
            strengths1 = set(user1.get('skills', {}).get('strengths', []))
            weaknesses2 = set(user2.get('skills', {}).get('weaknesses', []))
            can_help = strengths1 & weaknesses2
            
            if can_help:
                reasons.append(f"Can help with: {', '.join(list(can_help)[:2])}")
            
            # Experience level
            points1 = user1.get('points', 0)
            points2 = user2.get('points', 0)
            if abs(points1 - points2) < 200:  # Similar experience
                reasons.append("Similar experience level")
            
            if not reasons:
                reasons.append("Good potential for collaboration")
            
            return reasons
            
        except Exception as e:
            logger.error(f"Error generating match reasons: {e}")
            return ["Potential for good collaboration"]
    
    def _level_to_number(self, level: str) -> int:
        """Convert academic level to number"""
        mapping = {"undergraduate": 1, "graduate": 2, "phd": 3, "postdoc": 4}
        return mapping.get(level.lower(), 1)
    
    async def analyze_feedback_batch(self, feedback_list: List[Dict]) -> Dict[str, Any]:
        """Analyze feedback in batch and provide insights"""
        
        try:
            # Individual feedback analysis
            analyses = self.feedback_predictor.batch_analyze_feedback(feedback_list)
            
            # Trend analysis
            trends = self.feedback_predictor.get_feedback_trends(analyses)
            
            # Generate recommendations based on feedback
            recommendations = await self._generate_feedback_recommendations(trends, analyses)
            
            return {
                "individual_analyses": analyses,
                "trends": trends,
                "recommendations": recommendations,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "feedback_count": len(feedback_list)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing feedback batch: {e}")
            return {"error": str(e)}
    
    async def _generate_feedback_recommendations(self, trends: Dict, 
                                               analyses: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on feedback analysis"""
        
        recommendations = []
        
        try:
            avg_score = trends.get("average_score", 3.0)
            positive_ratio = trends.get("positive_feedback_ratio", 0.5)
            high_quality_ratio = trends.get("high_quality_ratio", 0.5)
            
            # Score-based recommendations
            if avg_score < 2.5:
                recommendations.append("Overall satisfaction is low - consider reviewing session quality and teaching methods")
            elif avg_score > 4.0:
                recommendations.append("Excellent performance - continue current practices and share successful strategies")
            
            # Sentiment-based recommendations
            if positive_ratio < 0.4:
                recommendations.append("High negative sentiment detected - focus on improving user experience and engagement")
            elif positive_ratio > 0.7:
                recommendations.append("Strong positive sentiment - consider expanding successful approaches")
            
            # Quality-based recommendations
            if high_quality_ratio < 0.5:
                recommendations.append("Session quality needs improvement - provide additional training and resources")
            
            # Trend-based recommendations
            improvement_areas = trends.get("improvement_areas", [])
            for area in improvement_areas:
                recommendations.append(f"Action needed: {area}")
            
            # Specific feedback analysis
            negative_feedback = [
                a for a in analyses 
                if a.get("sentiment_analysis", {}).get("sentiment") == "negative"
            ]
            
            if len(negative_feedback) > 2:
                common_issues = self._identify_common_issues(negative_feedback)
                for issue in common_issues:
                    recommendations.append(f"Address recurring issue: {issue}")
            
            if not recommendations:
                recommendations.append("Overall feedback is positive - maintain current quality standards")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating feedback recommendations: {e}")
            return ["Review feedback trends and address any concerning patterns"]
    
    def _identify_common_issues(self, negative_feedback: List[Dict]) -> List[str]:
        """Identify common issues from negative feedback"""
        
        issues = []
        
        try:
            # Analyze key phrases from negative feedback
            all_phrases = []
            for feedback in negative_feedback:
                phrases = feedback.get("key_phrases", [])
                all_phrases.extend(phrases)
            
            # Count phrase frequency
            phrase_count = {}
            for phrase in all_phrases:
                phrase_count[phrase] = phrase_count.get(phrase, 0) + 1
            
            # Find common issues (phrases mentioned in multiple feedback items)
            common_phrases = [
                phrase for phrase, count in phrase_count.items() 
                if count >= 2 and len(phrase) > 3
            ]
            
            # Map phrases to issue categories
            for phrase in common_phrases[:3]:  # Top 3 issues
                if phrase in ['unprepared', 'preparation', 'organized']:
                    issues.append("Poor session preparation")
                elif phrase in ['explanation', 'unclear', 'confusing']:
                    issues.append("Unclear explanations and communication")
                elif phrase in ['time', 'management', 'wasted']:
                    issues.append("Poor time management")
                elif phrase in ['knowledge', 'understanding', 'lacks']:
                    issues.append("Insufficient subject knowledge")
                else:
                    issues.append(f"Recurring concern: {phrase}")
            
            return list(set(issues))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error identifying common issues: {e}")
            return []
    
    async def get_learning_resource_recommendations(self, user_profile: Dict,
                                                  available_resources: List[Dict],
                                                  n_recommendations: int = 5) -> List[Dict]:
        """Get personalized learning resource recommendations"""
        
        try:
            # Analyze user topics and interests
            user_text = " ".join(user_profile.get('skills', {}).get('interests', []))
            topic_analysis = await self.analyze_user_topics(user_text)
            
            # Get recommendations from model
            recommendations = self.recommendation_model.recommend_learning_resources(
                user_profile, available_resources, n_recommendations
            )
            
            # Enhance with topic analysis
            for rec in recommendations:
                rec["topic_match"] = topic_analysis
                rec["explanation"] = self._generate_resource_explanation(
                    user_profile, rec["resource"], topic_analysis
                )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting learning resource recommendations: {e}")
            return []
    
    def _generate_resource_explanation(self, user_profile: Dict, resource: Dict, 
                                     topic_analysis: Dict) -> str:
        """Generate explanation for why a resource is recommended"""
        
        try:
            user_interests = user_profile.get('skills', {}).get('interests', [])
            user_weaknesses = user_profile.get('skills', {}).get('weaknesses', [])
            resource_topics = resource.get('topics', [])
            
            explanations = []
            
            # Interest match
            interest_match = set(user_interests) & set(resource_topics)
            if interest_match:
                explanations.append(f"matches your interest in {', '.join(list(interest_match)[:2])}")
            
            # Weakness support
            weakness_match = set(user_weaknesses) & set(resource_topics)
            if weakness_match:
                explanations.append(f"helps strengthen {', '.join(list(weakness_match)[:2])}")
            
            # Level appropriateness
            user_level = user_profile.get('profile', {}).get('academic_level', '')
            resource_level = resource.get('level', '')
            if resource_level == user_level:
                explanations.append(f"appropriate for {user_level} level")
            
            # Quality
            rating = resource.get('average_rating', 0)
            if rating >= 4.0:
                explanations.append("highly rated by other learners")
            
            if explanations:
                return f"Recommended because it " + " and ".join(explanations)
            else:
                return "Good match for your learning goals"
                
        except Exception as e:
            logger.error(f"Error generating resource explanation: {e}")
            return "Recommended for your learning journey"
    
    async def update_models_with_new_data(self, users_data: List[Dict] = None,
                                        feedback_data: List[Dict] = None,
                                        interaction_data: List[Dict] = None) -> Dict[str, bool]:
        """Update all models with new data"""
        
        results = {}
        
        try:
            # Update recommendation model if user data provided
            if users_data and len(users_data) >= 3:
                results["recommendation_model"] = await self.train_recommendation_model(
                    users_data, interaction_data
                )
            
            # Update feedback model with new data
            if feedback_data:
                results["feedback_model"] = self.feedback_predictor.update_model_with_feedback(
                    feedback_data
                )
            
            logger.info(f"Model update results: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error updating models: {e}")
            return {"error": str(e)}
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all ML services and models"""
        
        return {
            "service_status": "active",
            "models": self.model_status,
            "topic_classifier_stats": self.topic_classifier.get_model_info(),
            "recommendation_model_stats": self.recommendation_model.get_model_stats(),
            "feedback_predictor_trained": self.feedback_predictor.is_trained,
            "last_status_check": datetime.utcnow().isoformat()
        }
    
    async def predict_match_success(self, user1_profile: Dict, user2_profile: Dict) -> Dict[str, Any]:
        """Predict likelihood of successful match between two users"""
        
        try:
            # Calculate compatibility score
            compatibility_factors = {
                "interest_overlap": 0,
                "level_compatibility": 0,
                "field_similarity": 0,
                "complementary_skills": 0,
                "activity_level_match": 0
            }
            
            # Interest overlap
            interests1 = set(user1_profile.get('skills', {}).get('interests', []))
            interests2 = set(user2_profile.get('skills', {}).get('interests', []))
            if interests1 and interests2:
                overlap = len(interests1 & interests2) / max(len(interests1), len(interests2))
                compatibility_factors["interest_overlap"] = overlap
            
            # Academic level compatibility
            level1 = user1_profile.get('profile', {}).get('academic_level', '')
            level2 = user2_profile.get('profile', {}).get('academic_level', '')
            level_diff = abs(self._level_to_number(level1) - self._level_to_number(level2))
            compatibility_factors["level_compatibility"] = max(0, 1 - level_diff * 0.3)
            
            # Field similarity
            field1 = user1_profile.get('profile', {}).get('field_of_study', '').lower()
            field2 = user2_profile.get('profile', {}).get('field_of_study', '').lower()
            if field1 and field2:
                compatibility_factors["field_similarity"] = 1.0 if field1 == field2 else 0.5 if field1 in field2 or field2 in field1 else 0.0
            
            # Complementary skills
            strengths1 = set(user1_profile.get('skills', {}).get('strengths', []))
            weaknesses2 = set(user2_profile.get('skills', {}).get('weaknesses', []))
            strengths2 = set(user2_profile.get('skills', {}).get('strengths', []))
            weaknesses1 = set(user1_profile.get('skills', {}).get('weaknesses', []))
            
            mutual_help = len((strengths1 & weaknesses2) | (strengths2 & weaknesses1))
            compatibility_factors["complementary_skills"] = min(1.0, mutual_help * 0.25)
            
            # Activity level match
            points1 = user1_profile.get('points', 0)
            points2 = user2_profile.get('points', 0)
            if points1 > 0 and points2 > 0:
                activity_ratio = min(points1, points2) / max(points1, points2)
                compatibility_factors["activity_level_match"] = activity_ratio
            
            # Calculate weighted overall score
            weights = {
                "interest_overlap": 0.3,
                "level_compatibility": 0.2,
                "field_similarity": 0.2,
                "complementary_skills": 0.2,
                "activity_level_match": 0.1
            }
            
            overall_score = sum(
                compatibility_factors[factor] * weights[factor]
                for factor in compatibility_factors
            )
            
            # Predict success probability
            success_probability = min(1.0, overall_score * 1.2)  # Slight boost for good matches
            
            return {
                "success_probability": round(success_probability, 3),
                "compatibility_score": round(overall_score, 3),
                "compatibility_factors": compatibility_factors,
                "prediction_confidence": 0.8,  # Static confidence for now
                "recommendation": "Highly recommended" if success_probability > 0.7 else 
                                "Recommended" if success_probability > 0.5 else 
                                "Moderate potential" if success_probability > 0.3 else 
                                "Low compatibility"
            }
            
        except Exception as e:
            logger.error(f"Error predicting match success: {e}")
            return {
                "success_probability": 0.5,
                "compatibility_score": 0.5,
                "error": str(e)
            }


# Global ML service instance
ml_service = MLService()