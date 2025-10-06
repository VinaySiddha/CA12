// MongoDB setup script for the Intelligent Matchmaking System
// Run this script with: mongosh mongodb://localhost:27017/intelligent_matchmaking

// Switch to the database
db = db.getSiblingDB('intelligent_matchmaking');

// Create indexes for better performance

// Users collection indexes
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "profile.field_of_study": 1 });
db.users.createIndex({ "profile.academic_level": 1 });
db.users.createIndex({ "skills.interests": 1 });
db.users.createIndex({ "skills.strengths": 1 });
db.users.createIndex({ "skills.weaknesses": 1 });
db.users.createIndex({ "location.coordinates": "2dsphere" });
db.users.createIndex({ "is_active": 1, "last_active": -1 });
db.users.createIndex({ "created_at": -1 });
db.users.createIndex({ "points": -1 });
db.users.createIndex({ "level": -1 });

// Matches collection indexes
db.matches.createIndex({ "user_id": 1, "created_at": -1 });
db.matches.createIndex({ "matched_user_id": 1, "created_at": -1 });
db.matches.createIndex({ "status": 1 });
db.matches.createIndex({ "compatibility_score": -1 });
db.matches.createIndex({ "topics": 1 });
db.matches.createIndex({ "match_type": 1 });
db.matches.createIndex({ "user_id": 1, "matched_user_id": 1 }, { unique: true });

// Feedback collection indexes
db.feedback.createIndex({ "session_id": 1 });
db.feedback.createIndex({ "reviewer_id": 1, "created_at": -1 });
db.feedback.createIndex({ "reviewee_id": 1, "created_at": -1 });
db.feedback.createIndex({ "rating": -1 });
db.feedback.createIndex({ "sentiment": 1 });
db.feedback.createIndex({ "created_at": -1 });

// Gamification collection indexes
db.gamification.createIndex({ "user_id": 1 }, { unique: true });
db.gamification.createIndex({ "points": -1 });
db.gamification.createIndex({ "level": -1 });
db.gamification.createIndex({ "badges.earned_date": -1 });
db.gamification.createIndex({ "achievements.earned_date": -1 });

// Study Groups collection indexes
db.study_groups.createIndex({ "topic": 1 });
db.study_groups.createIndex({ "subject": 1 });
db.study_groups.createIndex({ "difficulty_level": 1 });
db.study_groups.createIndex({ "member_ids": 1 });
db.study_groups.createIndex({ "creator_id": 1 });
db.study_groups.createIndex({ "is_active": 1, "created_at": -1 });
db.study_groups.createIndex({ "max_members": 1 });

// Sessions collection indexes
db.sessions.createIndex({ "participants": 1, "scheduled_time": -1 });
db.sessions.createIndex({ "topic": 1 });
db.sessions.createIndex({ "status": 1 });
db.sessions.createIndex({ "created_at": -1 });
db.sessions.createIndex({ "scheduled_time": 1 });

// Learning Resources collection indexes
db.learning_resources.createIndex({ "topics": 1 });
db.learning_resources.createIndex({ "difficulty_level": 1 });
db.learning_resources.createIndex({ "resource_type": 1 });
db.learning_resources.createIndex({ "average_rating": -1 });
db.learning_resources.createIndex({ "created_at": -1 });

// Notifications collection indexes
db.notifications.createIndex({ "user_id": 1, "created_at": -1 });
db.notifications.createIndex({ "is_read": 1 });
db.notifications.createIndex({ "notification_type": 1 });
db.notifications.createIndex({ "created_at": -1 });

// Messages collection indexes (for future chat feature)
db.messages.createIndex({ "conversation_id": 1, "timestamp": -1 });
db.messages.createIndex({ "sender_id": 1, "timestamp": -1 });
db.messages.createIndex({ "recipient_id": 1, "timestamp": -1 });

// Analytics collection indexes
db.analytics.createIndex({ "event_type": 1, "timestamp": -1 });
db.analytics.createIndex({ "user_id": 1, "timestamp": -1 });
db.analytics.createIndex({ "timestamp": -1 });

// Create text indexes for search functionality
db.users.createIndex({
    "profile.full_name": "text",
    "profile.bio": "text",
    "skills.interests": "text",
    "skills.strengths": "text"
});

db.study_groups.createIndex({
    "name": "text",
    "description": "text",
    "topic": "text"
});

db.learning_resources.createIndex({
    "title": "text",
    "description": "text",
    "topics": "text"
});

// Create TTL indexes for temporary data
db.password_reset_tokens.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 });
db.email_verification_tokens.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 });
db.sessions.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 });

// Print success message
print("MongoDB indexes created successfully!");
print("Database: intelligent_matchmaking");
print("Collections indexed:");
print("- users");
print("- matches");
print("- feedback");
print("- gamification");
print("- study_groups");
print("- sessions");
print("- learning_resources");
print("- notifications");
print("- messages");
print("- analytics");
print("- password_reset_tokens");
print("- email_verification_tokens");

// Display database stats
print("\nDatabase Statistics:");
print("Collections count: " + db.runCommand("listCollections").cursor.firstBatch.length);
print("Database name: " + db.getName());

// Show indexes for each collection
print("\nIndexes created:");
var collections = ["users", "matches", "feedback", "gamification", "study_groups", "sessions", "learning_resources", "notifications", "messages", "analytics"];

collections.forEach(function(collectionName) {
    var indexes = db.getCollection(collectionName).getIndexes();
    print("\n" + collectionName + " (" + indexes.length + " indexes):");
    indexes.forEach(function(index) {
        print("  - " + index.name + ": " + JSON.stringify(index.key));
    });
});

print("\nSetup completed successfully!");