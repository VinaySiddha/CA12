#!/usr/bin/env python3
"""
Test script to verify profile update API functionality
"""
import requests
import json

def test_profile_update_api():
    """Test the profile update API endpoint"""
    base_url = "http://localhost:8000"
    
    print("Testing profile update API...")
    
    # Test data matching the backend schema
    test_update_data = {
        "full_name": "Test User Updated",
        "profile": {
            "bio": "Updated bio for testing",
            "academic_level": "Bachelor's Degree",
            "field_of_study": "Computer Science",
            "learning_preferences": ["Visual"],
            "institution": "Test University",
            "timezone": "UTC",
            "languages": ["English"]
        },
        "skills": {
            "interests": ["Programming", "AI"],
            "strengths": ["Python", "JavaScript"],
            "weaknesses": ["Public Speaking"],
            "expertise_level": {
                "Python": 4,
                "JavaScript": 3
            }
        }
    }
    
    print("Test data structure:")
    print(json.dumps(test_update_data, indent=2))
    
    print("\nTo test this manually:")
    print("1. Make sure the backend server is running")
    print("2. Get a valid auth token by logging in")
    print("3. Make a PUT request to /users/profile with the above data")
    print("4. Include 'Authorization: Bearer <your_token>' header")

if __name__ == "__main__":
    test_profile_update_api()