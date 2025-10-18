#!/usr/bin/env python3
"""
Test script to verify profile update functionality
"""
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.security import get_password_hash, verify_password

def test_password_functionality():
    """Test password hashing and verification"""
    print("Testing password functionality...")
    
    # Test normal password
    normal_password = "test123"
    hashed = get_password_hash(normal_password)
    print(f"Normal password hashed: {bool(hashed)}")
    print(f"Normal password verified: {verify_password(normal_password, hashed)}")
    
    # Test long password (over 72 bytes)
    long_password = "a" * 100
    hashed_long = get_password_hash(long_password)
    print(f"Long password hashed: {bool(hashed_long)}")
    print(f"Long password verified: {verify_password(long_password, hashed_long)}")
    
    # Test unicode password
    unicode_password = "test123ñáéíóú"
    hashed_unicode = get_password_hash(unicode_password)
    print(f"Unicode password hashed: {bool(hashed_unicode)}")
    print(f"Unicode password verified: {verify_password(unicode_password, hashed_unicode)}")
    
    print("All password tests passed!")

if __name__ == "__main__":
    test_password_functionality()