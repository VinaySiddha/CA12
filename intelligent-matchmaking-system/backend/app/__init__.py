"""
Backend application package for Intelligent Matchmaking System
"""

import logging
import asyncio
import sys
import os

# Add ml directory to path for easier imports
ml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ml'))
if ml_path not in sys.path:
    sys.path.append(ml_path)

__version__ = "1.0.0"
__author__ = "Educational Matchmaking Team"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
logger.info("Initializing Intelligent Matchmaking System backend")