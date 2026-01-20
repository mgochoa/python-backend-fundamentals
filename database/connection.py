"""
Database Connection Management Module

This module provides utilities for connecting to and interacting with the SQLite database.
Students will learn about:
- Database connection management and resource cleanup
- Parameterized queries to prevent SQL injection
- Error handling for database operations
- Context managers for automatic resource management
- The difference between query (SELECT) and update (INSERT/UPDATE/DELETE) operations

Key Concepts:
1. Connection Management: Opening and closing database connections properly
2. Cursor Objects: Used to execute SQL statements and fetch results
3. Parameterized Queries: Using placeholders (?) to safely insert user data
4. Row Factory: Converting query results to dictionary-like objects
5. Transaction Management: Committing changes or rolling back on errors
"""

import sqlite3
from typing import List, Optional, Any, Dict
from pathlib import Path

# Import database configuration
from config.database import get_database_path, get_database_config


# Custom Exception Classes
# These help us provide clear, specific error messages to users

class DatabaseConnectionError(Exception):
    """
    Raised when we cannot connect to the database.
    
    This might happen if:
    - The database file is locked by another process
    - We don't have permission to access the file
    - The disk is full and we can't create the file
    """
    pass


class QueryExecutionError(Exception):
    """
    Raised when a SQL query fails to execute.
    
    This might happen if:
    - The SQL syntax is incorrect
    - A table or column doesn't exist
    - A constraint is violated (e.g., unique, foreign key)
    - The database is locked during a write operation
    """
    pass


def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.
    
    This function:
    1. Gets the database path from configuration
    2. Creates a connection with appropriate settings
    3. Configures the connection to return rows as dictionaries
    4. Enables foreign key constraint checking
    
    Returns:
        sqlite3.Connection: An active database connection
        
    Raises:
        DatabaseConnectionError: If the connection cannot be established
    
    Example:
        >>> conn = get_connection()
        >>> # Use the connection for queries
        >>> conn.close()  # Always close when done!
    
    Learning Notes:
    - SQLite connections are lightweight but should still be closed properly
    - The row_factory setting makes results easier to work with
    - Foreign keys must be explicitly enabled in SQLite
    - In production, you might use connection pooling for better performance
    """
    try:
        # Get the database path from our configuration
        db_path = get_database_path()
        config = get_database_config()
        
        # Create the connection with timeout setting
        # timeout: how long to wait if database is locked (in seconds)
        conn = sqlite3.connect(
            db_path,
            timeout=config.get("timeout", 10.0),
            check_same_thread=config.get("check_same_thread", False)
        )
        
        # Set row_factory to sqlite3.Row
        # This makes query results behave like dictionaries
        # Instead of: result[0], result[1]
        # We can use: result['id'], result['title']
        conn.row_factory = sqlite3.Row
        
        # Enable foreign key constraints
        # SQLite doesn't enforce foreign keys by default!
        # This ensures referential integrity (e.g., can't delete a book that's currently loaned)
        conn.execute("PRAGMA foreign_keys = ON")
        
        return conn
        
    except sqlite3.Error as e:
        # Convert SQLite-specific error to our custom error
        # This provides a cleaner interface for the rest of our application
        raise DatabaseConnectionError(
            f"Failed to connect to database at {db_path}: {str(e)}"
        )


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return the results.
    
    This function is for READ operations only (SELECT statements).
    It handles:
    1. Opening a database connection
    2. Executing the query with parameters
    3. Fetching all results
    4. Converting results to a list of dictionaries
    5. Closing the connection (even if an error occurs)
    
    Args:
        query: SQL SELECT statement with ? placeholders for parameters
        params: Tuple of values to substitute for ? placeholders
        
    Returns:
        List of dictionaries, where each dictionary represents one row
        Keys are column names, values are the data from that column
        Returns empty list if no results found
        
    Raises:
        QueryExecutionError: If the query fails to execute
        
    Example:
        >>> # Simple query with no parameters
        >>> books = execute_query("SELECT * FROM books")
        >>> 
        >>> # Query with parameters (SAFE from SQL injection!)
        >>> books = execute_query(
        ...     "SELECT * FROM books WHERE author = ?",
        ...     ("J.K. Rowling",)
        ... )
        >>> 
        >>> # Access results
        >>> for book in books:
        ...     print(f"{book['title']} by {book['author']}")
    
    Learning Notes:
    - ALWAYS use parameterized queries (with ?) instead of string formatting
    - BAD:  f"SELECT * FROM books WHERE author = '{author}'"  # SQL injection risk!
    - GOOD: execute_query("SELECT * FROM books WHERE author = ?", (author,))
    - The ? placeholder is automatically escaped by SQLite
    - Parameters must be a tuple, even for single values: (value,) not (value)
    """
    # We'll use a connection variable that we can reference in finally block
    conn = None
    
    try:
        # Get a database connection
        conn = get_connection()
        
        # Create a cursor - this is what actually executes SQL statements
        # Think of it like a pointer that moves through the database
        cursor = conn.cursor()
        
        # Execute the query with parameters
        # SQLite will safely substitute the ? placeholders with values from params
        cursor.execute(query, params)
        
        # Fetch all results
        # fetchall() returns a list of Row objects
        rows = cursor.fetchall()
        
        # Convert Row objects to dictionaries for easier use
        # Row objects can be accessed like dictionaries: row['column_name']
        # But converting to dict makes them more flexible
        results = [dict(row) for row in rows]
        
        return results
        
    except sqlite3.Error as e:
        # Something went wrong with the query
        # Provide helpful error message including the query (but not sensitive data!)
        raise QueryExecutionError(
            f"Failed to execute query: {str(e)}\n"
            f"Query: {query}\n"
            f"Hint: Check your SQL syntax and table/column names"
        )
        
    finally:
        # ALWAYS close the connection, even if an error occurred
        # This is crucial for preventing resource leaks
        # The finally block runs no matter what (success, error, or return)
        if conn:
            conn.close()


