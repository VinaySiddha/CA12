"""
Expert Matching Model - Intelligent matching between students and experts/professionals
based on shared interests, expertise areas, and learning goals
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ExpertMatchingModel:
    """
    ML Model for matching students with experts/professionals based on:
    - Student interests vs Expert expertise areas
    - Shared topics and keywords
    - Skill level compatibility
    - Learning goals alignment
    """
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            stop_words='english'
        )
        self.is_trained = False
        self.expert_profiles = []
        self.expert_vectors = None
        
    def prepare_expert_profile_text(self, expert: Dict) -> str:
        """Convert expert profile to text for TF-IDF"""
        text_parts = []
        
        # Expertise areas
        expertise = expert.get('expertise_areas', [])
        if expertise:
            text_parts.append(' '.join(expertise))
        
        # Skills and interests
        skills = expert.get('skills', {})
        if skills:
            interests = skills.get('interests', [])
            strengths = skills.get('strengths', [])
            text_parts.extend(interests + strengths)
        
        # Profile information
        profile = expert.get('profile', {})
        if profile:
            field = profile.get('field_of_study', '')
            if field:
                text_parts.append(field)
        
        # Job title and company
        job_title = expert.get('job_title', '')
        if job_title:
            text_parts.append(job_title)
            
        return ' '.join(text_parts).lower()
    
    def prepare_student_profile_text(self, student: Dict) -> str:
        """Convert student profile to text for TF-IDF"""
        text_parts = []
        
        # Skills and interests
        skills = student.get('skills', {})
        if skills:
            interests = skills.get('interests', [])
            weaknesses = skills.get('weaknesses', [])  # Areas they need help with
            text_parts.extend(interests + weaknesses)
        
        # Profile information
        profile = student.get('profile', {})
        if profile:
            field = profile.get('field_of_study', '')
            bio = profile.get('bio', '')
            if field:
                text_parts.append(field)
            if bio:
                text_parts.append(bio)
        
        return ' '.join(text_parts).lower()
    
    def train(self, experts: List[Dict]) -> bool:
        """Train the model with expert profiles"""
        try:
            if len(experts) < 1:
                logger.warning("No experts available for training")
                return False
            
            # Store expert profiles
            self.expert_profiles = experts
            
            # Prepare text representations
            expert_texts = [self.prepare_expert_profile_text(expert) for expert in experts]
            
            # Fit TF-IDF vectorizer
            self.expert_vectors = self.tfidf_vectorizer.fit_transform(expert_texts)
            
            self.is_trained = True
            logger.info(f"Expert matching model trained with {len(experts)} experts")
            return True
            
        except Exception as e:
            logger.error(f"Error training expert matching model: {e}")
            self.is_trained = False
            return False
    
    def calculate_interest_overlap_score(self, student: Dict, expert: Dict) -> float:
        """Calculate interest overlap between student and expert"""
        student_interests = set(student.get('skills', {}).get('interests', []))
        student_weaknesses = set(student.get('skills', {}).get('weaknesses', []))
        
        expert_expertise = set(expert.get('expertise_areas', []))
        expert_interests = set(expert.get('skills', {}).get('interests', []))
        expert_strengths = set(expert.get('skills', {}).get('strengths', []))
        
        # Combine student's learning needs
        student_needs = student_interests | student_weaknesses
        
        # Combine expert's teaching capabilities
        expert_capabilities = expert_expertise | expert_interests | expert_strengths
        
        if not student_needs or not expert_capabilities:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(student_needs & expert_capabilities)
        union = len(student_needs | expert_capabilities)
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_experience_compatibility(self, student: Dict, expert: Dict) -> float:
        """Calculate if expert's experience level is suitable for student"""
        student_level = student.get('profile', {}).get('academic_level', 'undergraduate')
        expert_years = expert.get('years_experience', 0)
        
        # Map academic levels to required experience
        level_experience_map = {
            'undergraduate': (0, 5),   # Prefer 0-5 years for undergrads
            'graduate': (2, 10),        # Prefer 2-10 years for grad students
            'phd': (5, 20),             # Prefer 5-20 years for PhD
            'postdoc': (8, 30)          # Prefer 8+ years for postdocs
        }
        
        min_exp, max_exp = level_experience_map.get(student_level, (0, 100))
        
        if min_exp <= expert_years <= max_exp:
            return 1.0
        elif expert_years < min_exp:
            return 0.7  # Less experienced but still valuable
        else:
            return 0.9  # Very experienced (always good)
    
    def calculate_field_alignment(self, student: Dict, expert: Dict) -> float:
        """Calculate field of study alignment"""
        student_field = student.get('profile', {}).get('field_of_study', '').lower()
        expert_field = expert.get('profile', {}).get('field_of_study', '').lower()
        
        if not student_field or not expert_field:
            return 0.5
        
        # Exact match
        if student_field == expert_field:
            return 1.0
        
        # Partial match
        if student_field in expert_field or expert_field in student_field:
            return 0.8
        
        # Related fields (simplified)
        related_fields = {
            'computer science': ['software engineering', 'data science', 'ai', 'machine learning'],
            'mathematics': ['statistics', 'data science', 'physics'],
            'physics': ['engineering', 'mathematics'],
            'biology': ['chemistry', 'biotechnology', 'medicine'],
            'chemistry': ['biology', 'biochemistry'],
            'business': ['economics', 'finance', 'marketing'],
        }
        
        for field, related in related_fields.items():
            if field in student_field and any(r in expert_field for r in related):
                return 0.6
            if field in expert_field and any(r in student_field for r in related):
                return 0.6
        
        return 0.3
    
    def find_matches(self, student: Dict, top_k: int = 10) -> List[Dict]:
        """
        Find top-k expert matches for a student
        
        Returns:
            List of dicts with expert info and match scores
        """
        if not self.is_trained:
            logger.warning("Model not trained. Call train() first.")
            return []
        
        try:
            # Prepare student profile
            student_text = self.prepare_student_profile_text(student)
            student_vector = self.tfidf_vectorizer.transform([student_text])
            
            # Calculate TF-IDF cosine similarity
            text_similarities = cosine_similarity(student_vector, self.expert_vectors)[0]
            
            # Calculate comprehensive match scores
            matches = []
            for idx, expert in enumerate(self.expert_profiles):
                # Multi-factor scoring
                text_score = text_similarities[idx]
                interest_score = self.calculate_interest_overlap_score(student, expert)
                experience_score = self.calculate_experience_compatibility(student, expert)
                field_score = self.calculate_field_alignment(student, expert)
                
                # Weighted combination
                final_score = (
                    0.40 * interest_score +      # 40% - Interest overlap (most important)
                    0.30 * text_score +           # 30% - Text similarity
                    0.20 * field_score +          # 20% - Field alignment
                    0.10 * experience_score       # 10% - Experience compatibility
                )
                
                matches.append({
                    'expert_id': str(expert.get('_id', expert.get('id'))),
                    'expert_name': expert.get('full_name', 'Unknown'),
                    'expert_role': expert.get('role', 'expert'),
                    'job_title': expert.get('job_title', ''),
                    'company': expert.get('company', ''),
                    'expertise_areas': expert.get('expertise_areas', []),
                    'years_experience': expert.get('years_experience', 0),
                    'match_score': float(final_score),
                    'score_breakdown': {
                        'interest_overlap': float(interest_score),
                        'text_similarity': float(text_score),
                        'field_alignment': float(field_score),
                        'experience_compatibility': float(experience_score)
                    },
                    'matched_interests': list(
                        set(student.get('skills', {}).get('interests', [])) & 
                        set(expert.get('expertise_areas', []))
                    )
                })
            
            # Sort by match score and return top-k
            matches.sort(key=lambda x: x['match_score'], reverse=True)
            return matches[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding matches: {e}")
            return []
    
    def explain_match(self, student: Dict, expert: Dict) -> Dict:
        """Generate detailed explanation for why a match was suggested"""
        interest_score = self.calculate_interest_overlap_score(student, expert)
        field_score = self.calculate_field_alignment(student, expert)
        experience_score = self.calculate_experience_compatibility(student, expert)
        
        student_interests = set(student.get('skills', {}).get('interests', []))
        expert_expertise = set(expert.get('expertise_areas', []))
        common_interests = student_interests & expert_expertise
        
        explanation = {
            'match_quality': 'Excellent' if interest_score > 0.7 else 'Good' if interest_score > 0.4 else 'Fair',
            'common_interests': list(common_interests),
            'expert_strengths': expert.get('expertise_areas', []),
            'field_compatibility': 'High' if field_score > 0.7 else 'Medium' if field_score > 0.4 else 'Low',
            'experience_level': f"{expert.get('years_experience', 0)} years",
            'recommendation_reason': self._generate_recommendation_text(interest_score, field_score, common_interests)
        }
        
        return explanation
    
    def _generate_recommendation_text(self, interest_score: float, field_score: float, 
                                     common_interests: set) -> str:
        """Generate human-readable recommendation text"""
        if interest_score > 0.7:
            return f"Excellent match! You share {len(common_interests)} key interests with this expert."
        elif interest_score > 0.4:
            return f"Good match based on {len(common_interests)} shared interests and field alignment."
        elif field_score > 0.7:
            return "This expert works in your field and could provide valuable insights."
        else:
            return "This expert has diverse expertise that could broaden your perspective."


# Global instance
expert_matching_model = ExpertMatchingModel()
