// MongoDB shell script to fix malformed bcrypt hashes
// Run this with: mongo intelligent_matchmaking fix_passwords.js

print("🔧 Fixing malformed bcrypt hashes...");

// Switch to the database
use intelligent_matchmaking

// Proper bcrypt hash for password "password123"
// Generated with bcrypt rounds=12
var properHash = "$2b$12$LQv3c1yqBwEHFqoB/XkLEuMEwtT1B5J2D6jVaLxQfWZWF.ZoqW/Ca";

// Find all users with malformed passwords
var users = db.users.find({});
var updateCount = 0;

users.forEach(function(user) {
    var currentHash = user.hashed_password || '';
    
    // Check if hash is malformed
    if (!currentHash.startsWith('$2b$') || 
        currentHash.length < 60 || 
        currentHash.includes('example')) {
        
        print("Fixing password for user: " + (user.email || user._id));
        
        // Update with proper hash
        var result = db.users.updateOne(
            { "_id": user._id },
            { "$set": { "hashed_password": properHash } }
        );
        
        if (result.modifiedCount > 0) {
            updateCount++;
            print("✅ Updated password for: " + (user.email || user._id));
        } else {
            print("❌ Failed to update: " + (user.email || user._id));
        }
    } else {
        print("✅ Password already valid for: " + (user.email || user._id));
    }
});

print("\n🎉 Fixed " + updateCount + " user passwords");
print("🔑 Default password for all users: password123");
print("\n📋 Test user credentials:");
print("Email: alice.johnson@university.edu");
print("Password: password123");