def execute_update(query: str, params: tuple = ()) -> int:
    """
    Execute an INSERT, UPDATE, or DELETE query.
    
    This function is for WRITE operations (INSERT, UPDATE, DELETE).
    It handles:
    1. Opening a database connection
    2. Executing the query with parameters
    3. Committing the transaction (saving changes)
    4. Returning the number of affected rows
    5. Rolling back on error (undoing changes)
    6. Closing the connection
    
    Args:
        query: SQL INSERT, UPDATE, or DELETE statement with ? placeholders
        params: Tuple of values to substitute for ? placeholders
        
    Returns:
        int: Number of rows affected by the operation
        - For INSERT: usually 1 (or 0 if nothing inserted)
        - For UPDATE: number of rows that were updated
        - For DELETE: number of rows that were deleted
        
    Raises:
        QueryExecutionError: If the query fails to execute
        
    Example:
        >>> # INSERT a new book
        >>> affected = execute_update(
        ...     "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
        ...     ("Python Crash Course", "Eric Matthes", "978-1593279288")
        ... )
        >>> print(f"Inserted {affected} row(s)")
        >>> 
        >>> # UPDATE a book's availability
        >>> affected = execute_update(
        ...     "UPDATE books SET available = ? WHERE id = ?",
        ...     (False, 1)
        ... )
        >>> print(f"Updated {affected} row(s)")
        >>> 
        >>> # DELETE a book
        >>> affected = execute_update(
        ...     "DELETE FROM books WHERE id = ?",
        ...     (1,)
        ... )
        >>> print(f"Deleted {affected} row(s)")
    
    Learning Notes:
    - Changes are not permanent until we call commit()
    - If an error occurs, we call rollback() to undo changes
    - This is called "transaction management"
    - Transactions ensure data consistency (all changes succeed or all fail)
    - rowcount tells us how many rows were affected
    - For INSERT, you can get the new row's ID with cursor.lastrowid
    """
    conn = None
    
    try:
        # Get a database connection
        conn = get_connection()
        
        # Create a cursor to execute the query
        cursor = conn.cursor()
        
        # Execute the query with parameters
        cursor.execute(query, params)
        
        # Commit the transaction
        # This makes the changes permanent in the database
        # Without commit(), changes are only in memory and will be lost!
        conn.commit()
        
        # Return the number of affected rows
        # This is useful for checking if the operation actually did something
        # For example, UPDATE might affect 0 rows if no records matched the WHERE clause
        return cursor.rowcount
        
    except sqlite3.IntegrityError as e:
        # Integrity errors are special - they mean a constraint was violated
        # Examples: unique constraint, foreign key constraint, not null constraint
        if conn:
            conn.rollback()  # Undo any changes
        
        # Provide a helpful error message
        error_msg = str(e).lower()
        if "unique" in error_msg:
            raise QueryExecutionError(
                f"Duplicate entry: A record with this unique value already exists.\n"
                f"Details: {str(e)}"
            )
        elif "foreign key" in error_msg:
            raise QueryExecutionError(
                f"Invalid reference: The referenced record does not exist.\n"
                f"Details: {str(e)}"
            )
        elif "not null" in error_msg:
            raise QueryExecutionError(
                f"Missing required field: A required value was not provided.\n"
                f"Details: {str(e)}"
            )
        else:
            raise QueryExecutionError(
                f"Database constraint violation: {str(e)}"
            )
            
    except sqlite3.Error as e:
        # Other database errors
        if conn:
            conn.rollback()  # Undo any changes
            
        raise QueryExecutionError(
            f"Failed to execute update: {str(e)}\n"
            f"Query: {query}\n"
            f"Hint: Check your SQL syntax and ensure the table exists"
        )
        
    finally:
        # ALWAYS close the connection
        if conn:
            conn.close()


