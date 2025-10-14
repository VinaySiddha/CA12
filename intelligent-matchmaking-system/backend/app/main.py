"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import (
    auth_routes,
    user_routes,
    match_routes,
    feedback_routes,
    admin_routes,
    gamification_routes,
    ml_routes,
    token_routes,
    social_routes,
    resource_routes,
    meeting_routes,
    chat_routes,
    notification_routes
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    description="An intelligent matchmaking system for peer-assisted learning in educational communities",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.vercel.app"]
)

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(token_routes.router, prefix="/token", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(match_routes.router, prefix="/matches", tags=["Matches"])
app.include_router(feedback_routes.router, prefix="/feedback", tags=["Feedback"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(gamification_routes.router, prefix="/gamification", tags=["Gamification"])
app.include_router(social_routes.router, prefix="/social", tags=["Social Feed"])
app.include_router(ml_routes.router, prefix="/ml", tags=["Machine Learning"])
app.include_router(resource_routes.router, tags=["Resources"])
app.include_router(meeting_routes.router, tags=["Meetings"])
app.include_router(chat_routes.router, tags=["Chat"])
app.include_router(notification_routes.router, tags=["Notifications"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the Intelligent Matchmaking System API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-01-01T00:00:00Z"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)