"""
Topic NLP model for processing and categorizing educational topics
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import logging
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)


class TopicNLPModel:
    def __init__(self):
        self.model = None
        self.categories = [
            "Computer Science",
            "Mathematics", 
            "Physics",
            "Chemistry",
            "Biology",
            "Psychology",
            "Business",
            "Engineering",
            "Literature",
            "History",
            "Other"
        ]
        
        # Create the model pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                lowercase=True
            )),
            ('classifier', MultinomialNB(alpha=1.0))
        ])
        
        self.is_trained = False
    
    def prepare_training_data(self) -> Tuple[List[str], List[str]]:
        """Prepare synthetic training data for topic classification"""
        
        # Sample training data for each category
        training_data = {
            "Computer Science": [
                "python programming", "machine learning algorithms", "data structures and algorithms",
                "web development", "artificial intelligence", "database design", "software engineering",
                "computer networks", "cybersecurity", "mobile app development", "cloud computing",
                "javascript react", "java programming", "c++ programming", "neural networks",
                "data science", "big data analytics", "computer graphics", "operating systems"
            ],
            
            "Mathematics": [
                "calculus derivatives", "linear algebra matrices", "statistics probability",
                "differential equations", "discrete mathematics", "number theory", "geometry proofs",
                "trigonometry functions", "algebra equations", "mathematical analysis",
                "complex numbers", "mathematical modeling", "optimization theory", "graph theory",
                "topology", "real analysis", "abstract algebra", "combinatorics"
            ],
            
            "Physics": [
                "quantum mechanics", "classical mechanics", "thermodynamics", "electromagnetism",
                "relativity theory", "particle physics", "nuclear physics", "optics",
                "wave physics", "statistical mechanics", "condensed matter", "astrophysics",
                "atomic physics", "plasma physics", "solid state physics", "field theory"
            ],
            
            "Chemistry": [
                "organic chemistry reactions", "inorganic chemistry", "physical chemistry",
                "analytical chemistry", "biochemistry", "chemical bonding", "thermochemistry",
                "electrochemistry", "chemical kinetics", "molecular chemistry", "polymer chemistry",
                "environmental chemistry", "medicinal chemistry", "materials chemistry"
            ],
            
            "Biology": [
                "molecular biology", "cell biology", "genetics DNA", "evolution theory",
                "ecology ecosystems", "microbiology", "anatomy physiology", "biochemistry",
                "immunology", "neurobiology", "developmental biology", "marine biology",
                "botany plants", "zoology animals", "bioinformatics", "biotechnology"
            ],
            
            "Psychology": [
                "cognitive psychology", "social psychology", "developmental psychology",
                "clinical psychology", "behavioral psychology", "neuropsychology",
                "personality psychology", "abnormal psychology", "research methods",
                "psychological statistics", "therapy counseling", "human behavior"
            ],
            
            "Business": [
                "marketing strategy", "financial management", "business administration",
                "operations management", "human resources", "entrepreneurship",
                "economics microeconomics", "accounting principles", "project management",
                "business analytics", "supply chain", "international business", "finance"
            ],
            
            "Engineering": [
                "mechanical engineering", "electrical engineering", "civil engineering",
                "chemical engineering", "aerospace engineering", "biomedical engineering",
                "industrial engineering", "materials engineering", "environmental engineering",
                "structural engineering", "fluid mechanics", "control systems"
            ],
            
            "Literature": [
                "english literature", "creative writing", "poetry analysis", "literary criticism",
                "world literature", "american literature", "british literature", "drama",
                "fiction writing", "literary theory", "comparative literature", "rhetoric"
            ],
            
            "History": [
                "world history", "american history", "european history", "ancient history",
                "medieval history", "modern history", "cultural history", "political history",
                "social history", "military history", "art history", "historical research"
            ]
        }
        
        # Create texts and labels
        texts = []
        labels = []
        
        for category, topics in training_data.items():
            for topic in topics:
                texts.append(topic)
                labels.append(category)
                
                # Add some variations
                variations = [
                    f"help with {topic}",
                    f"learning {topic}",
                    f"studying {topic}",
                    f"need help in {topic}",
                    f"tutoring for {topic}"
                ]
                
                for variation in variations:
                    texts.append(variation)
                    labels.append(category)
        
        return texts, labels
    
    def train(self, texts: Optional[List[str]] = None, labels: Optional[List[str]] = None) -> Dict[str, float]:
        """Train the topic classification model"""
        
        if texts is None or labels is None:
            texts, labels = self.prepare_training_data()
        
        logger.info(f"Training topic model with {len(texts)} samples")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Train the model
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Model training completed. Accuracy: {accuracy:.3f}")
        logger.info(f"Classification report:\n{classification_report(y_test, y_pred)}")
        
        self.is_trained = True
        
        return {
            "accuracy": accuracy,
            "train_samples": len(X_train),
            "test_samples": len(X_test)
        }
    
    def predict_topic(self, text: str) -> Dict[str, float]:
        """Predict topic category for given text"""
        
        if not self.is_trained:
            logger.warning("Model not trained. Training with default data.")
            self.train()
        
        if not text or not text.strip():
            return {"Other": 1.0}
        
        try:
            # Get prediction probabilities
            probabilities = self.pipeline.predict_proba([text.lower()])[0]
            classes = self.pipeline.classes_
            
            # Create probability dictionary
            topic_probs = {}
            for class_name, prob in zip(classes, probabilities):
                topic_probs[class_name] = float(prob)
            
            return topic_probs
            
        except Exception as e:
            logger.error(f"Error predicting topic: {e}")
            return {"Other": 1.0}
    
    def predict_topics_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        """Predict topics for multiple texts"""
        
        if not self.is_trained:
            self.train()
        
        results = []
        for text in texts:
            results.append(self.predict_topic(text))
        
        return results
    
    def get_top_topic(self, text: str) -> Tuple[str, float]:
        """Get the most likely topic for given text"""
        
        probabilities = self.predict_topic(text)
        
        if not probabilities:
            return "Other", 0.0
        
        top_topic = max(probabilities, key=probabilities.get)
        confidence = probabilities[top_topic]
        
        return top_topic, confidence
    
    def extract_keywords(self, text: str, n_keywords: int = 10) -> List[Tuple[str, float]]:
        """Extract important keywords from text"""
        
        if not self.is_trained:
            self.train()
        
        try:
            # Get TF-IDF features
            tfidf = self.pipeline.named_steps['tfidf']
            feature_names = tfidf.get_feature_names_out()
            
            # Transform the text
            text_vector = tfidf.transform([text.lower()])
            
            # Get feature scores
            scores = text_vector.toarray()[0]
            
            # Get top keywords
            feature_scores = list(zip(feature_names, scores))
            feature_scores = [(word, score) for word, score in feature_scores if score > 0]
            feature_scores.sort(key=lambda x: x[1], reverse=True)
            
            return feature_scores[:n_keywords]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def suggest_related_topics(self, topic: str, n_suggestions: int = 5) -> List[str]:
        """Suggest related topics based on the given topic"""
        
        topic_relationships = {
            "Computer Science": ["Mathematics", "Engineering", "Physics"],
            "Mathematics": ["Computer Science", "Physics", "Engineering"],
            "Physics": ["Mathematics", "Chemistry", "Engineering"],
            "Chemistry": ["Physics", "Biology", "Engineering"],
            "Biology": ["Chemistry", "Psychology"],
            "Psychology": ["Biology", "Other"],
            "Business": ["Mathematics", "Psychology"],
            "Engineering": ["Mathematics", "Physics", "Computer Science"],
            "Literature": ["History", "Psychology"],
            "History": ["Literature", "Other"]
        }
        
        related = topic_relationships.get(topic, [])
        
        # Add some general suggestions if not enough
        all_topics = list(self.categories)
        for t in all_topics:
            if t != topic and t not in related and len(related) < n_suggestions:
                related.append(t)
        
        return related[:n_suggestions]
    
    def save_model(self, filepath: str) -> bool:
        """Save the trained model to file"""
        
        if not self.is_trained:
            logger.error("Cannot save untrained model")
            return False
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'pipeline': self.pipeline,
                    'categories': self.categories,
                    'is_trained': self.is_trained
                }, f)
            
            logger.info(f"Model saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """Load a trained model from file"""
        
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.pipeline = model_data['pipeline']
            self.categories = model_data['categories']
            self.is_trained = model_data['is_trained']
            
            logger.info(f"Model loaded from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, any]:
        """Get information about the model"""
        
        return {
            "is_trained": self.is_trained,
            "categories": self.categories,
            "n_categories": len(self.categories),
            "model_type": "Naive Bayes with TF-IDF",
            "features": "TF-IDF with 1-2 grams, max 5000 features"
        }


# Global model instance
topic_model = TopicNLPModel()

# Train the model on import if not already trained
if not topic_model.is_trained:
    try:
        topic_model.train()
        logger.info("Topic NLP model trained successfully")
    except Exception as e:
        logger.error(f"Failed to train topic model: {e}")