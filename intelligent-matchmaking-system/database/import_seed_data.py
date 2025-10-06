#!/usr/bin/env python3
"""
Windows-compatible seed data importer for MongoDB
This script replaces the need for 'jq' command on Windows systems
"""
import json
import os
from pymongo import MongoClient
from datetime import datetime
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def connect_to_mongodb():
    """Connect to MongoDB database"""
    try:
        # Try to connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['intelligent_matchmaking']
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB")
        return db
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return None

def load_seed_data():
    """Load seed data from JSON file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    seed_file = os.path.join(script_dir, 'seed_data.json')
    
    try:
        with open(seed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Successfully loaded seed data from {seed_file}")
        return data
    except FileNotFoundError:
        print(f"❌ Seed data file not found: {seed_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in seed data: {e}")
        return None

def import_collection(db, collection_name, data):
    """Import data into a specific collection"""
    if not data:
        print(f"⚠️  No data to import for {collection_name}")
        return 0
    
    try:
        collection = db[collection_name]
        
        # Special handling for users collection to fix bcrypt hashes
        if collection_name == 'users':
            fixed_data = []
            default_password = "password123"
            proper_hash = pwd_context.hash(default_password)
            
            for user in data:
                # Create a copy of the user data
                fixed_user = user.copy()
                
                # Check if password hash is malformed
                current_hash = user.get('hashed_password', '')
                if (not current_hash.startswith('$2b$') or 
                    len(current_hash) < 60 or 
                    'example' in current_hash):
                    
                    print(f"🔧 Fixing password hash for user: {user.get('email', 'unknown')}")
                    fixed_user['hashed_password'] = proper_hash
                
                fixed_data.append(fixed_user)
            
            data = fixed_data
            print(f"✅ Fixed password hashes. Default password: {default_password}")
        
        # Clear existing data
        result = collection.delete_many({})
        print(f"🗑️  Cleared {result.deleted_count} existing documents from {collection_name}")
        
        # Insert new data
        if isinstance(data, list):
            result = collection.insert_many(data)
            count = len(result.inserted_ids)
        else:
            result = collection.insert_one(data)
            count = 1
            
        print(f"✅ Imported {count} documents into {collection_name}")
        return count
        
    except Exception as e:
        print(f"❌ Failed to import {collection_name}: {e}")
        return 0

def main():
    """Main function to import all seed data"""
    print("🚀 Starting seed data import...")
    print("=" * 50)
    
    # Connect to database
    db = connect_to_mongodb()
    if db is None:
        return
    
    # Load seed data
    seed_data = load_seed_data()
    if not seed_data:
        return
    
    # Import each collection
    total_imported = 0
    collections_to_import = [
        'users',
        'study_groups', 
        'learning_resources',
        'sessions',
        'matches',
        'feedback',
        'gamification',
        'notifications'
    ]
    
    print("\n📊 Importing collections:")
    print("-" * 30)
    
    for collection_name in collections_to_import:
        if collection_name in seed_data:
            count = import_collection(db, collection_name, seed_data[collection_name])
            total_imported += count
        else:
            print(f"⚠️  No data found for {collection_name}")
    
    print("\n" + "=" * 50)
    print(f"🎉 Import completed! Total documents imported: {total_imported}")
    
    # Display collection stats
    print("\n📈 Database Statistics:")
    print("-" * 30)
    
    for collection_name in collections_to_import:
        try:
            count = db[collection_name].count_documents({})
            print(f"{collection_name:20}: {count:4} documents")
        except Exception as e:
            print(f"{collection_name:20}: Error - {e}")
    
    print("\n✅ Seed data import completed successfully!")

if __name__ == "__main__":
    main()