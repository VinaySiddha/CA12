#!/usr/bin/env python3
"""
Launch script for the FastAPI application from any directory
"""
import sys
import os
from pathlib import Path

# Get the directory containing this script
script_dir = Path(__file__).parent.absolute()
backend_dir = script_dir 

# Add the backend directory to Python path
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

# Now import and run the application
if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    print("🚀 Starting FastAPI server...")
    print(f"📁 Backend directory: {backend_dir}")
    print(f"🐍 Python path includes: {backend_dir}")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )