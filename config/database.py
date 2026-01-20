"""
Database Configuration Module

This module contains configuration settings for the database connection.
Students will learn about:
- Centralized configuration management
- Path handling for cross-platform compatibility
- Environment-based configuration (development vs production)
"""

import os
from pathlib import Path

# Get the project root directory (parent of config directory)
PROJECT_ROOT = Path(__file__).parent.parent

# Database file location
# Using Path for cross-platform compatibility (works on Windows, Mac, Linux)
DATABASE_PATH = PROJECT_ROOT / "data" / "learning_project.db"

# Ensure the data directory exists
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# Database configuration settings
DATABASE_CONFIG = {
    "path": str(DATABASE_PATH),
    "timeout": 10.0,  # Connection timeout in seconds
    "check_same_thread": False,  # Allow multi-threaded access (for learning purposes)
}


def get_database_path() -> str:
    """
    Get the path to the database file.
    
    Returns:
        str: Absolute path to the database file
    
    Example:
        >>> db_path = get_database_path()
        >>> print(f"Database located at: {db_path}")
    """
    return DATABASE_CONFIG["path"]


def get_database_config() -> dict:
    """
    Get the complete database configuration dictionary.
    
    Returns:
        dict: Configuration settings for database connection
    
    Example:
        >>> config = get_database_config()
        >>> print(f"Timeout: {config['timeout']} seconds")
    """
    return DATABASE_CONFIG.copy()


# Learning Note:
# In production applications, you might use environment variables for configuration:
# DATABASE_PATH = os.getenv("DATABASE_PATH", "default/path/to/db.sqlite")
# This allows different settings for development, testing, and production environments.
