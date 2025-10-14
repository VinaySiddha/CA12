"""
Create demo expert/professional users with proper interests and expertise
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_demo_experts():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.matchmaking_db
    users_collection = db.users
    
    # Demo expert users with expertise areas and interests
    demo_experts = [
        {
            "email": "john.expert@example.com",
            "username": "john_expert",
            "full_name": "Dr. John Smith",
            "hashed_password": pwd_context.hash("expert123"),
            "role": "expert",
            "is_active": True,
            "is_verified": True,
            "expertise_areas": ["Machine Learning", "Artificial Intelligence", "Python", "Data Science"],
            "years_experience": 10,
            "company": "Tech Corp",
            "job_title": "Senior ML Engineer",
            "linkedin_url": "https://linkedin.com/in/johnsmith",
            "profile": {
                "bio": "ML expert with 10 years of experience in AI and data science",
                "academic_level": "phd",
                "field_of_study": "Computer Science",
                "institution": "MIT",
                "learning_preferences": ["visual", "reading"],
                "availability": {
                    "monday": ["18:00-20:00"],
                    "wednesday": ["18:00-20:00"],
                    "friday": ["18:00-20:00"]
                },
                "timezone": "UTC",
                "languages": ["English"]
            },
            "skills": {
                "strengths": ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
                "weaknesses": [],
                "interests": ["AI", "Neural Networks", "Computer Vision", "NLP"],
                "expertise_level": {
                    "python": 9,
                    "machine_learning": 9,
                    "deep_learning": 8,
                    "data_science": 9
                }
            },
            "points": 500,
            "level": 5,
            "badges": ["Expert Mentor", "AI Master"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "email": "sarah.pro@example.com",
            "username": "sarah_professional",
            "full_name": "Sarah Johnson",
            "hashed_password": pwd_context.hash("expert123"),
            "role": "professional",
            "is_active": True,
            "is_verified": True,
            "expertise_areas": ["Web Development", "React", "Node.js", "JavaScript", "Full Stack"],
            "years_experience": 7,
            "company": "StartupHub",
            "job_title": "Lead Full Stack Developer",
            "linkedin_url": "https://linkedin.com/in/sarahjohnson",
            "portfolio_url": "https://sarahj.dev",
            "profile": {
                "bio": "Full stack developer passionate about modern web technologies",
                "academic_level": "graduate",
                "field_of_study": "Software Engineering",
                "institution": "Stanford University",
                "learning_preferences": ["kinesthetic", "visual"],
                "availability": {
                    "tuesday": ["19:00-21:00"],
                    "thursday": ["19:00-21:00"],
                    "saturday": ["10:00-12:00"]
                },
                "timezone": "UTC",
                "languages": ["English", "Spanish"]
            },
            "skills": {
                "strengths": ["React", "Node.js", "MongoDB", "Express", "TypeScript"],
                "weaknesses": [],
                "interests": ["Web Development", "Cloud Computing", "DevOps", "Microservices"],
                "expertise_level": {
                    "javascript": 9,
                    "react": 9,
                    "nodejs": 8,
                    "databases": 7
                }
            },
            "points": 450,
            "level": 4,
            "badges": ["Web Wizard", "Code Mentor"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "email": "michael.data@example.com",
            "username": "michael_data",
            "full_name": "Michael Chen",
            "hashed_password": pwd_context.hash("expert123"),
            "role": "expert",
            "is_active": True,
            "is_verified": True,
            "expertise_areas": ["Data Analysis", "Statistics", "Python", "Data Visualization", "SQL"],
            "years_experience": 5,
            "company": "Data Insights Inc",
            "job_title": "Data Scientist",
            "linkedin_url": "https://linkedin.com/in/michaelchen",
            "profile": {
                "bio": "Data scientist specializing in statistical analysis and visualization",
                "academic_level": "graduate",
                "field_of_study": "Statistics",
                "institution": "UC Berkeley",
                "learning_preferences": ["visual", "reading"],
                "availability": {
                    "monday": ["17:00-19:00"],
                    "wednesday": ["17:00-19:00"],
                    "friday": ["17:00-19:00"]
                },
                "timezone": "UTC",
                "languages": ["English", "Mandarin"]
            },
            "skills": {
                "strengths": ["Python", "Pandas", "Matplotlib", "SQL", "Statistics"],
                "weaknesses": [],
                "interests": ["Data Science", "Machine Learning", "Business Intelligence", "Analytics"],
                "expertise_level": {
                    "python": 8,
                    "statistics": 9,
                    "data_analysis": 9,
                    "sql": 8
                }
            },
            "points": 380,
            "level": 4,
            "badges": ["Data Expert", "Statistics Master"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "email": "emily.ux@example.com",
            "username": "emily_ux",
            "full_name": "Emily Rodriguez",
            "hashed_password": pwd_context.hash("expert123"),
            "role": "professional",
            "is_active": True,
            "is_verified": True,
            "expertise_areas": ["UX Design", "UI Design", "Figma", "User Research", "Prototyping"],
            "years_experience": 6,
            "company": "Design Studio Pro",
            "job_title": "Senior UX Designer",
            "linkedin_url": "https://linkedin.com/in/emilyrodriguez",
            "portfolio_url": "https://emilyux.design",
            "profile": {
                "bio": "UX designer focused on creating intuitive and beautiful user experiences",
                "academic_level": "graduate",
                "field_of_study": "Human-Computer Interaction",
                "institution": "Carnegie Mellon",
                "learning_preferences": ["visual", "kinesthetic"],
                "availability": {
                    "tuesday": ["18:00-20:00"],
                    "thursday": ["18:00-20:00"],
                    "sunday": ["14:00-16:00"]
                },
                "timezone": "UTC",
                "languages": ["English"]
            },
            "skills": {
                "strengths": ["Figma", "Adobe XD", "User Research", "Wireframing", "Prototyping"],
                "weaknesses": [],
                "interests": ["UX Design", "UI Design", "Product Design", "Design Systems"],
                "expertise_level": {
                    "ux_design": 9,
                    "ui_design": 8,
                    "figma": 9,
                    "user_research": 8
                }
            },
            "points": 420,
            "level": 4,
            "badges": ["Design Master", "UX Champion"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "email": "david.cloud@example.com",
            "username": "david_cloud",
            "full_name": "David Williams",
            "hashed_password": pwd_context.hash("expert123"),
            "role": "expert",
            "is_active": True,
            "is_verified": True,
            "expertise_areas": ["Cloud Computing", "AWS", "DevOps", "Docker", "Kubernetes"],
            "years_experience": 8,
            "company": "CloudTech Solutions",
            "job_title": "Cloud Architect",
            "linkedin_url": "https://linkedin.com/in/davidwilliams",
            "profile": {
                "bio": "Cloud architect specializing in AWS and DevOps practices",
                "academic_level": "graduate",
                "field_of_study": "Computer Science",
                "institution": "Georgia Tech",
                "learning_preferences": ["kinesthetic", "reading"],
                "availability": {
                    "monday": ["19:00-21:00"],
                    "thursday": ["19:00-21:00"],
                    "saturday": ["15:00-17:00"]
                },
                "timezone": "UTC",
                "languages": ["English"]
            },
            "skills": {
                "strengths": ["AWS", "Docker", "Kubernetes", "Terraform", "CI/CD"],
                "weaknesses": [],
                "interests": ["Cloud Computing", "DevOps", "Infrastructure", "Automation"],
                "expertise_level": {
                    "aws": 9,
                    "devops": 8,
                    "docker": 9,
                    "kubernetes": 8
                }
            },
            "points": 490,
            "level": 5,
            "badges": ["Cloud Expert", "DevOps Master"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Insert demo experts
    for expert in demo_experts:
        existing = await users_collection.find_one({"email": expert["email"]})
        if existing:
            print(f"Expert {expert['email']} already exists, updating...")
            await users_collection.update_one(
                {"email": expert["email"]},
                {"$set": expert}
            )
        else:
            result = await users_collection.insert_one(expert)
            print(f"Created expert: {expert['full_name']} ({expert['email']})")
    
    print(f"\n✅ Demo experts setup complete!")
    print(f"Total experts created/updated: {len(demo_experts)}")
    print("\nDemo Expert Credentials:")
    print("1. john.expert@example.com / expert123 - ML Expert")
    print("2. sarah.pro@example.com / expert123 - Full Stack Developer")
    print("3. michael.data@example.com / expert123 - Data Scientist")
    print("4. emily.ux@example.com / expert123 - UX Designer")
    print("5. david.cloud@example.com / expert123 - Cloud Architect")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_demo_experts())
