"""
Database Setup Script

This script initializes the database for the Python Backend Learning Project.
It creates the database file and sets up all necessary tables.

Students will learn about:
- Database initialization and setup processes
- Reading and executing SQL schema files
- Error handling during setup
- Providing clear user feedback

Usage:
    python setup.py              # Interactive mode (prompts before overwriting)
    python setup.py --force      # Force mode (overwrites without prompting)
    python setup.py -f           # Short form of --force
    python setup.py --help       # Show help message
    python setup.py -h           # Short form of --help

What this script does:
1. Checks if database already exists (warns before overwriting)
2. Creates the database file
3. Executes schema files to create tables
4. Provides clear success/error messages
5. Verifies the setup was successful
"""

import sys
import sqlite3
from pathlib import Path
from typing import List, Tuple

# Import our database configuration
from config.database import get_database_path, DATABASE_PATH


def print_header():
    """Print a welcome header for the setup script."""
    print("=" * 60)
    print("  Python Backend Learning Project - Database Setup")
    print("=" * 60)
    print()


def print_success(message: str):
    """Print a success message with a checkmark."""
    print(f"✓ {message}")


def print_error(message: str):
    """Print an error message with an X."""
    print(f"✗ {message}")


def print_info(message: str):
    """Print an informational message."""
    print(f"ℹ {message}")


def check_existing_database() -> bool:
    """
    Check if the database file already exists.
    
    Returns:
        bool: True if database exists, False otherwise
    
    Learning Note:
    - Path.exists() checks if a file or directory exists
    - Good practice to check before overwriting data
    """
    db_path = Path(get_database_path())
    return db_path.exists()


def get_schema_files() -> List[Path]:
    """
    Get all SQL schema files from the database/schemas directory.
    
    Returns:
        List[Path]: List of paths to .sql files, sorted alphabetically
    
    Learning Note:
    - glob() finds files matching a pattern (* is wildcard)
    - sorted() ensures consistent execution order
    - We execute schemas in alphabetical order for predictability
    """
    schemas_dir = Path(__file__).parent / "database" / "schemas"
    
    # Find all .sql files in the schemas directory
    schema_files = list(schemas_dir.glob("*.sql"))
    
    # Sort alphabetically for consistent order
    # This matters if schemas have dependencies on each other
    return sorted(schema_files)


def read_schema_file(schema_path: Path) -> str:
    """
    Read the contents of a schema SQL file.
    
    Args:
        schema_path: Path to the .sql file
    
    Returns:
        str: Contents of the SQL file
    
    Raises:
        FileNotFoundError: If the schema file doesn't exist
        IOError: If the file cannot be read
    
    Learning Note:
    - 'with' statement ensures file is closed automatically
    - 'utf-8' encoding handles special characters properly
    - Always use context managers (with) for file operations
    """
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    except IOError as e:
        raise IOError(f"Error reading schema file {schema_path}: {e}")


def execute_schema(conn: sqlite3.Connection, schema_sql: str, schema_name: str) -> None:
    """
    Execute a SQL schema to create tables.
    
    Args:
        conn: Active database connection
        schema_sql: SQL statements to execute
        schema_name: Name of the schema (for error messages)
    
    Raises:
        sqlite3.Error: If SQL execution fails
    
    Learning Note:
    - executescript() can run multiple SQL statements at once
    - It automatically commits after execution
    - Useful for running entire schema files
    - Different from execute() which runs one statement at a time
    """
    try:
        cursor = conn.cursor()
        
        # executescript() runs multiple SQL statements separated by semicolons
        # It's perfect for schema files that contain multiple CREATE TABLE statements
        cursor.executescript(schema_sql)
        
        print_success(f"Executed schema: {schema_name}")
        
    except sqlite3.Error as e:
        # Provide detailed error information
        print_error(f"Failed to execute schema: {schema_name}")
        print_error(f"Error details: {str(e)}")
        raise


def verify_setup(conn: sqlite3.Connection) -> Tuple[bool, List[str]]:
    """
    Verify that tables were created successfully.
    
    Args:
        conn: Active database connection
    
    Returns:
        Tuple of (success: bool, table_names: List[str])
    
    Learning Note:
    - sqlite_master is a special table that stores database schema info
    - It contains metadata about all tables, indexes, etc.
    - Querying it is a good way to verify database structure
    """
    try:
        cursor = conn.cursor()
        
        # Query the sqlite_master table to get all table names
        # type='table' filters out indexes, views, etc.
        # name NOT LIKE 'sqlite_%' excludes internal SQLite tables
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        
        if tables:
            return True, tables
        else:
            return False, []
            
    except sqlite3.Error as e:
        print_error(f"Error verifying setup: {str(e)}")
        return False, []


