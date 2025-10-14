#!/usr/bin/env python3
"""
Script to populate the database with initial user data for testing the ML recommendation model
"""
import sys
import os
import asyncio
import json
import random
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from passlib.context import CryptContext

# Add parent directory to path for importing app modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(ROOT_DIR)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "intelligent_matchmaking"

# User data
USER_ROLES = ["student", "teacher", "mentor", "admin"]
ACADEMIC_LEVELS = ["undergraduate", "graduate", "phd", "postdoc"]
LEARNING_PREFERENCES = ["visual", "auditory", "kinesthetic", "reading"]

TECH_INTERESTS = [
    "Machine Learning", "Web Development", "Mobile Development", "Data Science",
    "Cloud Computing", "Cybersecurity", "Game Development", "IoT",
    "Blockchain", "DevOps", "Natural Language Processing", "Computer Vision",
    "Database Systems", "Distributed Systems", "Network Security", "Quantum Computing",
    "Algorithms", "Data Structures", "Software Architecture", "UI/UX Design"
]

GENERAL_INTERESTS = [
    "Mathematics", "Physics", "Chemistry", "Biology", "Economics", "Psychology",
    "Literature", "History", "Philosophy", "Music", "Art", "Business",
    "Marketing", "Finance", "Entrepreneurship", "Public Speaking"
]

UNIVERSITIES = [
    "MIT", "Stanford", "Harvard", "UC Berkeley", "Georgia Tech", 
    "Carnegie Mellon", "University of Michigan", "Cornell", "Princeton",
    "University of Washington", "University of Toronto", "University of Cambridge",
    "Oxford University", "ETH Zurich", "National University of Singapore"
]

