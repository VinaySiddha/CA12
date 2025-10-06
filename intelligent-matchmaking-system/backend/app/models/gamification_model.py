"""
Gamification data models
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from .user_model import PyObjectId



class Badge(BaseModel):
    id: str
    name: str
    description: str
    icon_url: Optional[str] = None
    criteria: Dict  # Requirements to earn the badge
    points_value: int = 0
    rarity: str = "common"  # "common", "rare", "epic", "legendary"


class Achievement(BaseModel):
    user_id: PyObjectId
    badge_id: str
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    progress: Dict = {}  # Track progress towards badge


class Leaderboard(BaseModel):
    user_id: PyObjectId
    username: str
    total_points: int
    level: int
    rank: int
    category: str = "overall"  # "overall", "weekly", "monthly", "topic_specific"
    period: str  # "all_time", "2024-10", etc.


class UserStats(BaseModel):
    user_id: PyObjectId
    
    # Learning statistics
    total_study_sessions: int = 0
    total_study_hours: int = 0
    topics_mastered: List[str] = []
    current_streak: int = 0  # days
    longest_streak: int = 0
    
    # Mentoring statistics
    sessions_as_mentor: int = 0
    sessions_as_mentee: int = 0
    mentees_helped: int = 0
    average_rating_as_mentor: float = 0.0
    
    # Engagement statistics
    logins_this_month: int = 0
    feedback_given: int = 0
    study_groups_joined: int = 0
    study_groups_created: int = 0
    
    # Last updated
    last_calculated: datetime = Field(default_factory=datetime.utcnow)


class GamificationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    
    # Current status
    total_points: int = 0
    level: int = 1
    experience_points: int = 0
    points_to_next_level: int = 100
    
    # Badges and achievements
    badges_earned: List[str] = []
    achievements: List[Achievement] = []
    
    # Statistics
    stats: UserStats
    
    # Preferences
    notifications_enabled: bool = True
    public_profile: bool = True
    show_on_leaderboard: bool = True
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


# Predefined badges
AVAILABLE_BADGES = {
    "first_session": Badge(
        id="first_session",
        name="Getting Started",
        description="Complete your first study session",
        criteria={"sessions_completed": 1},
        points_value=50,
        rarity="common"
    ),
    "helpful_mentor": Badge(
        id="helpful_mentor",
        name="Helpful Mentor",
        description="Receive 10 positive ratings as a mentor",
        criteria={"positive_mentor_ratings": 10},
        points_value=200,
        rarity="rare"
    ),
    "knowledge_seeker": Badge(
        id="knowledge_seeker",
        name="Knowledge Seeker",
        description="Complete 25 study sessions as a mentee",
        criteria={"mentee_sessions": 25},
        points_value=300,
        rarity="rare"
    ),
    "streak_master": Badge(
        id="streak_master",
        name="Streak Master",
        description="Maintain a 30-day study streak",
        criteria={"study_streak": 30},
        points_value=500,
        rarity="epic"
    ),
    "topic_master": Badge(
        id="topic_master",
        name="Topic Master",
        description="Master 5 different topics",
        criteria={"topics_mastered": 5},
        points_value=400,
        rarity="epic"
    ),
    "community_builder": Badge(
        id="community_builder",
        name="Community Builder",
        description="Create 3 successful study groups",
        criteria={"study_groups_created": 3},
        points_value=350,
        rarity="rare"
    )
}