"""
Initialize ML package and expose main components
"""
from .topic_nlp_model import topic_classifier, TopicClassifier
from .recommendation_model import recommendation_model, RecommendationModel
from .feedback_predictor import feedback_predictor, FeedbackPredictor
from .ml_service import ml_service, MLService

__all__ = [
    'topic_classifier',
    'TopicClassifier',
    'recommendation_model', 
    'RecommendationModel',
    'feedback_predictor',
    'FeedbackPredictor',
    'ml_service',
    'MLService'
]

__version__ = "1.0.0"