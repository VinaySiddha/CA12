"""
Generate realistic users for the intelligent matchmaking system
This script creates 10 student users and 10 teacher users with diverse profiles
"""
import asyncio
import random
import sys
import os
from datetime import datetime, timedelta
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Database settings
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "intelligent_matchmaking"


# Realistic data for user generation
STUDENT_NAMES = [
    {"full_name": "Arjun Patel", "username": "arjun_patel", "email": "arjun.patel@student.edu"},
    {"full_name": "Priya Sharma", "username": "priya_sharma", "email": "priya.sharma@student.edu"},
    {"full_name": "Rahul Kumar", "username": "rahul_kumar", "email": "rahul.kumar@student.edu"},
    {"full_name": "Ananya Singh", "username": "ananya_singh", "email": "ananya.singh@student.edu"},
    {"full_name": "Vikram Gupta", "username": "vikram_gupta", "email": "vikram.gupta@student.edu"},
    {"full_name": "Sneha Reddy", "username": "sneha_reddy", "email": "sneha.reddy@student.edu"},
    {"full_name": "Karthik Nair", "username": "karthik_nair", "email": "karthik.nair@student.edu"},
    {"full_name": "Meera Joshi", "username": "meera_joshi", "email": "meera.joshi@student.edu"},
    {"full_name": "Aditya Verma", "username": "aditya_verma", "email": "aditya.verma@student.edu"},
    {"full_name": "Ishita Bhatt", "username": "ishita_bhatt", "email": "ishita.bhatt@student.edu"}
]

TEACHER_NAMES = [
    {"full_name": "Dr. Rajesh Khanna", "username": "dr_rajesh_khanna", "email": "rajesh.khanna@university.edu"},
    {"full_name": "Prof. Kavita Desai", "username": "prof_kavita_desai", "email": "kavita.desai@university.edu"},
    {"full_name": "Dr. Suresh Iyer", "username": "dr_suresh_iyer", "email": "suresh.iyer@university.edu"},
    {"full_name": "Prof. Neha Agarwal", "username": "prof_neha_agarwal", "email": "neha.agarwal@university.edu"},
    {"full_name": "Dr. Amit Mehta", "username": "dr_amit_mehta", "email": "amit.mehta@university.edu"},
    {"full_name": "Prof. Sunita Rao", "username": "prof_sunita_rao", "email": "sunita.rao@university.edu"},
    {"full_name": "Dr. Manish Jindal", "username": "dr_manish_jindal", "email": "manish.jindal@university.edu"},
    {"full_name": "Prof. Deepika Sinha", "username": "prof_deepika_sinha", "email": "deepika.sinha@university.edu"},
    {"full_name": "Dr. Vivek Chopra", "username": "dr_vivek_chopra", "email": "vivek.chopra@university.edu"},
    {"full_name": "Prof. Ritu Malhotra", "username": "prof_ritu_malhotra", "email": "ritu.malhotra@university.edu"}
]

SUBJECTS = [
    "Computer Science", "Data Science", "Machine Learning", "Artificial Intelligence",
    "Software Engineering", "Web Development", "Mobile Development", "Cybersecurity",
    "Mathematics", "Statistics", "Physics", "Electronics", "Mechanical Engineering",
    "Business Administration", "Economics", "Finance", "Marketing", "Management"
]

INTERESTS_POOL = [
    "Programming", "Machine Learning", "Data Analysis", "Web Development", "Mobile Apps",
    "Artificial Intelligence", "Blockchain", "Cybersecurity", "Cloud Computing", "DevOps",
    "UI/UX Design", "Database Design", "Algorithm Design", "System Architecture",
    "Research", "Innovation", "Entrepreneurship", "Startups", "Technology Trends",
    "Open Source", "Game Development", "Robotics", "IoT", "Big Data", "Analytics"
]

SKILLS_POOL = [
    "Python", "Java", "JavaScript", "C++", "React", "Node.js", "MongoDB", "SQL",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy",
    "Git", "Docker", "Kubernetes", "AWS", "Azure", "Linux", "Agile", "Scrum",
    "Project Management", "Leadership", "Communication", "Problem Solving", "Critical Thinking"
]

LEARNING_STYLES = ["Visual", "Auditory", "Kinesthetic", "Reading/Writing", "Multimodal"]

EDUCATIONAL_LEVELS = ["Bachelor's", "Master's", "PhD", "Diploma", "Certificate"]

INSTITUTIONS = [
    "Indian Institute of Technology", "Indian Institute of Science", "National Institute of Technology",
    "Delhi University", "Mumbai University", "Bangalore University", "Chennai University",
    "Pune University", "Hyderabad University", "Kolkata University"
]

