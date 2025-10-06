"""
Routes package for the FastAPI application
"""

# Import all route modules to make them available
from . import (
    auth_routes,
    user_routes,
    match_routes,
    feedback_routes,
    admin_routes,
    gamification_routes
)

__all__ = [
    "auth_routes",
    "user_routes", 
    "match_routes",
    "feedback_routes",
    "admin_routes",
    "gamification_routes"
]