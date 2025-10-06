"""
Recommendation model for suggesting study partners and learning resources
"""
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
import logging
from typing import List, Dict, Tuple, Optional, Any

logger = logging.getLogger(__name__)


class RecommendationModel:
    def __init__(self):
        self.user_similarity_model = None
        self.content_model = None
        self.collaborative_model = None
        self.scaler = StandardScaler()
        self.svd = TruncatedSVD(n_components=50, random_state=42)
        
        self.user_features = None
        self.user_ids = None
        self.item_features = None
        self.item_ids = None
        
        self.is_trained = False
    
    def prepare_user_features(self, users_data: List[Dict]) -> np.ndarray:
        """Prepare user feature matrix for recommendations"""
        
        features = []
        user_ids = []
        
        for user in users_data:
            feature_vector = []
            
            # Basic profile features
            profile = user.get('profile', {})
            skills = user.get('skills', {})
            
            # Academic level (encoded)
            level_mapping = {"undergraduate": 1, "graduate": 2, "phd": 3, "postdoc": 4}
            academic_level = profile.get('academic_level', 'undergraduate')
            feature_vector.append(level_mapping.get(academic_level, 1))
            
            # Field of study (encoded - simplified)
            field_mapping = {
                "computer science": 1, "mathematics": 2, "physics": 3, "chemistry": 4,
                "biology": 5, "psychology": 6, "business": 7, "engineering": 8,
                "literature": 9, "history": 10
            }
            field = profile.get('field_of_study', '').lower()
            field_code = 0
            for key, value in field_mapping.items():
                if key in field:
                    field_code = value
                    break
            feature_vector.append(field_code)
            
            # Learning preferences (binary encoding)
            preferences = profile.get('learning_preferences', [])
            for pref in ['visual', 'auditory', 'kinesthetic', 'reading']:
                feature_vector.append(1 if pref in preferences else 0)
            
            # Skills metrics
            feature_vector.append(len(skills.get('interests', [])))
            feature_vector.append(len(skills.get('strengths', [])))
            feature_vector.append(len(skills.get('weaknesses', [])))
            
            # Gamification metrics
            feature_vector.append(user.get('points', 0))
            feature_vector.append(user.get('level', 1))
            
            # Activity metrics (would come from usage data)
            feature_vector.append(user.get('session_count', 0))
            feature_vector.append(user.get('avg_rating', 3.0))
            
            features.append(feature_vector)
            user_ids.append(str(user.get('_id', user.get('id'))))
        
        return np.array(features), user_ids
    
    def train_user_similarity_model(self, users_data: List[Dict]) -> bool:
        """Train user-based collaborative filtering model"""
        
        try:
            if len(users_data) < 3:
                logger.warning("Insufficient user data for training")
                return False
            
            # Prepare features
            features, user_ids = self.prepare_user_features(users_data)
            
            if features.size == 0:
                return False
            
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train nearest neighbors model
            n_neighbors = min(10, len(features))
            self.user_similarity_model = NearestNeighbors(
                n_neighbors=n_neighbors,
                metric='cosine',
                algorithm='brute'
            )
            self.user_similarity_model.fit(features_scaled)
            
            # Store for later use
            self.user_features = features_scaled
            self.user_ids = user_ids
            
            logger.info(f"User similarity model trained with {len(users_data)} users")
            return True
            
        except Exception as e:
            logger.error(f"Error training user similarity model: {e}")
            return False
    
    def train_content_based_model(self, items_data: List[Dict]) -> bool:
        """Train content-based recommendation model"""
        
        try:
            if len(items_data) < 3:
                logger.warning("Insufficient item data for content-based model")
                return False
            
            # Prepare item features (topics, difficulty, etc.)
            features = []
            item_ids = []
            
            for item in items_data:
                feature_vector = []
                
                # Topic categories (binary encoding)
                topics = item.get('topics', [])
                topic_categories = [
                    'computer science', 'mathematics', 'physics', 'chemistry',
                    'biology', 'psychology', 'business', 'engineering'
                ]
                
                for category in topic_categories:
                    has_category = any(category in topic.lower() for topic in topics)
                    feature_vector.append(1 if has_category else 0)
                
                # Difficulty level
                difficulty_mapping = {"beginner": 1, "intermediate": 2, "advanced": 3}
                difficulty = item.get('difficulty', 'intermediate')
                feature_vector.append(difficulty_mapping.get(difficulty, 2))
                
                # Duration preference
                feature_vector.append(item.get('duration_preference', 60))
                
                # Rating/popularity
                feature_vector.append(item.get('average_rating', 3.0))
                feature_vector.append(item.get('popularity_score', 0.5))
                
                features.append(feature_vector)
                item_ids.append(str(item.get('_id', item.get('id'))))
            
            self.item_features = np.array(features)
            self.item_ids = item_ids
            
            logger.info(f"Content-based model prepared with {len(items_data)} items")
            return True
            
        except Exception as e:
            logger.error(f"Error training content-based model: {e}")
            return False
    
    def train_collaborative_filtering(self, interaction_data: List[Dict]) -> bool:
        """Train collaborative filtering model using matrix factorization"""
        
        try:
            if len(interaction_data) < 10:
                logger.warning("Insufficient interaction data for collaborative filtering")
                return False
            
            # Create user-item interaction matrix
            df = pd.DataFrame(interaction_data)
            
            # Pivot to create user-item matrix
            user_item_matrix = df.pivot_table(
                index='user_id',
                columns='item_id', 
                values='rating',
                fill_value=0
            )
            
            # Apply SVD for dimensionality reduction
            if user_item_matrix.shape[1] > 50:
                matrix_reduced = self.svd.fit_transform(user_item_matrix.values)
            else:
                matrix_reduced = user_item_matrix.values
            
            # Train nearest neighbors on reduced matrix
            self.collaborative_model = NearestNeighbors(
                n_neighbors=min(10, len(matrix_reduced)),
                metric='cosine'
            )
            self.collaborative_model.fit(matrix_reduced)
            
            logger.info(f"Collaborative filtering model trained with {len(interaction_data)} interactions")
            return True
            
        except Exception as e:
            logger.error(f"Error training collaborative filtering: {e}")
            return False
    
    def recommend_users(self, user_profile: Dict, n_recommendations: int = 5, 
                       exclude_ids: List[str] = None) -> List[Dict]:
        """Recommend similar users for collaboration"""
        
        if not self.user_similarity_model or self.user_features is None:
            logger.warning("User similarity model not trained")
            return []
        
        try:
            # Prepare user feature vector
            user_features, _ = self.prepare_user_features([user_profile])
            if user_features.size == 0:
                return []
            
            user_features_scaled = self.scaler.transform(user_features)
            
            # Find similar users
            distances, indices = self.user_similarity_model.kneighbors(
                user_features_scaled, 
                n_neighbors=min(n_recommendations + 5, len(self.user_ids))
            )
            
            recommendations = []
            exclude_set = set(exclude_ids or [])
            current_user_id = str(user_profile.get('_id', user_profile.get('id', '')))
            exclude_set.add(current_user_id)
            
            for distance, idx in zip(distances[0], indices[0]):
                recommended_user_id = self.user_ids[idx]
                
                if recommended_user_id not in exclude_set:
                    similarity_score = 1 - distance  # Convert distance to similarity
                    
                    recommendations.append({
                        'user_id': recommended_user_id,
                        'similarity_score': float(similarity_score),
                        'recommendation_type': 'user_similarity'
                    })
                
                if len(recommendations) >= n_recommendations:
                    break
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating user recommendations: {e}")
            return []
    
    def recommend_learning_resources(self, user_profile: Dict, 
                                   available_resources: List[Dict],
                                   n_recommendations: int = 5) -> List[Dict]:
        """Recommend learning resources based on user profile"""
        
        try:
            user_interests = user_profile.get('skills', {}).get('interests', [])
            user_weaknesses = user_profile.get('skills', {}).get('weaknesses', [])
            user_level = user_profile.get('profile', {}).get('academic_level', 'undergraduate')
            
            resource_scores = []
            
            for resource in available_resources:
                score = 0
                
                # Topic relevance
                resource_topics = resource.get('topics', [])
                topic_relevance = len(set(user_interests + user_weaknesses) & set(resource_topics))
                score += topic_relevance * 0.4
                
                # Level appropriateness
                resource_level = resource.get('level', 'intermediate')
                if resource_level == user_level:
                    score += 0.3
                elif abs(self._level_to_number(resource_level) - self._level_to_number(user_level)) == 1:
                    score += 0.2
                
                # Resource quality
                score += resource.get('average_rating', 3.0) * 0.2
                
                # Popularity
                score += resource.get('popularity_score', 0.5) * 0.1
                
                resource_scores.append({
                    'resource': resource,
                    'score': score,
                    'resource_id': str(resource.get('_id', resource.get('id')))
                })
            
            # Sort by score and return top recommendations
            resource_scores.sort(key=lambda x: x['score'], reverse=True)
            
            recommendations = []
            for item in resource_scores[:n_recommendations]:
                recommendations.append({
                    'resource_id': item['resource_id'],
                    'resource': item['resource'],
                    'relevance_score': float(item['score']),
                    'recommendation_type': 'content_based'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating resource recommendations: {e}")
            return []
    
    def recommend_study_groups(self, user_profile: Dict, 
                             available_groups: List[Dict],
                             n_recommendations: int = 5) -> List[Dict]:
        """Recommend study groups based on user profile"""
        
        try:
            user_interests = user_profile.get('skills', {}).get('interests', [])
            user_field = user_profile.get('profile', {}).get('field_of_study', '').lower()
            user_level = user_profile.get('profile', {}).get('academic_level', 'undergraduate')
            
            group_scores = []
            
            for group in available_groups:
                score = 0
                
                # Topic/subject relevance
                group_topic = group.get('topic', '').lower()
                if any(interest.lower() in group_topic for interest in user_interests):
                    score += 0.4
                
                if user_field in group_topic:
                    score += 0.3
                
                # Group size (prefer not too large or too small)
                member_count = len(group.get('member_ids', []))
                max_members = group.get('max_members', 6)
                
                if 2 <= member_count <= max_members * 0.8:
                    score += 0.2
                elif member_count < 2:
                    score += 0.1
                
                # Activity level (newer groups might be more active)
                # This is simplified - in practice, you'd look at actual activity metrics
                score += 0.1
                
                group_scores.append({
                    'group': group,
                    'score': score,
                    'group_id': str(group.get('_id', group.get('id')))
                })
            
            # Sort by score
            group_scores.sort(key=lambda x: x['score'], reverse=True)
            
            recommendations = []
            for item in group_scores[:n_recommendations]:
                recommendations.append({
                    'group_id': item['group_id'],
                    'group': item['group'],
                    'relevance_score': float(item['score']),
                    'recommendation_type': 'group_matching'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating group recommendations: {e}")
            return []
    
    def get_hybrid_recommendations(self, user_profile: Dict, 
                                 available_users: List[Dict],
                                 interaction_history: List[Dict] = None,
                                 n_recommendations: int = 5) -> List[Dict]:
        """Generate hybrid recommendations combining multiple approaches"""
        
        recommendations = []
        
        # User similarity recommendations
        user_recs = self.recommend_users(user_profile, n_recommendations)
        for rec in user_recs:
            rec['approach'] = 'collaborative'
            rec['weight'] = 0.6
        recommendations.extend(user_recs)
        
        # Content-based recommendations would go here
        # (This would need content/resource data)
        
        # Combine and weight recommendations
        final_recommendations = []
        seen_users = set()
        
        for rec in recommendations:
            user_id = rec['user_id']
            if user_id not in seen_users:
                seen_users.add(user_id)
                final_recommendations.append(rec)
            
            if len(final_recommendations) >= n_recommendations:
                break
        
        return final_recommendations
    
    def _level_to_number(self, level: str) -> int:
        """Convert academic level to number for comparison"""
        mapping = {"undergraduate": 1, "graduate": 2, "phd": 3, "postdoc": 4}
        return mapping.get(level.lower(), 2)
    
    def update_model_with_feedback(self, feedback_data: List[Dict]) -> bool:
        """Update model based on user feedback"""
        
        try:
            # This would implement online learning or model retraining
            # For now, just log the feedback
            logger.info(f"Received {len(feedback_data)} feedback items for model improvement")
            
            # In a real implementation, you would:
            # 1. Analyze feedback patterns
            # 2. Identify model weaknesses
            # 3. Retrain with updated data
            # 4. A/B test new model version
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating model with feedback: {e}")
            return False
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get model statistics and performance metrics"""
        
        stats = {
            "user_similarity_model_trained": self.user_similarity_model is not None,
            "content_model_trained": self.item_features is not None,
            "collaborative_model_trained": self.collaborative_model is not None,
            "n_users_in_model": len(self.user_ids) if self.user_ids else 0,
            "n_items_in_model": len(self.item_ids) if self.item_ids else 0,
        }
        
        return stats


# Global model instance
recommendation_model = RecommendationModel()