def initialize_database(force: bool = False) -> bool:
    """
    Initialize the database by creating tables from schema files.
    
    Args:
        force: If True, overwrite existing database without prompting
    
    Returns:
        bool: True if initialization succeeded, False otherwise
    
    This is the main function that orchestrates the setup process.
    """
    db_path = Path(get_database_path())
    
    # Check if database already exists
    if check_existing_database() and not force:
        print_info(f"Database already exists at: {db_path}")
        response = input("Do you want to recreate it? This will DELETE all existing data! (yes/no): ")
        
        if response.lower() not in ['yes', 'y']:
            print_info("Setup cancelled. Existing database preserved.")
            return False
        
        # Delete the existing database
        try:
            db_path.unlink()
            print_success("Removed existing database")
        except OSError as e:
            print_error(f"Failed to remove existing database: {e}")
            return False
    
    # Ensure the data directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    print_success(f"Data directory ready: {db_path.parent}")
    
    # Get all schema files
    schema_files = get_schema_files()
    
    if not schema_files:
        print_info("No schema files found in database/schemas/")
        print_info("Creating empty database...")
        print_info("")
        print_info("To add tables, create .sql files in database/schemas/")
        print_info("Example: database/schemas/library_schema.sql")
        
        # Create an empty database file
        try:
            conn = sqlite3.connect(str(db_path))
            conn.close()
            print_success(f"Empty database created at: {db_path}")
            return True
        except sqlite3.Error as e:
            print_error(f"Failed to create database: {e}")
            return False
    
    print_info(f"Found {len(schema_files)} schema file(s) to execute:")
    for schema_file in schema_files:
        print(f"  - {schema_file.name}")
    print()
    
    # Create database connection
    try:
        conn = sqlite3.connect(str(db_path))
        print_success(f"Database connection established")
        
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        
    except sqlite3.Error as e:
        print_error(f"Failed to connect to database: {e}")
        return False
    
    # Execute each schema file
    try:
        for schema_file in schema_files:
            print_info(f"Processing {schema_file.name}...")
            
            # Read the schema file
            try:
                schema_sql = read_schema_file(schema_file)
            except (FileNotFoundError, IOError) as e:
                print_error(str(e))
                conn.close()
                return False
            
            # Execute the schema
            execute_schema(conn, schema_sql, schema_file.name)
        
        print()
        
        # Verify the setup
        success, tables = verify_setup(conn)
        
        if success:
            print_success("Database setup completed successfully!")
            print()
            print_info(f"Created {len(tables)} table(s):")
            for table in tables:
                print(f"  - {table}")
            print()
            print_info(f"Database location: {db_path}")
            print_info("You can now run your Python scripts to interact with the database!")
            
        else:
            print_error("Setup completed but no tables were created.")
            print_info("Check your schema files for errors.")
        
        conn.close()
        return success
        
    except sqlite3.Error as e:
        print_error(f"Database setup failed: {e}")
        if conn:
            conn.close()
        return False


def main():
    """
    Main entry point for the setup script.
    
    Learning Note:
    - if __name__ == "__main__" ensures this only runs when script is executed directly
    - Not when imported as a module
    - sys.exit() returns an exit code (0 = success, 1 = failure)
    - Exit codes are used by shell scripts and CI/CD systems
    - sys.argv contains command-line arguments
    """
    # Check for help flag
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Python Backend Learning Project - Database Setup")
        print()
        print("Usage:")
        print("  python setup.py              Interactive mode (prompts before overwriting)")
        print("  python setup.py --force      Force mode (overwrites without prompting)")
        print("  python setup.py -f           Short form of --force")
        print("  python setup.py --help       Show this help message")
        print("  python setup.py -h           Short form of --help")
        print()
        print("This script initializes the database by:")
        print("  1. Creating the database file (data/learning_project.db)")
        print("  2. Executing all .sql schema files in database/schemas/")
        print("  3. Verifying that tables were created successfully")
        print()
        sys.exit(0)
    
    print_header()
    
    print("This script will set up your database for the learning project.")
    print("It will create tables based on SQL schema files in database/schemas/")
    print()
    
    # Check for --force flag in command-line arguments
    force = "--force" in sys.argv or "-f" in sys.argv
    
    if force:
        print_info("Running in force mode (will overwrite existing database)")
        print()
    
    try:
        success = initialize_database(force=force)
        
        if success:
            print()
            print("=" * 60)
            print("  Setup Complete! Happy Learning! 🎉")
            print("=" * 60)
            sys.exit(0)
        else:
            print()
            print("=" * 60)
            print("  Setup Failed - Please check the errors above")
            print("=" * 60)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print()
        print_info("Setup interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print()
        print_error(f"Unexpected error during setup: {e}")
        print_error("Please report this issue if it persists")
        sys.exit(1)


if __name__ == "__main__":
    main()


"""
LEARNING SUMMARY:

Key Concepts Demonstrated:
1. File Operations: Reading SQL files, checking if files exist
2. Path Handling: Using pathlib.Path for cross-platform compatibility
3. Database Operations: Creating database, executing SQL scripts
4. Error Handling: Try-except blocks with specific error types
5. User Interaction: Prompting for confirmation, providing feedback
6. Script Organization: Breaking complex tasks into small functions

Common Issues and Solutions:
- "Database is locked": Close other programs accessing the database
- "No such table": Schema files weren't executed properly
- "Permission denied": Check file permissions on the data directory
- "Syntax error in SQL": Check your schema files for SQL errors

Next Steps:
1. Create schema files in database/schemas/ (e.g., library_schema.sql)
2. Run this script: python setup.py
3. Verify tables were created
4. Start implementing your models in models/

Tips for Students:
- Read the error messages carefully - they tell you what went wrong
- Start with simple schemas before adding complex relationships
- Test your SQL in a SQLite browser before adding to schema files
- Use CREATE TABLE IF NOT EXISTS to make schemas re-runnable
"""
