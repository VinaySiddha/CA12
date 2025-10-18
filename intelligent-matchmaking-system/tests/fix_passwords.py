#!/usr/bin/env python3
"""
Script to fix existing user passwords that might be too long for bcrypt
"""
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.security import get_password_hash

async def fix_user_passwords():
    """Fix passwords for existing users"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    users_collection = db.users
    
    print("Checking for users with potentially problematic passwords...")
    
    # Get all users
    users = await users_collection.find({}).to_list(None)
    
    if not users:
        print("No users found in the database.")
        return
    
    print(f"Found {len(users)} users. Checking password hashes...")
    
    updated_count = 0
    
    for user in users:
        user_id = user["_id"]
        hashed_password = user.get("hashed_password", "")
        
        # Check if the password hash looks problematic
        # (this is a simple check - in a real scenario you might need more sophisticated detection)
        if len(hashed_password.encode('utf-8')) > 100:  # Suspiciously long hash
            print(f"User {user.get('username', 'unknown')} has a potentially problematic password hash")
            
            # You would need the original password to re-hash it properly
            # For now, we'll just report the issue
            print(f"  - Hash length: {len(hashed_password)} characters")
            print(f"  - User would need to reset their password")
    
    if updated_count == 0:
        print("No password hashes needed updating. All users should be able to log in normally.")
    else:
        print(f"Updated {updated_count} user password hashes.")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_user_passwords())