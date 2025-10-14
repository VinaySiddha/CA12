"""
Create MongoDB indexes for production performance optimization
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "intelligent_matchmaking"


async def create_indexes():
    """Create all necessary indexes for optimal performance"""
    print("🔧 Creating MongoDB indexes for production...")
    print("=" * 60)
    
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    # Users Collection Indexes
    print("\n📊 Creating indexes for 'users' collection...")
    users = db.users
    
    # Unique indexes
    await users.create_index([("email", 1)], unique=True, name="idx_users_email")
    print("  ✅ Created unique index on 'email'")
    
    await users.create_index([("username", 1)], unique=True, name="idx_users_username")
    print("  ✅ Created unique index on 'username'")
    
    # Query optimization indexes
    await users.create_index([("role", 1)], name="idx_users_role")
    print("  ✅ Created index on 'role'")
    
    await users.create_index([("is_active", 1)], name="idx_users_is_active")
    print("  ✅ Created index on 'is_active'")
    
    # Array indexes for matching
    await users.create_index([("skills.interests", 1)], name="idx_users_interests")
    print("  ✅ Created index on 'skills.interests'")
    
    await users.create_index([("expertise_areas", 1)], name="idx_users_expertise")
    print("  ✅ Created index on 'expertise_areas'")
    
    await users.create_index([("skills.strengths", 1)], name="idx_users_strengths")
    print("  ✅ Created index on 'skills.strengths'")
    
    # Compound indexes
    await users.create_index([("role", 1), ("is_active", 1)], name="idx_users_role_active")
    print("  ✅ Created compound index on 'role' + 'is_active'")
    
    # Posts Collection Indexes
    print("\n📊 Creating indexes for 'posts' collection...")
    posts = db.posts
    
    await posts.create_index([("user_id", 1)], name="idx_posts_user")
    print("  ✅ Created index on 'user_id'")
    
    await posts.create_index([("created_at", -1)], name="idx_posts_created_desc")
    print("  ✅ Created index on 'created_at' (descending)")
    
    await posts.create_index([("tags", 1)], name="idx_posts_tags")
    print("  ✅ Created index on 'tags'")
    
    await posts.create_index([("likes", 1)], name="idx_posts_likes")
    print("  ✅ Created index on 'likes'")
    
    # Compound index for feed queries
    await posts.create_index([("created_at", -1), ("user_id", 1)], name="idx_posts_feed")
    print("  ✅ Created compound index for feed queries")
    
    # Matches Collection Indexes
    print("\n📊 Creating indexes for 'matches' collection...")
    matches = db.matches
    
    await matches.create_index([("mentor_id", 1)], name="idx_matches_mentor")
    print("  ✅ Created index on 'mentor_id'")
    
    await matches.create_index([("mentee_id", 1)], name="idx_matches_mentee")
    print("  ✅ Created index on 'mentee_id'")
    
    await matches.create_index([("status", 1)], name="idx_matches_status")
    print("  ✅ Created index on 'status'")
    
    await matches.create_index([("match_type", 1)], name="idx_matches_type")
    print("  ✅ Created index on 'match_type'")
    
    await matches.create_index([("created_at", -1)], name="idx_matches_created_desc")
    print("  ✅ Created index on 'created_at' (descending)")
    
    # Compound indexes for match queries
    await matches.create_index([("mentor_id", 1), ("status", 1)], name="idx_matches_mentor_status")
    print("  ✅ Created compound index on 'mentor_id' + 'status'")
    
    await matches.create_index([("mentee_id", 1), ("status", 1)], name="idx_matches_mentee_status")
    print("  ✅ Created compound index on 'mentee_id' + 'status'")
    
    # Study Groups Collection Indexes
    print("\n📊 Creating indexes for 'study_groups' collection...")
    study_groups = db.study_groups
    
    await study_groups.create_index([("created_by", 1)], name="idx_groups_creator")
    print("  ✅ Created index on 'created_by'")
    
    await study_groups.create_index([("topics", 1)], name="idx_groups_topics")
    print("  ✅ Created index on 'topics'")
    
    await study_groups.create_index([("members.user_id", 1)], name="idx_groups_members")
    print("  ✅ Created index on 'members.user_id'")
    
    await study_groups.create_index([("is_active", 1)], name="idx_groups_active")
    print("  ✅ Created index on 'is_active'")
    
    await study_groups.create_index([("created_at", -1)], name="idx_groups_created_desc")
    print("  ✅ Created index on 'created_at' (descending)")
    
    # Text index for search
    await study_groups.create_index([("name", "text"), ("description", "text")], name="idx_groups_search")
    print("  ✅ Created text search index on 'name' + 'description'")
    
    # Feedback Collection Indexes
    print("\n📊 Creating indexes for 'feedback' collection...")
    feedback = db.feedback
    
    await feedback.create_index([("match_id", 1)], name="idx_feedback_match")
    print("  ✅ Created index on 'match_id'")
    
    await feedback.create_index([("from_user_id", 1)], name="idx_feedback_from")
    print("  ✅ Created index on 'from_user_id'")
    
    await feedback.create_index([("to_user_id", 1)], name="idx_feedback_to")
    print("  ✅ Created index on 'to_user_id'")
    
    await feedback.create_index([("rating", 1)], name="idx_feedback_rating")
    print("  ✅ Created index on 'rating'")
    
    await feedback.create_index([("created_at", -1)], name="idx_feedback_created_desc")
    print("  ✅ Created index on 'created_at' (descending)")
    
    # Compound index for user feedback queries
    await feedback.create_index([("to_user_id", 1), ("rating", 1)], name="idx_feedback_to_rating")
    print("  ✅ Created compound index on 'to_user_id' + 'rating'")
    
    print("\n" + "=" * 60)
    print("✅ All indexes created successfully!")
    print("\n📈 Index Statistics:")
    
    # Show index stats
    collections = [
        ('users', users),
        ('posts', posts),
        ('matches', matches),
        ('study_groups', study_groups),
        ('feedback', feedback)
    ]
    
    total_indexes = 0
    for name, collection in collections:
        indexes = await collection.index_information()
        index_count = len(indexes)
        total_indexes += index_count
        print(f"  • {name}: {index_count} indexes")
    
    print(f"\n  Total indexes created: {total_indexes}")
    print("\n💡 Tip: Run this script after any database reset to ensure optimal performance")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(create_indexes())
