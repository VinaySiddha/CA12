"""
Database connection and configuration
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None
    database = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Create database connection"""
    try:
        mongodb.client = AsyncIOMotorClient(settings.mongodb_url)
        mongodb.database = mongodb.client[settings.database_name]
        
        # Test the connection
        await mongodb.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
        logger.info("Disconnected from MongoDB")


def get_database():
    """Get database instance"""
    return mongodb.database


# Collections
def get_users_collection():
    return mongodb.database.users


def get_matches_collection():
    return mongodb.database.matches


def get_feedback_collection():
    return mongodb.database.feedback


def get_gamification_collection():
    return mongodb.database.gamification


def get_sessions_collection():
    return mongodb.database.sessions