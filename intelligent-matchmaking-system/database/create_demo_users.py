"""
Script to create demo users with proper password hashing
Run this to set up demo users for testing the application
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "intelligent_matchmaking"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Demo users data
DEMO_USERS = [
    {
        "email": "student@example.com",
        "username": "student_demo",
        "full_name": "Demo Student",
        "password": "student123",
        "role": "student",
        "is_active": True,
        "profile": {
            "bio": "Computer science student interested in AI and web development",
            "academic_level": "undergraduate",
            "field_of_study": "Computer Science",
            "institution": "State University",
            "learning_preferences": ["visual", "kinesthetic"],
            "availability": {
                "monday": ["14:00-16:00"],
                "wednesday": ["14:00-16:00"],
                "friday": ["14:00-16:00"]
            },
            "timezone": "UTC",
            "languages": ["English"]
        },
        "skills": {
            "strengths": ["JavaScript", "HTML", "CSS"],
            "weaknesses": ["Machine Learning", "Data Science", "Cloud Computing"],
            "interests": ["Machine Learning", "Web Development", "Python", "React", "Data Science"],
            "expertise_level": {
                "javascript": 6,
                "html": 7,
                "css": 7,
                "python": 5
            }
        },
        "points": 100,
        "level": 2,
        "badges": []
    },
    {
        "email": "teacher@example.com",
        "username": "teacher_demo",
        "full_name": "Demo Teacher",
        "password": "teacher123",
        "role": "teacher",
        "teaching_subjects": ["Computer Science", "Mathematics"],
        "years_experience": 5,
        "is_active": True,
    },
    {
        "email": "admin@example.com",
        "username": "admin_demo",
        "full_name": "Demo Admin",
        "password": "admin123",
        "role": "admin",
        "is_active": True,
    }
]


async def create_demo_users():
    """Create demo users in the database"""
    print("🔧 Creating demo users...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db.users
    
    created_count = 0
    updated_count = 0
    
    for user_data in DEMO_USERS:
        email = user_data["email"]
        password = user_data.pop("password")
        
        # Hash the password
        hashed_password = pwd_context.hash(password)
        
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": email})
        
        if existing_user:
            # Update existing user
            result = await users_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        **user_data,
                        "hashed_password": hashed_password,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ Updated user: {email}")
            else:
                print(f"ℹ️  User already up to date: {email}")
        else:
            # Create new user
            user_doc = {
                **user_data,
                "hashed_password": hashed_password,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await users_collection.insert_one(user_doc)
            if result.inserted_id:
                created_count += 1
                print(f"✅ Created user: {email}")
            else:
                print(f"❌ Failed to create user: {email}")
    
    print(f"\n🎉 Demo users setup complete!")
    print(f"   Created: {created_count} users")
    print(f"   Updated: {updated_count} users")
    print("\n📋 Demo Login Credentials:")
    print("=" * 50)
    print("Student Account:")
    print("  Email: student@example.com")
    print("  Password: student123")
    print("\nTeacher Account:")
    print("  Email: teacher@example.com")
    print("  Password: teacher123")
    print("\nAdmin Account:")
    print("  Email: admin@example.com")
    print("  Password: admin123")
    print("=" * 50)
    
    # Close connection
    client.close()


if __name__ == "__main__":
    asyncio.run(create_demo_users())