FIELDS_OF_STUDY = [
    "Computer Science", "Data Science", "Information Technology", "Software Engineering",
    "Artificial Intelligence", "Mechanical Engineering", "Electrical Engineering",
    "Physics", "Mathematics", "Economics", "Business Administration",
    "Psychology", "Biology", "Chemistry", "Medicine"
]


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def generate_user():
    """Generate a random user"""
    role = random.choice(USER_ROLES)
    academic_level = random.choice(ACADEMIC_LEVELS)
    learning_preferences = random.sample(LEARNING_PREFERENCES, random.randint(1, 3))
    
    # Generate interests with some bias based on role
    if role == "student":
        interests = random.sample(TECH_INTERESTS, random.randint(3, 8))
    elif role == "teacher":
        interests = random.sample(TECH_INTERESTS, random.randint(2, 5)) + random.sample(GENERAL_INTERESTS, random.randint(1, 3))
    else:
        interests = random.sample(TECH_INTERESTS + GENERAL_INTERESTS, random.randint(3, 10))
    
    # Generate strengths and weaknesses with some overlap
    all_skills = TECH_INTERESTS + GENERAL_INTERESTS
    strengths = random.sample(all_skills, random.randint(3, 8))
    
    # Weaknesses should not include strengths
    weaknesses_pool = [skill for skill in all_skills if skill not in strengths]
    weaknesses = random.sample(weaknesses_pool, random.randint(2, 6))
    
    # Generate profile data
    first_name = f"User{random.randint(100, 999)}"
    last_name = f"Test{random.randint(10, 99)}"
    university = random.choice(UNIVERSITIES)
    field_of_study = random.choice(FIELDS_OF_STUDY)
    
    # Generate more data for teachers
    teaching_subjects = []
    years_experience = 0
    if role == "teacher":
        teaching_subjects = random.sample(TECH_INTERESTS, random.randint(1, 4))
        years_experience = random.randint(1, 15)
    
    # Generate user document
    user = {
        "username": f"{first_name.lower()}.{last_name.lower()}",
        "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
        "hashed_password": get_password_hash("password123"),
        "full_name": f"{first_name} {last_name}",
        "role": role,
        "is_active": True,
        "profile": {
            "bio": f"I am a {role} interested in {', '.join(interests[:2])}",
            "academic_level": academic_level,
            "field_of_study": field_of_study,
            "university": university,
            "learning_preferences": learning_preferences,
        },
        "skills": {
            "interests": interests,
            "strengths": strengths,
            "weaknesses": weaknesses
        },
        "points": random.randint(0, 1000),
        "level": random.randint(1, 10),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Add teacher-specific fields
    if role == "teacher":
        user["profile"]["teaching_subjects"] = teaching_subjects
        user["profile"]["years_experience"] = years_experience
    
    return user


async def populate_database():
    """Populate the database with initial data"""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db["users"]
    
    # Create demo users
    demo_users = [
        {
            "username": "student.demo",
            "email": "student.demo@example.com",
            "hashed_password": get_password_hash("password123"),
            "full_name": "Student Demo",
            "role": "student",
            "is_active": True,
            "profile": {
                "bio": "I'm a computer science student looking to learn and collaborate.",
                "academic_level": "undergraduate",
                "field_of_study": "Computer Science",
                "university": "Demo University",
                "learning_preferences": ["visual", "reading"],
            },
            "skills": {
                "interests": ["Machine Learning", "Web Development", "Algorithms", "Data Structures"],
                "strengths": ["Web Development", "Python", "JavaScript"],
                "weaknesses": ["Machine Learning", "Database Systems", "Computer Vision"]
            },
            "points": 120,
            "level": 2,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "username": "teacher.demo",
            "email": "teacher.demo@example.com",
            "hashed_password": get_password_hash("password123"),
            "full_name": "Teacher Demo",
            "role": "teacher",
            "is_active": True,
            "profile": {
                "bio": "Experienced educator with expertise in computer science and data science.",
                "academic_level": "postdoc",
                "field_of_study": "Computer Science",
                "university": "Demo University",
                "learning_preferences": ["auditory", "kinesthetic"],
                "teaching_subjects": ["Machine Learning", "Data Science", "Python Programming"],
                "years_experience": 8
            },
            "skills": {
                "interests": ["Machine Learning", "Data Science", "AI Ethics", "Education Technology"],
                "strengths": ["Machine Learning", "Python", "Statistics", "Data Analysis"],
                "weaknesses": ["Web Development", "UI/UX Design"]
            },
            "points": 850,
            "level": 8,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "username": "admin.demo",
            "email": "admin.demo@example.com",
            "hashed_password": get_password_hash("password123"),
            "full_name": "Admin Demo",
            "role": "admin",
            "is_active": True,
            "profile": {
                "bio": "System administrator for the intelligent matchmaking platform.",
                "academic_level": "graduate",
                "field_of_study": "Information Technology",
                "university": "Demo University",
                "learning_preferences": ["reading"],
            },
            "skills": {
                "interests": ["System Administration", "Cloud Computing", "Cybersecurity"],
                "strengths": ["System Administration", "Database Management", "Cloud Computing"],
                "weaknesses": ["Mobile Development", "UI/UX Design"]
            },
            "points": 500,
            "level": 5,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Insert demo users
    for user in demo_users:
        existing = users_collection.find_one({"username": user["username"]})
        if not existing:
            users_collection.insert_one(user)
            print(f"Added demo user: {user['username']} ({user['role']})")
        else:
            print(f"Demo user already exists: {user['username']}")
    
    # Generate and insert random users
    num_users = 50  # Number of random users to generate
    random_users = [generate_user() for _ in range(num_users)]
    
    for user in random_users:
        existing = users_collection.find_one({"username": user["username"]})
        if not existing:
            users_collection.insert_one(user)
            print(f"Added random user: {user['username']} ({user['role']})")
        else:
            print(f"Random user already exists: {user['username']}")
    
    print(f"Added {len(demo_users)} demo users and {len(random_users)} random users")


if __name__ == "__main__":
    asyncio.run(populate_database())