BIO_TEMPLATES = {
    "student": [
        "Passionate {field_of_study} student with keen interest in {interest1} and {interest2}. Always eager to learn new technologies and work on innovative projects.",
        "Final year {field_of_study} student specializing in {interest1}. Love to explore {interest2} and contribute to open-source projects in my free time.",
        "Dedicated {field_of_study} student with strong foundation in {interest1}. Currently working on projects related to {interest2} and seeking mentorship opportunities.",
        "Enthusiastic learner pursuing {field_of_study} with focus on {interest1} and {interest2}. Believe in continuous learning and practical application of knowledge.",
        "Motivated {field_of_study} student passionate about {interest1}. Enjoy collaborating on {interest2} projects and participating in hackathons."
    ],
    "teacher": [
        "Experienced {field_of_study} professor with {years} years of teaching and research experience. Specialized in {interest1} and {interest2}. Passionate about mentoring students.",
        "Associate Professor at {institution} with expertise in {field_of_study}. Research focus on {interest1} and {interest2}. Published numerous papers in top-tier conferences.",
        "Senior faculty member specializing in {field_of_study} with strong background in {interest1}. Actively involved in industry collaborations and student guidance.",
        "Professor with {years} years of academic experience in {field_of_study}. Areas of expertise include {interest1} and {interest2}. Committed to innovative teaching methods.",
        "Distinguished educator and researcher in {field_of_study}. Expert in {interest1} and {interest2}. Mentored over 100 students in various projects and research work."
    ]
}


def generate_student_profile(student_data):
    """Generate a realistic student profile"""
    interests = random.sample(INTERESTS_POOL, random.randint(3, 7))
    skills = random.sample(SKILLS_POOL, random.randint(4, 8))
    field_of_study = random.choice(SUBJECTS)
    
    bio_template = random.choice(BIO_TEMPLATES["student"])
    bio = bio_template.format(
        field_of_study=field_of_study,
        interest1=interests[0] if interests else "technology",
        interest2=interests[1] if len(interests) > 1 else "innovation"
    )
    
    return {
        "username": student_data["username"],
        "email": student_data["email"],
        "full_name": student_data["full_name"],
        "hashed_password": get_password_hash("student123"),
        "role": "student",
        "is_active": True,
        "is_verified": True,
        "bio": bio,
        "field_of_study": field_of_study,
        "educational_level": random.choice(EDUCATIONAL_LEVELS[:3]),  # Students: Bachelor's, Master's, PhD
        "institution": random.choice(INSTITUTIONS),
        "year_of_study": random.randint(1, 4),
        "gpa": round(random.uniform(7.0, 9.5), 2),
        "interests": interests,
        "skills": {
            "technical_skills": [skill for skill in skills if skill in ["Python", "Java", "JavaScript", "C++", "React", "Node.js", "MongoDB", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Git", "Docker", "Kubernetes", "AWS", "Azure", "Linux"]],
            "soft_skills": [skill for skill in skills if skill in ["Project Management", "Leadership", "Communication", "Problem Solving", "Critical Thinking"]],
            "interests": interests[:3]  # Top 3 interests
        },
        "learning_style": random.choice(LEARNING_STYLES),
        "goals": [
            f"Master {interests[0] if interests else 'programming'}",
            f"Get internship in {field_of_study.lower()} field",
            "Build portfolio of real-world projects",
            "Network with industry professionals"
        ],
        "availability": {
            "preferred_days": random.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], random.randint(3, 5)),
            "preferred_times": random.choice([["Morning", "Afternoon"], ["Afternoon", "Evening"], ["Evening"], ["Morning"]]),
            "timezone": "Asia/Kolkata"
        },
        "profile": {
            "bio": bio,
            "field_of_study": field_of_study,
            "academic_level": random.choice(EDUCATIONAL_LEVELS[:3]),
            "institution": random.choice(INSTITUTIONS),
            "learning_preferences": [random.choice(LEARNING_STYLES)],
            "career_goals": [f"Expert in {interests[0] if interests else 'technology'}", "Industry leadership role"],
            "current_projects": [f"{interests[0] if interests else 'Web'} application development", f"{interests[1] if len(interests) > 1 else 'Mobile'} project"],
            "achievements": ["Dean's List", "Hackathon winner", "Research paper published"] if random.random() > 0.5 else ["Academic excellence award", "Project competition finalist"]
        },
        "points": random.randint(50, 500),
        "level": random.randint(1, 5),
        "badges": random.sample(["Early Bird", "Active Learner", "Team Player", "Quick Responder", "Mentor", "Explorer"], random.randint(1, 3)),
        "created_at": datetime.utcnow() - timedelta(days=random.randint(30, 365)),
        "updated_at": datetime.utcnow() - timedelta(days=random.randint(1, 30))
    }


