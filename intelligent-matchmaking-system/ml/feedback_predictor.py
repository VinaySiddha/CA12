"""
Feedback prediction model for analyzing sentiment and extracting insights
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import pickle
import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedbackPredictor:
    def __init__(self):
        self.sentiment_model = None
        self.topic_model = None
        self.quality_model = None
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
        
        self.sentiment_labels = ['negative', 'neutral', 'positive']
        self.quality_labels = ['poor', 'average', 'good', 'excellent']
        
        self.is_trained = False
        self._initialize_training_data()
    
    def _initialize_training_data(self):
        """Initialize synthetic training data for feedback analysis"""
        
        # Sentiment training data
        self.sentiment_training_data = [
            # Positive feedback
            ("The study session was incredibly helpful and engaging", "positive"),
            ("My partner was knowledgeable and patient", "positive"),
            ("Excellent collaboration, learned a lot", "positive"),
            ("Great explanation of complex concepts", "positive"),
            ("Very supportive and encouraging learning environment", "positive"),
            ("Outstanding preparation and materials provided", "positive"),
            ("Highly effective teaching methods", "positive"),
            ("Perfect match for my learning style", "positive"),
            ("Exceeded my expectations completely", "positive"),
            ("Wonderful experience, would definitely recommend", "positive"),
            ("Clear communication and well-structured session", "positive"),
            ("Helped me understand difficult topics easily", "positive"),
            ("Professional and well-prepared partner", "positive"),
            ("Motivating and inspiring session", "positive"),
            ("Excellent use of examples and analogies", "positive"),
            
            # Neutral feedback
            ("The session was okay, covered basic material", "neutral"),
            ("Average experience, met expectations", "neutral"),
            ("Standard session, nothing special", "neutral"),
            ("Covered the topics as planned", "neutral"),
            ("Normal pacing, adequate explanation", "neutral"),
            ("Regular study session, went as expected", "neutral"),
            ("Decent collaboration, could be improved", "neutral"),
            ("Satisfactory but not exceptional", "neutral"),
            ("Met the basic requirements", "neutral"),
            ("Standard quality session", "neutral"),
            ("Acceptable level of preparation", "neutral"),
            ("Average communication skills", "neutral"),
            ("Basic understanding achieved", "neutral"),
            ("Routine study session", "neutral"),
            ("Moderate engagement level", "neutral"),
            
            # Negative feedback
            ("Partner was unprepared and disorganized", "negative"),
            ("Wasted time, didn't learn much", "negative"),
            ("Poor explanation of concepts", "negative"),
            ("Unengaged and distracted throughout", "negative"),
            ("Disappointing experience overall", "negative"),
            ("Lacks knowledge in the subject area", "negative"),
            ("Unprofessional behavior during session", "negative"),
            ("Confusing explanations made things worse", "negative"),
            ("No effort put into preparation", "negative"),
            ("Unhelpful and impatient attitude", "negative"),
            ("Session was boring and ineffective", "negative"),
            ("Failed to address my learning needs", "negative"),
            ("Poor time management and organization", "negative"),
            ("Negative and discouraging environment", "negative"),
            ("Complete waste of time", "negative"),
        ]
        
        # Quality assessment training data
        self.quality_training_data = [
            # Excellent quality
            ("Exceptional depth of knowledge and teaching ability", "excellent"),
            ("Perfect preparation with comprehensive materials", "excellent"),
            ("Outstanding communication and clarity", "excellent"),
            ("Exceeded all expectations thoroughly", "excellent"),
            ("Masterful explanation of complex topics", "excellent"),
            ("Superb organization and structure", "excellent"),
            ("Brilliant use of examples and analogies", "excellent"),
            ("Exceptional patience and support", "excellent"),
            
            # Good quality
            ("Well-prepared with good materials", "good"),
            ("Clear explanations and good examples", "good"),
            ("Knowledgeable and helpful partner", "good"),
            ("Good organization and time management", "good"),
            ("Effective teaching methods used", "good"),
            ("Strong understanding of subject matter", "good"),
            ("Good communication skills displayed", "good"),
            ("Helpful and supportive throughout", "good"),
            
            # Average quality
            ("Basic preparation and materials", "average"),
            ("Standard explanation quality", "average"),
            ("Adequate knowledge level", "average"),
            ("Acceptable organization", "average"),
            ("Average communication skills", "average"),
            ("Standard session quality", "average"),
            ("Basic understanding demonstrated", "average"),
            ("Moderate helpfulness", "average"),
            
            # Poor quality
            ("Insufficient preparation evident", "poor"),
            ("Unclear and confusing explanations", "poor"),
            ("Limited knowledge of subject", "poor"),
            ("Poor organization and planning", "poor"),
            ("Ineffective communication", "poor"),
            ("Unhelpful attitude displayed", "poor"),
            ("Wasted time with poor structure", "poor"),
            ("Failed to meet basic expectations", "poor"),
        ]
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def train_sentiment_model(self) -> bool:
        """Train sentiment analysis model"""
        
        try:
            # Prepare training data
            texts, labels = zip(*self.sentiment_training_data)
            texts = [self.preprocess_text(text) for text in texts]
            
            # Create pipeline
            self.sentiment_model = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
                ('classifier', LogisticRegression(random_state=42))
            ])
            
            # Train model
            self.sentiment_model.fit(texts, labels)
            
            # Cross-validation
            cv_scores = cross_val_score(self.sentiment_model, texts, labels, cv=3, scoring='accuracy')
            logger.info(f"Sentiment model CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
            
            return True
            
        except Exception as e:
            logger.error(f"Error training sentiment model: {e}")
            return False
    
    def train_quality_model(self) -> bool:
        """Train quality assessment model"""
        
        try:
            # Prepare training data
            texts, labels = zip(*self.quality_training_data)
            texts = [self.preprocess_text(text) for text in texts]
            
            # Create pipeline
            self.quality_model = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
                ('classifier', MultinomialNB(alpha=0.1))
            ])
            
            # Train model
            self.quality_model.fit(texts, labels)
            
            # Cross-validation
            cv_scores = cross_val_score(self.quality_model, texts, labels, cv=3, scoring='accuracy')
            logger.info(f"Quality model CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
            
            return True
            
        except Exception as e:
            logger.error(f"Error training quality model: {e}")
            return False
    
    def train_all_models(self) -> bool:
        """Train all feedback analysis models"""
        
        sentiment_success = self.train_sentiment_model()
        quality_success = self.train_quality_model()
        
        self.is_trained = sentiment_success and quality_success
        
        if self.is_trained:
            logger.info("All feedback models trained successfully")
        else:
            logger.warning("Some feedback models failed to train")
        
        return self.is_trained
    
    def predict_sentiment(self, feedback_text: str) -> Dict[str, Any]:
        """Predict sentiment of feedback text"""
        
        if not self.sentiment_model:
            return {"sentiment": "neutral", "confidence": 0.0, "error": "Model not trained"}
        
        try:
            processed_text = self.preprocess_text(feedback_text)
            
            if not processed_text.strip():
                return {"sentiment": "neutral", "confidence": 0.0, "error": "Empty text"}
            
            # Predict sentiment
            prediction = self.sentiment_model.predict([processed_text])[0]
            probabilities = self.sentiment_model.predict_proba([processed_text])[0]
            
            # Get confidence (highest probability)
            max_prob_idx = np.argmax(probabilities)
            confidence = probabilities[max_prob_idx]
            
            # Create probability distribution
            prob_dist = {
                label: float(prob) 
                for label, prob in zip(self.sentiment_labels, probabilities)
            }
            
            return {
                "sentiment": prediction,
                "confidence": float(confidence),
                "probabilities": prob_dist,
                "processed_text": processed_text
            }
            
        except Exception as e:
            logger.error(f"Error predicting sentiment: {e}")
            return {"sentiment": "neutral", "confidence": 0.0, "error": str(e)}
    
    def predict_quality(self, feedback_text: str) -> Dict[str, Any]:
        """Predict quality assessment from feedback text"""
        
        if not self.quality_model:
            return {"quality": "average", "confidence": 0.0, "error": "Model not trained"}
        
        try:
            processed_text = self.preprocess_text(feedback_text)
            
            if not processed_text.strip():
                return {"quality": "average", "confidence": 0.0, "error": "Empty text"}
            
            # Predict quality
            prediction = self.quality_model.predict([processed_text])[0]
            probabilities = self.quality_model.predict_proba([processed_text])[0]
            
            # Get confidence
            max_prob_idx = np.argmax(probabilities)
            confidence = probabilities[max_prob_idx]
            
            # Create probability distribution
            prob_dist = {
                label: float(prob) 
                for label, prob in zip(self.quality_labels, probabilities)
            }
            
            return {
                "quality": prediction,
                "confidence": float(confidence),
                "probabilities": prob_dist,
                "processed_text": processed_text
            }
            
        except Exception as e:
            logger.error(f"Error predicting quality: {e}")
            return {"quality": "average", "confidence": 0.0, "error": str(e)}
    
    def analyze_feedback_comprehensive(self, feedback_text: str, 
                                     numerical_rating: Optional[float] = None) -> Dict[str, Any]:
        """Comprehensive feedback analysis combining multiple approaches"""
        
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "original_text": feedback_text,
            "numerical_rating": numerical_rating
        }
        
        # Sentiment analysis
        sentiment_result = self.predict_sentiment(feedback_text)
        analysis["sentiment_analysis"] = sentiment_result
        
        # Quality assessment
        quality_result = self.predict_quality(feedback_text)
        analysis["quality_assessment"] = quality_result
        
        # Text statistics
        analysis["text_statistics"] = self._get_text_statistics(feedback_text)
        
        # Key phrases extraction
        analysis["key_phrases"] = self._extract_key_phrases(feedback_text)
        
        # Overall score calculation
        analysis["overall_score"] = self._calculate_overall_score(
            sentiment_result, quality_result, numerical_rating
        )
        
        # Insights and recommendations
        analysis["insights"] = self._generate_insights(analysis)
        
        return analysis
    
    def _get_text_statistics(self, text: str) -> Dict[str, Any]:
        """Extract basic text statistics"""
        
        words = text.split()
        sentences = text.split('.')
        
        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "avg_word_length": np.mean([len(word) for word in words]) if words else 0,
            "text_length": len(text)
        }
    
    def _extract_key_phrases(self, text: str, n_phrases: int = 5) -> List[str]:
        """Extract key phrases from feedback text"""
        
        try:
            processed_text = self.preprocess_text(text)
            words = processed_text.split()
            
            # Simple approach: find repeated words or important terms
            # In practice, you might use more sophisticated NLP techniques
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Skip short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency and return top phrases
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            key_phrases = [word for word, freq in top_words[:n_phrases]]
            
            return key_phrases
            
        except Exception as e:
            logger.error(f"Error extracting key phrases: {e}")
            return []
    
    def _calculate_overall_score(self, sentiment_result: Dict, quality_result: Dict, 
                               numerical_rating: Optional[float]) -> float:
        """Calculate overall feedback score"""
        
        try:
            # Base score from sentiment
            sentiment_scores = {"negative": 1.0, "neutral": 3.0, "positive": 5.0}
            sentiment_score = sentiment_scores.get(sentiment_result.get("sentiment", "neutral"), 3.0)
            sentiment_confidence = sentiment_result.get("confidence", 0.5)
            
            # Quality score
            quality_scores = {"poor": 1.0, "average": 2.5, "good": 4.0, "excellent": 5.0}
            quality_score = quality_scores.get(quality_result.get("quality", "average"), 2.5)
            quality_confidence = quality_result.get("confidence", 0.5)
            
            # Weighted combination
            ml_score = (sentiment_score * sentiment_confidence + quality_score * quality_confidence) / 2
            
            # If numerical rating is provided, combine with ML predictions
            if numerical_rating is not None:
                overall_score = (ml_score + numerical_rating) / 2
            else:
                overall_score = ml_score
            
            return round(overall_score, 2)
            
        except Exception as e:
            logger.error(f"Error calculating overall score: {e}")
            return 3.0
    
    def _generate_insights(self, analysis: Dict) -> List[str]:
        """Generate insights based on feedback analysis"""
        
        insights = []
        
        sentiment = analysis.get("sentiment_analysis", {}).get("sentiment", "neutral")
        quality = analysis.get("quality_assessment", {}).get("quality", "average")
        overall_score = analysis.get("overall_score", 3.0)
        
        # Sentiment-based insights
        if sentiment == "positive":
            insights.append("Positive feedback indicates successful learning experience")
        elif sentiment == "negative":
            insights.append("Negative sentiment suggests areas for improvement needed")
        
        # Quality-based insights
        if quality == "excellent":
            insights.append("High-quality session with exceptional delivery")
        elif quality == "poor":
            insights.append("Session quality needs significant improvement")
        
        # Score-based insights
        if overall_score >= 4.0:
            insights.append("Strong overall performance with high satisfaction")
        elif overall_score <= 2.0:
            insights.append("Low satisfaction score requires immediate attention")
        
        # Text analysis insights
        text_stats = analysis.get("text_statistics", {})
        if text_stats.get("word_count", 0) > 50:
            insights.append("Detailed feedback provides rich information for improvement")
        elif text_stats.get("word_count", 0) < 10:
            insights.append("Brief feedback may lack sufficient detail for analysis")
        
        return insights
    
    def batch_analyze_feedback(self, feedback_list: List[Dict]) -> List[Dict]:
        """Analyze multiple feedback items in batch"""
        
        results = []
        
        for feedback in feedback_list:
            text = feedback.get("feedback_text", "")
            rating = feedback.get("rating")
            feedback_id = feedback.get("id", feedback.get("_id"))
            
            analysis = self.analyze_feedback_comprehensive(text, rating)
            analysis["feedback_id"] = str(feedback_id)
            
            results.append(analysis)
        
        return results
    
    def get_feedback_trends(self, feedback_analyses: List[Dict]) -> Dict[str, Any]:
        """Analyze trends across multiple feedback items"""
        
        if not feedback_analyses:
            return {}
        
        try:
            sentiments = [f.get("sentiment_analysis", {}).get("sentiment", "neutral") for f in feedback_analyses]
            qualities = [f.get("quality_assessment", {}).get("quality", "average") for f in feedback_analyses]
            scores = [f.get("overall_score", 3.0) for f in feedback_analyses]
            
            trends = {
                "total_feedback_count": len(feedback_analyses),
                "average_score": round(np.mean(scores), 2),
                "score_std": round(np.std(scores), 2),
                "sentiment_distribution": {
                    sentiment: sentiments.count(sentiment) for sentiment in self.sentiment_labels
                },
                "quality_distribution": {
                    quality: qualities.count(quality) for quality in self.quality_labels
                },
                "positive_feedback_ratio": sentiments.count("positive") / len(sentiments),
                "high_quality_ratio": (qualities.count("good") + qualities.count("excellent")) / len(qualities),
                "improvement_areas": self._identify_improvement_areas(feedback_analyses)
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing feedback trends: {e}")
            return {}
    
    def _identify_improvement_areas(self, feedback_analyses: List[Dict]) -> List[str]:
        """Identify areas that need improvement based on feedback patterns"""
        
        improvement_areas = []
        
        # Analyze negative feedback for common issues
        negative_feedback = [
            f for f in feedback_analyses 
            if f.get("sentiment_analysis", {}).get("sentiment") == "negative"
        ]
        
        if len(negative_feedback) > len(feedback_analyses) * 0.3:  # More than 30% negative
            improvement_areas.append("High negative feedback rate requires attention")
        
        # Analyze low quality feedback
        poor_quality = [
            f for f in feedback_analyses 
            if f.get("quality_assessment", {}).get("quality") in ["poor", "average"]
        ]
        
        if len(poor_quality) > len(feedback_analyses) * 0.4:  # More than 40% poor/average
            improvement_areas.append("Session quality needs improvement")
        
        # Check score distribution
        low_scores = [f for f in feedback_analyses if f.get("overall_score", 3.0) < 2.5]
        if len(low_scores) > len(feedback_analyses) * 0.25:  # More than 25% low scores
            improvement_areas.append("Overall satisfaction scores are concerning")
        
        return improvement_areas
    
    def save_models(self, model_path: str = "feedback_models.pkl") -> bool:
        """Save trained models to file"""
        
        try:
            models = {
                "sentiment_model": self.sentiment_model,
                "quality_model": self.quality_model,
                "is_trained": self.is_trained,
                "sentiment_labels": self.sentiment_labels,
                "quality_labels": self.quality_labels
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(models, f)
            
            logger.info(f"Models saved to {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
            return False
    
    def load_models(self, model_path: str = "feedback_models.pkl") -> bool:
        """Load trained models from file"""
        
        try:
            with open(model_path, 'rb') as f:
                models = pickle.load(f)
            
            self.sentiment_model = models["sentiment_model"]
            self.quality_model = models["quality_model"]
            self.is_trained = models["is_trained"]
            self.sentiment_labels = models["sentiment_labels"]
            self.quality_labels = models["quality_labels"]
            
            logger.info(f"Models loaded from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False


# Global model instance
feedback_predictor = FeedbackPredictor()

# Auto-train on import
try:
    feedback_predictor.train_all_models()
except Exception as e:
    logger.warning(f"Auto-training failed: {e}")