# Additional helper function for getting the last inserted ID
def execute_insert(query: str, params: tuple = ()) -> int:
    """
    Execute an INSERT query and return the ID of the newly created record.
    
    This is a convenience function specifically for INSERT operations
    where you need to know the ID of the new record.
    
    Args:
        query: SQL INSERT statement with ? placeholders
        params: Tuple of values to substitute for ? placeholders
        
    Returns:
        int: The ID (primary key) of the newly inserted record
        
    Raises:
        QueryExecutionError: If the query fails to execute
        
    Example:
        >>> # Insert a book and get its ID
        >>> book_id = execute_insert(
        ...     "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
        ...     ("Learning Python", "Mark Lutz", "978-1449355739")
        ... )
        >>> print(f"New book created with ID: {book_id}")
        >>> 
        >>> # Now we can use this ID to create related records
        >>> loan_id = execute_insert(
        ...     "INSERT INTO loans (book_id, member_id, due_date) VALUES (?, ?, ?)",
        ...     (book_id, 1, "2024-12-31")
        ... )
    
    Learning Notes:
    - lastrowid gives us the auto-generated ID from AUTOINCREMENT
    - This only works for tables with INTEGER PRIMARY KEY AUTOINCREMENT
    - Very useful for creating related records (foreign key relationships)
    - In other databases (MySQL, PostgreSQL), the syntax might be different
    """
    conn = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Execute the INSERT query
        cursor.execute(query, params)
        
        # Get the ID of the newly inserted row
        # lastrowid is set by SQLite after an INSERT
        new_id = cursor.lastrowid
        
        # Commit the transaction
        conn.commit()
        
        return new_id
        
    except sqlite3.IntegrityError as e:
        if conn:
            conn.rollback()
        
        error_msg = str(e).lower()
        if "unique" in error_msg:
            raise QueryExecutionError(
                f"Duplicate entry: A record with this unique value already exists.\n"
                f"Details: {str(e)}"
            )
        elif "foreign key" in error_msg:
            raise QueryExecutionError(
                f"Invalid reference: The referenced record does not exist.\n"
                f"Details: {str(e)}"
            )
        else:
            raise QueryExecutionError(
                f"Database constraint violation: {str(e)}"
            )
            
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
            
        raise QueryExecutionError(
            f"Failed to execute insert: {str(e)}\n"
            f"Query: {query}"
        )
        
    finally:
        if conn:
            conn.close()


# Context Manager for Advanced Students
class DatabaseConnection:
    """
    Context manager for database connections.
    
    This is an ADVANCED pattern using Python's 'with' statement.
    It automatically handles opening and closing connections.
    
    Example:
        >>> with DatabaseConnection() as conn:
        ...     cursor = conn.cursor()
        ...     cursor.execute("SELECT * FROM books")
        ...     results = cursor.fetchall()
        >>> # Connection is automatically closed here!
    
    Learning Notes:
    - Context managers use __enter__ and __exit__ methods
    - The 'with' statement ensures cleanup happens automatically
    - This is the same pattern used by open() for files
    - More advanced than the execute_query/execute_update functions
    - Useful when you need more control over the connection
    """
    
    def __init__(self):
        """Initialize the context manager."""
        self.conn = None
    
    def __enter__(self) -> sqlite3.Connection:
        """
        Called when entering the 'with' block.
        Opens and returns the database connection.
        """
        self.conn = get_connection()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' block.
        Closes the connection and handles any errors.
        
        Args:
            exc_type: Type of exception (if one occurred)
            exc_val: Exception value (if one occurred)
            exc_tb: Exception traceback (if one occurred)
        """
        if self.conn:
            if exc_type is not None:
                # An error occurred, rollback any uncommitted changes
                self.conn.rollback()
            self.conn.close()
        
        # Return False to propagate any exception
        # Return True would suppress the exception
        return False


# Module-level documentation for students
"""
SUMMARY OF KEY CONCEPTS:

1. Database Connections:
   - Must be opened before use and closed after
   - Use get_connection() to create a connection
   - Always close connections to prevent resource leaks

2. Parameterized Queries:
   - Use ? placeholders instead of string formatting
   - Prevents SQL injection attacks
   - Example: execute_query("SELECT * FROM books WHERE id = ?", (book_id,))

3. Query vs Update:
   - execute_query(): For SELECT (reading data)
   - execute_update(): For INSERT, UPDATE, DELETE (modifying data)
   - execute_insert(): For INSERT when you need the new record's ID

4. Error Handling:
   - DatabaseConnectionError: Can't connect to database
   - QueryExecutionError: Query failed to execute
   - Always includes helpful error messages

5. Transactions:
   - Changes aren't permanent until commit() is called
   - Use rollback() to undo changes if something goes wrong
   - execute_update() handles this automatically

6. Best Practices:
   - Always use parameterized queries
   - Always close connections (use try/finally)
   - Check rowcount to see if operation affected any rows
   - Use meaningful error messages

NEXT STEPS:
- Study the example queries in models/library.py
- Try writing your own queries in models/todo.py
- Experiment with the Python REPL to test queries
- Read about SQL injection to understand why parameterization matters
"""