def generate_teacher_profile(teacher_data):
    """Generate a realistic teacher profile"""
    interests = random.sample(INTERESTS_POOL, random.randint(4, 8))
    skills = random.sample(SKILLS_POOL, random.randint(6, 12))
    field_of_study = random.choice(SUBJECTS)
    years_experience = random.randint(5, 25)
    
    bio_template = random.choice(BIO_TEMPLATES["teacher"])
    bio = bio_template.format(
        field_of_study=field_of_study,
        years=years_experience,
        institution=random.choice(INSTITUTIONS),
        interest1=interests[0] if interests else "technology",
        interest2=interests[1] if len(interests) > 1 else "innovation"
    )
    
    return {
        "username": teacher_data["username"],
        "email": teacher_data["email"],
        "full_name": teacher_data["full_name"],
        "hashed_password": get_password_hash("teacher123"),
        "role": "teacher",
        "is_active": True,
        "is_verified": True,
        "bio": bio,
        "field_of_study": field_of_study,
        "educational_level": "PhD",
        "institution": random.choice(INSTITUTIONS),
        "department": field_of_study,
        "designation": random.choice(["Assistant Professor", "Associate Professor", "Professor", "Senior Professor"]),
        "years_of_experience": years_experience,
        "research_areas": interests[:3],
        "interests": interests,
        "skills": {
            "technical_skills": [skill for skill in skills if skill in ["Python", "Java", "JavaScript", "C++", "React", "Node.js", "MongoDB", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Git", "Docker", "Kubernetes", "AWS", "Azure", "Linux"]],
            "soft_skills": [skill for skill in skills if skill in ["Project Management", "Leadership", "Communication", "Problem Solving", "Critical Thinking"]],
            "research_skills": ["Research Methodology", "Data Analysis", "Academic Writing", "Grant Writing"],
            "teaching_specializations": interests[:4]
        },
        "teaching_preference": random.choice(LEARNING_STYLES),
        "availability": {
            "preferred_days": random.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], random.randint(3, 5)),
            "preferred_times": random.choice([["Morning", "Afternoon"], ["Afternoon", "Evening"], ["Morning", "Evening"]]),
            "timezone": "Asia/Kolkata",
            "max_students_per_session": random.randint(5, 20),
            "session_duration": random.choice([30, 45, 60, 90])
        },
        "profile": {
            "bio": bio,
            "field_of_study": field_of_study,
            "academic_level": "PhD",
            "institution": random.choice(INSTITUTIONS),
            "research_areas": interests[:3],
            "publications": random.randint(10, 50),
            "h_index": random.randint(5, 30),
            "courses_taught": [f"Advanced {field_of_study}", f"Introduction to {interests[0] if interests else 'Programming'}", f"{interests[1] if len(interests) > 1 else 'Data'} Structures"],
            "achievements": ["Best Teacher Award", "Research Excellence Award", "Innovation in Teaching"] if random.random() > 0.3 else ["Outstanding Faculty", "Student Choice Award"]
        },
        "rating": round(random.uniform(4.0, 5.0), 1),
        "total_sessions": random.randint(20, 200),
        "total_students_mentored": random.randint(50, 500),
        "points": random.randint(200, 1000),
        "level": random.randint(3, 10),
        "badges": random.sample(["Expert Mentor", "Research Leader", "Innovation Champion", "Student Favorite", "Industry Connect", "Knowledge Sharer"], random.randint(2, 4)),
        "created_at": datetime.utcnow() - timedelta(days=random.randint(180, 1095)),  # 6 months to 3 years
        "updated_at": datetime.utcnow() - timedelta(days=random.randint(1, 15))
    }


