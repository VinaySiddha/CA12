"""
NLP service for text processing and topic extraction
"""
import spacy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

# Try to load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy English model not found. Please install with: python -m spacy download en_core_web_sm")
    nlp = None

# Download NLTK data if needed
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception as e:
    logger.warning(f"Could not download NLTK data: {e}")


class NLPService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Common academic topics for fallback
        self.common_topics = [
            "mathematics", "algebra", "calculus", "statistics", "geometry",
            "physics", "chemistry", "biology", "computer science", "programming",
            "python", "java", "javascript", "machine learning", "data science",
            "artificial intelligence", "algorithms", "data structures",
            "english", "literature", "writing", "history", "psychology",
            "economics", "business", "marketing", "finance", "accounting"
        ]
    
    def extract_topics_from_text(self, text: str) -> List[str]:
        """Extract academic topics from text using NLP"""
        if not text or not text.strip():
            return []
        
        topics = []
        
        # Use spaCy if available
        if nlp:
            topics.extend(self._extract_with_spacy(text))
        
        # Use keyword matching as fallback
        topics.extend(self._extract_with_keywords(text))
        
        # Remove duplicates and return
        return list(set(topics))
    
    def _extract_with_spacy(self, text: str) -> List[str]:
        """Extract topics using spaCy NER and keyword matching"""
        topics = []
        
        try:
            doc = nlp(text.lower())
            
            # Extract named entities that might be academic subjects
            for ent in doc.ents:
                if ent.label_ in ["ORG", "PRODUCT", "EVENT", "WORK_OF_ART"]:
                    # Check if entity relates to academic topics
                    entity_text = ent.text.lower()
                    for topic in self.common_topics:
                        if topic in entity_text or entity_text in topic:
                            topics.append(topic)
                            break
            
            # Extract noun phrases that might be topics
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.lower()
                for topic in self.common_topics:
                    if topic in chunk_text:
                        topics.append(topic)
                        break
        
        except Exception as e:
            logger.error(f"Error in spaCy processing: {e}")
        
        return topics
    
    def _extract_with_keywords(self, text: str) -> List[str]:
        """Extract topics using keyword matching"""
        topics = []
        text_lower = text.lower()
        
        for topic in self.common_topics:
            if topic in text_lower:
                topics.append(topic)
        
        return topics
    
    def categorize_skill_level(self, description: str) -> str:
        """Categorize skill level from description"""
        description_lower = description.lower()
        
        beginner_keywords = ["beginner", "basic", "introduction", "starting", "new to", "learning", "help with"]
        intermediate_keywords = ["intermediate", "some experience", "familiar with", "working knowledge"]
        advanced_keywords = ["advanced", "expert", "proficient", "experienced", "master", "teach", "mentor"]
        
        advanced_score = sum(1 for keyword in advanced_keywords if keyword in description_lower)
        intermediate_score = sum(1 for keyword in intermediate_keywords if keyword in description_lower)
        beginner_score = sum(1 for keyword in beginner_keywords if keyword in description_lower)
        
        if advanced_score > max(intermediate_score, beginner_score):
            return "advanced"
        elif intermediate_score > beginner_score:
            return "intermediate"
        else:
            return "beginner"
    
    def suggest_learning_path(self, current_topics: List[str], target_topics: List[str]) -> List[str]:
        """Suggest a learning path from current to target topics"""
        # This is a simplified learning path suggestion
        # In a real implementation, this would use more sophisticated curriculum planning
        
        learning_paths = {
            "programming": ["python", "data structures", "algorithms", "machine learning"],
            "mathematics": ["algebra", "calculus", "statistics", "linear algebra"],
            "data science": ["statistics", "python", "machine learning", "data analysis"],
            "computer science": ["programming", "data structures", "algorithms", "computer systems"]
        }
        
        suggested_path = []
        
        for target in target_topics:
            target_lower = target.lower()
            
            # Find matching learning path
            for domain, path in learning_paths.items():
                if target_lower in path or any(topic in target_lower for topic in path):
                    # Add prerequisites not already known
                    for prereq in path:
                        if prereq not in [topic.lower() for topic in current_topics]:
                            suggested_path.append(prereq)
                    break
        
        return list(dict.fromkeys(suggested_path))  # Remove duplicates while preserving order
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        if not text1 or not text2:
            return 0.0
        
        try:
            # Use TF-IDF vectorization
            texts = [text1.lower(), text2.lower()]
            vectors = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            
            return float(similarity)
        
        except Exception as e:
            logger.error(f"Error calculating text similarity: {e}")
            return 0.0
    
    def extract_learning_preferences(self, text: str) -> List[str]:
        """Extract learning preferences from text"""
        preferences = []
        text_lower = text.lower()
        
        preference_keywords = {
            "visual": ["visual", "diagrams", "charts", "images", "see", "pictures", "graphics"],
            "auditory": ["audio", "listen", "hear", "verbal", "discussion", "explain", "talk"],
            "kinesthetic": ["hands-on", "practice", "doing", "interactive", "exercises", "practical"],
            "reading": ["reading", "text", "written", "books", "articles", "documentation"]
        }
        
        for preference, keywords in preference_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                preferences.append(preference)
        
        return preferences if preferences else ["reading"]  # Default to reading
    
    def cluster_topics(self, topic_texts: List[str], n_clusters: int = 5) -> Dict[int, List[str]]:
        """Cluster topics using K-means"""
        if not topic_texts or len(topic_texts) < n_clusters:
            return {0: topic_texts}
        
        try:
            # Vectorize texts
            vectors = self.vectorizer.fit_transform(topic_texts)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=min(n_clusters, len(topic_texts)), random_state=42)
            cluster_labels = kmeans.fit_predict(vectors)
            
            # Group topics by cluster
            clusters = {}
            for i, label in enumerate(cluster_labels):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(topic_texts[i])
            
            return clusters
        
        except Exception as e:
            logger.error(f"Error in topic clustering: {e}")
            return {0: topic_texts}


# Global instance
nlp_service = NLPService()