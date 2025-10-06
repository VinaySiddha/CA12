"""
Startup script for the FastAPI application
This script properly sets up the Python path and starts the server
"""
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

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