async def create_realistic_users():
    """Create realistic student and teacher users in the database"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print("🚀 Starting to create realistic users...")
    
    # Clear existing users (optional - comment out if you want to keep existing users)
    # await db.users.delete_many({"role": {"$in": ["student", "teacher"]}})
    
    created_students = []
    created_teachers = []
    
    # Create students
    print("\n👨‍🎓 Creating student users...")
    for i, student_data in enumerate(STUDENT_NAMES):
        try:
            # Check if user already exists
            existing_user = await db.users.find_one({"email": student_data["email"]})
            if existing_user:
                print(f"   ⚠️  Student {student_data['full_name']} already exists, skipping...")
                continue
            
            student_profile = generate_student_profile(student_data)
            result = await db.users.insert_one(student_profile)
            created_students.append(result.inserted_id)
            print(f"   ✅ Created student {i+1}/10: {student_data['full_name']}")
            print(f"      📧 Email: {student_data['email']}")
            print(f"      🎯 Field: {student_profile['field_of_study']}")
            print(f"      💡 Top interests: {', '.join(student_profile['interests'][:3])}")
            
        except Exception as e:
            print(f"   ❌ Error creating student {student_data['full_name']}: {str(e)}")
    
    # Create teachers
    print("\n👩‍🏫 Creating teacher users...")
    for i, teacher_data in enumerate(TEACHER_NAMES):
        try:
            # Check if user already exists
            existing_user = await db.users.find_one({"email": teacher_data["email"]})
            if existing_user:
                print(f"   ⚠️  Teacher {teacher_data['full_name']} already exists, skipping...")
                continue
            
            teacher_profile = generate_teacher_profile(teacher_data)
            result = await db.users.insert_one(teacher_profile)
            created_teachers.append(result.inserted_id)
            print(f"   ✅ Created teacher {i+1}/10: {teacher_data['full_name']}")
            print(f"      📧 Email: {teacher_data['email']}")
            print(f"      🎯 Field: {teacher_profile['field_of_study']}")
            print(f"      🔬 Research areas: {', '.join(teacher_profile['research_areas'])}")
            print(f"      📚 Experience: {teacher_profile['years_of_experience']} years")
            
        except Exception as e:
            print(f"   ❌ Error creating teacher {teacher_data['full_name']}: {str(e)}")
    
    # Create some sample meetings
    if created_teachers:
        print("\n📅 Creating sample meetings...")
        for i, teacher_id in enumerate(created_teachers[:5]):  # Create 5 sample meetings
            try:
                teacher = await db.users.find_one({"_id": teacher_id})
                if not teacher:
                    continue
                
                meeting_topics = [
                    "Introduction to Machine Learning Fundamentals",
                    "Advanced Web Development Techniques",
                    "Data Structures and Algorithms Workshop",
                    "Career Guidance in Technology",
                    "Research Methodology and Academic Writing"
                ]
                
                meeting_doc = {
                    "title": meeting_topics[i],
                    "description": f"Join {teacher['full_name']} for an interactive session on {meeting_topics[i].lower()}. Perfect for students looking to enhance their knowledge and skills.",
                    "teacher_id": teacher_id,
                    "teacher_name": teacher['full_name'],
                    "teacher_email": teacher['email'],
                    "subject": teacher['field_of_study'],
                    "category": "workshop",
                    "scheduled_date": datetime.utcnow() + timedelta(days=random.randint(7, 30)),
                    "duration_minutes": random.choice([60, 90, 120]),
                    "timezone": "Asia/Kolkata",
                    "meeting_platform": "google_meet",
                    "meeting_link": f"https://meet.google.com/abc-{random.randint(1000, 9999)}-xyz",
                    "max_participants": random.randint(20, 50),
                    "registered_students": random.sample(created_students, min(random.randint(5, 15), len(created_students))),
                    "attendees": [],
                    "is_recurring": False,
                    "recurrence_pattern": None,
                    "is_recorded": random.choice([True, False]),
                    "recording_url": None,
                    "status": "scheduled",
                    "is_active": True,
                    "is_public": True,
                    "prerequisites": random.sample(["Basic programming knowledge", "Mathematics background", "Interest in technology", "No prerequisites"], random.randint(0, 2)),
                    "materials_needed": ["Notebook", "Laptop", "Stable internet connection"],
                    "agenda": [
                        "Introduction and overview",
                        "Core concepts explanation",
                        "Practical examples",
                        "Q&A session",
                        "Next steps and resources"
                    ],
                    "tags": random.sample(teacher['interests'], min(3, len(teacher['interests']))),
                    "difficulty_level": random.choice(["beginner", "intermediate", "advanced"]),
                    "likes": random.sample(created_students, random.randint(2, 8)),
                    "rating": 0.0,
                    "feedback_count": 0,
                    "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 10)),
                    "updated_at": datetime.utcnow() - timedelta(days=random.randint(0, 5)),
                    "discussion_group_id": None
                }
                
                result = await db.meetings.insert_one(meeting_doc)
                print(f"   ✅ Created meeting: {meeting_topics[i]}")
                print(f"      👨‍🏫 By: {teacher['full_name']}")
                print(f"      📅 Scheduled: {meeting_doc['scheduled_date'].strftime('%Y-%m-%d %H:%M')}")
                
            except Exception as e:
                print(f"   ❌ Error creating meeting: {str(e)}")
    
    print(f"\n🎉 User creation completed!")
    print(f"   📊 Students created: {len(created_students)}")
    print(f"   📊 Teachers created: {len(created_teachers)}")
    
    print(f"\n🔑 Default passwords:")
    print(f"   👨‍🎓 Students: 'student123'")
    print(f"   👩‍🏫 Teachers: 'teacher123'")
    
    print(f"\n📧 Sample login credentials:")
    if len(created_students) > 0:
        print(f"   Student: {STUDENT_NAMES[0]['email']} / student123")
    if len(created_teachers) > 0:
        print(f"   Teacher: {TEACHER_NAMES[0]['email']} / teacher123")
    
    # Close database connection
    client.close()


if __name__ == "__main__":
    asyncio.run(create_realistic_users())