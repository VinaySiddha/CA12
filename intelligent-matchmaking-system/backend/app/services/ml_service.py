"""
Machine Learning service for recommendations and predictions
"""
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple, Any
import logging
import sys
import os
import importlib.util

# Add ml module to path
ml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ml'))
if ml_path not in sys.path:
    sys.path.append(ml_path)

# Try to import from ml module
try:
    from ml.recommendation_model import RecommendationModel
    recommendation_model_imported = True
except ImportError:
    recommendation_model_imported = False
    logger = logging.getLogger(__name__)
    logger.warning("Could not import RecommendationModel from ml module. Using fallback model.")

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self):
        self.user_recommender = None
        self.topic_recommender = None
        self.success_predictor = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=10)
        
        # Initialize the ML recommendation model from imported module
        if recommendation_model_imported:
            try:
                self.recommendation_model = RecommendationModel()
                logger.info("Successfully initialized RecommendationModel from ml module")
            except Exception as e:
                logger.error(f"Error initializing RecommendationModel: {e}")
                self.recommendation_model = None
        else:
            self.recommendation_model = None
        
    def train_user_recommender(self, user_data: List[Dict]) -> bool:
        """Train user recommendation model using collaborative filtering"""
        try:
            if len(user_data) < 5:  # Need minimum data
                logger.warning("Insufficient data to train user recommender")
                return False
            
            # Create user feature matrix
            features = self._extract_user_features(user_data)
            
            if len(features) == 0:
                return False
            
            # Train nearest neighbors model
            self.user_recommender = NearestNeighbors(
                n_neighbors=min(10, len(features)),
                metric='cosine'
            )
            self.user_recommender.fit(features)
            
            logger.info("User recommender model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training user recommender: {e}")
            return False
    
    def recommend_users(self, user_profile: Dict, n_recommendations: int = 5) -> List[Dict]:
        """Recommend users based on profile similarity"""
        # Try the advanced ML model first
        if self.recommendation_model is not None:
            try:
                # Prepare all users
                all_users = self._get_all_users_for_model()
                
                # Train model if not already trained
                if not self.recommendation_model.user_similarity_model:
                    logger.info("Training recommendation model with advanced algorithm")
                    trained = self.recommendation_model.train_user_similarity_model(all_users)
                    if not trained:
                        logger.warning("Could not train advanced recommendation model")
                
                # Get recommendations from the advanced model
                if self.recommendation_model.user_similarity_model:
                    user_id = str(user_profile.get('_id', ''))
                    exclude_ids = [user_id]  # Exclude self
                    
                    recommendations = self.recommendation_model.recommend_users(
                        user_profile, n_recommendations, exclude_ids
                    )
                    
                    if recommendations:
                        logger.info(f"Generated {len(recommendations)} recommendations using advanced model")
                        return recommendations
            except Exception as e:
                logger.error(f"Error using advanced recommendation model: {e}")
        
        # Fallback to simple recommender
        logger.info("Using simple recommender as fallback")
        if not self.user_recommender:
            logger.warning("Simple user recommender not trained")
            return []
        
        try:
            # Extract features for the target user
            user_features = self._extract_single_user_features(user_profile)
            
            if not user_features:
                return []
            
            # Find similar users
            distances, indices = self.user_recommender.kneighbors(
                [user_features], 
                n_neighbors=min(n_recommendations + 1, self.user_recommender.n_samples_fit_)
            )
            
            recommendations = []
            for i, (distance, index) in enumerate(zip(distances[0], indices[0])):
                if i == 0:  # Skip self
                    continue
                    
                recommendations.append({
                    "user_index": int(index),
                    "similarity_score": float(1 - distance),  # Convert distance to similarity
                    "rank": i
                })
            
            return recommendations[:n_recommendations]
            
        except Exception as e:
            logger.error(f"Error generating user recommendations: {e}")
            return []
            
    def _get_all_users_for_model(self) -> List[Dict]:
        """Get all users from database to use in recommendation model
        This is dynamically set by the matchmaking service, allowing the model
        to work with the most up-to-date user data."""
        return []  # Dynamically overridden by matchmaking service
    
    def train_topic_recommender(self, interaction_data: List[Dict]) -> bool:
        """Train topic recommendation model"""
        try:
            if len(interaction_data) < 10:
                logger.warning("Insufficient interaction data to train topic recommender")
                return False
            
            # Create user-topic interaction matrix
            df = pd.DataFrame(interaction_data)
            
            if df.empty:
                return False
            
            # Create pivot table (user x topic)
            user_topic_matrix = df.pivot_table(
                index='user_id',
                columns='topic',
                values='rating',
                fill_value=0
            )
            
            # Train model
            self.topic_recommender = NearestNeighbors(
                n_neighbors=min(10, len(user_topic_matrix.columns)),
                metric='cosine'
            )
            self.topic_recommender.fit(user_topic_matrix.T)  # Transpose to get topic similarity
            
            logger.info("Topic recommender model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training topic recommender: {e}")
            return False
    
    def recommend_topics(self, user_topic_preferences: Dict, n_recommendations: int = 5) -> List[str]:
        """Recommend topics based on user preferences"""
        if not self.topic_recommender:
            logger.warning("Topic recommender not trained")
            return self._fallback_topic_recommendations(user_topic_preferences)
        
        try:
            # Create user preference vector
            # This would need to match the training data structure
            # For now, return fallback recommendations
            return self._fallback_topic_recommendations(user_topic_preferences)
            
        except Exception as e:
            logger.error(f"Error generating topic recommendations: {e}")
            return self._fallback_topic_recommendations(user_topic_preferences)
    
    def train_success_predictor(self, training_data: List[Dict]) -> bool:
        """Train model to predict match success"""
        try:
            if len(training_data) < 20:
                logger.warning("Insufficient data to train success predictor")
                return False
            
            df = pd.DataFrame(training_data)
            
            # Extract features
            X = self._extract_match_features(df)
            y = df['success'].values  # Assuming binary success indicator
            
            if len(X) == 0:
                return False
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Apply PCA if too many features
            if X_scaled.shape[1] > 10:
                X_scaled = self.pca.fit_transform(X_scaled)
            
            # Train Random Forest classifier
            self.success_predictor = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            self.success_predictor.fit(X_scaled, y)
            
            logger.info("Success predictor model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training success predictor: {e}")
            return False
    
    def predict_match_success(self, match_features: Dict) -> float:
        """Predict probability of match success"""
        if not self.success_predictor:
            logger.warning("Success predictor not trained")
            return 0.5  # Default probability
        
        try:
            # Extract features
            features = self._extract_single_match_features(match_features)
            
            if not features:
                return 0.5
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Apply PCA if fitted
            if hasattr(self.pca, 'components_'):
                features_scaled = self.pca.transform(features_scaled)
            
            # Predict probability
            probability = self.success_predictor.predict_proba(features_scaled)[0][1]
            
            return float(probability)
            
        except Exception as e:
            logger.error(f"Error predicting match success: {e}")
            return 0.5
    
    def analyze_learning_patterns(self, user_data: List[Dict]) -> Dict[str, Any]:
        """Analyze learning patterns from user data"""
        try:
            if not user_data:
                return {}
            
            df = pd.DataFrame(user_data)
            
            analysis = {
                "most_popular_topics": self._get_popular_topics(df),
                "learning_preferences": self._analyze_learning_preferences(df),
                "optimal_session_duration": self._find_optimal_session_duration(df),
                "success_factors": self._identify_success_factors(df)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing learning patterns: {e}")
            return {}
    
    def _extract_user_features(self, user_data: List[Dict]) -> List[List[float]]:
        """Extract numerical features from user data"""
        features = []
        
        for user in user_data:
            feature_vector = []
            
            # Academic level (encoded)
            level_mapping = {"undergraduate": 1, "graduate": 2, "phd": 3, "postdoc": 4}
            level = user.get("profile", {}).get("academic_level", "undergraduate")
            feature_vector.append(level_mapping.get(level, 1))
            
            # Number of interests, strengths, weaknesses
            skills = user.get("skills", {})
            feature_vector.append(len(skills.get("interests", [])))
            feature_vector.append(len(skills.get("strengths", [])))
            feature_vector.append(len(skills.get("weaknesses", [])))
            
            # Learning preferences (binary encoding)
            preferences = user.get("profile", {}).get("learning_preferences", [])
            for pref_type in ["visual", "auditory", "kinesthetic", "reading"]:
                feature_vector.append(1 if pref_type in preferences else 0)
            
            # Gamification metrics
            feature_vector.append(user.get("points", 0))
            feature_vector.append(user.get("level", 1))
            
            features.append(feature_vector)
        
        return features
    
    def _extract_single_user_features(self, user_profile: Dict) -> List[float]:
        """Extract features for a single user"""
        return self._extract_user_features([user_profile])[0] if user_profile else []
    
    def _extract_match_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract features for match success prediction"""
        features = []
        
        for _, row in df.iterrows():
            feature_vector = []
            
            # Compatibility scores
            feature_vector.append(row.get('skill_compatibility', 0))
            feature_vector.append(row.get('schedule_compatibility', 0))
            feature_vector.append(row.get('learning_style_compatibility', 0))
            feature_vector.append(row.get('topic_relevance', 0))
            
            # User characteristics difference
            feature_vector.append(abs(row.get('mentor_level', 1) - row.get('mentee_level', 1)))
            feature_vector.append(row.get('common_interests_count', 0))
            
            features.append(feature_vector)
        
        return np.array(features)
    
    def _extract_single_match_features(self, match_data: Dict) -> List[float]:
        """Extract features for a single match"""
        feature_vector = []
        
        # Compatibility scores
        feature_vector.append(match_data.get('skill_compatibility', 0))
        feature_vector.append(match_data.get('schedule_compatibility', 0))
        feature_vector.append(match_data.get('learning_style_compatibility', 0))
        feature_vector.append(match_data.get('topic_relevance', 0))
        
        # Other features
        feature_vector.append(match_data.get('level_difference', 0))
        feature_vector.append(match_data.get('common_interests', 0))
        
        return feature_vector
    
    def _fallback_topic_recommendations(self, user_preferences: Dict) -> List[str]:
        """Fallback topic recommendations based on simple rules"""
        interests = user_preferences.get("interests", [])
        strengths = user_preferences.get("strengths", [])
        field_of_study = user_preferences.get("field_of_study", "").lower()
        
        recommendations = []
        
        # Topic mappings for different fields
        field_topics = {
            "computer science": ["algorithms", "data structures", "machine learning", "databases"],
            "mathematics": ["calculus", "linear algebra", "statistics", "discrete mathematics"],
            "physics": ["mechanics", "thermodynamics", "electromagnetism", "quantum physics"],
            "biology": ["genetics", "molecular biology", "ecology", "biochemistry"],
            "chemistry": ["organic chemistry", "physical chemistry", "analytical chemistry"],
            "psychology": ["cognitive psychology", "social psychology", "developmental psychology"],
            "business": ["marketing", "finance", "operations management", "strategy"]
        }
        
        # Add field-specific recommendations
        for field, topics in field_topics.items():
            if field in field_of_study:
                recommendations.extend(topics)
                break
        
        # Add related topics based on interests
        for interest in interests:
            interest_lower = interest.lower()
            if "programming" in interest_lower:
                recommendations.extend(["python", "javascript", "algorithms"])
            elif "data" in interest_lower:
                recommendations.extend(["statistics", "machine learning", "data analysis"])
            elif "math" in interest_lower:
                recommendations.extend(["calculus", "algebra", "statistics"])
        
        # Remove duplicates and limit
        recommendations = list(set(recommendations))
        return recommendations[:5]
    
    def _get_popular_topics(self, df: pd.DataFrame) -> List[str]:
        """Get most popular topics from data"""
        # This would analyze topic frequency in the data
        # For now, return common academic topics
        return ["mathematics", "computer science", "physics", "chemistry", "biology"]
    
    def _analyze_learning_preferences(self, df: pd.DataFrame) -> Dict[str, float]:
        """Analyze learning preference distribution"""
        # Placeholder analysis
        return {
            "visual": 0.35,
            "auditory": 0.25,
            "kinesthetic": 0.20,
            "reading": 0.20
        }
    
    def _find_optimal_session_duration(self, df: pd.DataFrame) -> int:
        """Find optimal session duration based on success rates"""
        # Placeholder - would analyze actual session data
        return 60  # minutes
    
    def _identify_success_factors(self, df: pd.DataFrame) -> List[str]:
        """Identify factors that contribute to success"""
        return [
            "High skill compatibility",
            "Regular session scheduling",
            "Active participation",
            "Clear learning objectives"
        ]


# Global instance
ml_service = MLService()