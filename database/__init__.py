"""
Database Package

This package contains all database-related code:
- connection.py: Database connection management and query execution
- schemas/: SQL schema definitions for each topic area
- migrations/: Database initialization and migration scripts

Students will learn about:
- Organizing database code in a dedicated package
- Separating concerns (connection logic, schemas, migrations)
- Python package structure with __init__.py files
"""

# This file makes the 'database' directory a Python package
# It can be left empty or used to expose key functions/classes

# Example of exposing functions for easier imports:
# from .connection import get_connection, execute_query, execute_update
# 
# This would allow: from database import get_connection
# Instead of: from database.connection import get_connection
