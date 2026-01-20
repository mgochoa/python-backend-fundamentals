"""
Error Handling Utilities Module

This module provides custom exception classes and error handling utilities.
Students will learn about:
- Creating custom exception classes
- Exception hierarchy and inheritance
- Converting technical errors to user-friendly messages
- Error handling patterns and best practices
- Integrating logging with error handling

Key Concepts:
1. Exception Hierarchy: Organizing exceptions by type
2. Custom Exceptions: Creating meaningful error types
3. Error Messages: Writing clear, actionable error messages
4. Error Recovery: Handling errors gracefully
5. Logging Errors: Recording errors for debugging

Why Error Handling Matters:
- Makes applications more robust and reliable
- Provides better user experience with clear error messages
- Helps developers debug issues quickly
- Prevents application crashes
- Maintains data integrity
"""

import sqlite3
from typing import Optional, Dict, Any
from utils.logger import get_logger

# Get a logger for this module
logger = get_logger(__name__)


# ============================================================================
# CUSTOM EXCEPTION CLASSES
# ============================================================================
# These custom exceptions help us provide specific, meaningful error messages
# instead of generic Python exceptions.

class BackendError(Exception):
    """
    Base exception class for all backend errors.
    
    This is the parent class for all our custom exceptions.
    By inheriting from this, we can catch all backend-specific errors
    with a single except clause if needed.
    
    Example:
        try:
            # Some backend operation
            pass
        except BackendError as e:
            # This catches ALL our custom exceptions
            print(f"Backend error: {e}")
    
    Learning Notes:
    - Creating a base exception class is a common pattern
    - It allows catching all related exceptions together
    - Helps organize exceptions into a hierarchy
    - Makes code more maintainable
    """
    pass


class ValidationError(BackendError):
    """
    Raised when input validation fails.
    
    Use this when user input doesn't meet requirements:
    - Empty required fields
    - Invalid formats (email, ISBN, etc.)
    - Out-of-range values
    - Invalid choices (status not in allowed values)
    
    Example:
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")
        
        if len(title) > 200:
            raise ValidationError("Title must be at most 200 characters")
    
    Learning Notes:
    - Validation should happen BEFORE database operations
    - Provide specific error messages that tell users what's wrong
    - Include the field name and the requirement in the message
    """
    pass


class DatabaseConnectionError(BackendError):
    """
    Raised when database connection fails.
    
    This might happen if:
    - Database file is locked by another process
    - No permission to access the database file
    - Disk is full and database file can't be created
    - Database file is corrupted
    
    Example:
        try:
            conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Cannot connect to database: {e}")
    
    Learning Notes:
    - Connection errors are usually environmental issues
    - May require system administrator intervention
    - Should be logged for troubleshooting
    - User can't usually fix these themselves
    """
    pass


class QueryExecutionError(BackendError):
    """
    Raised when a SQL query fails to execute.
    
    This might happen if:
    - SQL syntax is incorrect
    - Table or column doesn't exist
    - Database constraint is violated
    - Database is locked during write operation
    
    Example:
        try:
            cursor.execute(query, params)
        except sqlite3.Error as e:
            raise QueryExecutionError(f"Query failed: {e}")
    
    Learning Notes:
    - Query errors often indicate bugs in the code
    - Should be logged with the query for debugging
    - May need to check database schema
    - Consider if query needs to be fixed
    """
    pass


class DuplicateError(BackendError):
    """
    Raised when attempting to create a duplicate record.
    
    This happens when a UNIQUE constraint is violated:
    - Duplicate ISBN for books
    - Duplicate email for members
    - Duplicate username
    
    Example:
        try:
            execute_insert(query, params)
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise DuplicateError("A record with this value already exists")
    
    Learning Notes:
    - Duplicate errors are often user errors (not bugs)
    - User might want to update existing record instead
    - Should provide clear message about which field is duplicate
    - Consider offering to show the existing record
    """
    pass


class NotFoundError(BackendError):
    """
    Raised when a requested resource doesn't exist.
    
    Use this when:
    - Looking up a record by ID that doesn't exist
    - Searching for a record that isn't in the database
    - Trying to update or delete a non-existent record
    
    Example:
        book = Book.get_by_id(book_id)
        if not book:
            raise NotFoundError(f"Book with ID {book_id} not found")
    
    Learning Notes:
    - Not found errors are common in CRUD operations
    - Should specify what resource and which ID
    - User might have used wrong ID or record was deleted
    - Consider suggesting how to find the correct ID
    """
    pass


class ForeignKeyError(BackendError):
    """
    Raised when a foreign key constraint is violated.
    
    This happens when:
    - Trying to create a record with invalid foreign key
    - Trying to delete a record that's referenced by others
    - Referenced record doesn't exist
    
    Example:
        # Trying to create a loan for a book that doesn't exist
        try:
            execute_insert(loan_query, (book_id, member_id, due_date))
        except sqlite3.IntegrityError as e:
            if "FOREIGN KEY constraint failed" in str(e):
                raise ForeignKeyError("Referenced book or member does not exist")
    
    Learning Notes:
    - Foreign key errors indicate relationship problems
    - Need to check that referenced records exist first
    - May need to delete related records before deleting parent
    - Important for maintaining data integrity
    """
    pass


class PermissionError(BackendError):
    """
    Raised when user doesn't have permission for an operation.
    
    Use this for authorization checks:
    - User trying to delete someone else's task
    - User trying to access restricted data
    - User trying to perform admin-only operation
    
    Example:
        if task.user_id != current_user_id:
            raise PermissionError("You don't have permission to delete this task")
    
    Learning Notes:
    - Different from authentication (who you are)
    - Authorization is about what you're allowed to do
    - Important for multi-user systems
    - Should log permission violations for security monitoring
    """
    pass


# ============================================================================
# ERROR HANDLING FUNCTIONS
# ============================================================================

def handle_database_error(error: Exception, operation: str = "database operation") -> str:
    """
    Convert database errors to user-friendly messages.
    
    This function takes technical database errors and converts them
    into messages that users can understand and act on.
    
    Args:
        error: The exception that was raised
        operation: Description of what operation was being performed
    
    Returns:
        str: User-friendly error message
    
    Example:
        try:
            Book.create(title, author, isbn)
        except Exception as e:
            user_message = handle_database_error(e, "creating book")
            print(f"Error: {user_message}")
    
    Learning Notes:
    - Users don't need to see technical error details
    - Provide actionable information (what went wrong, how to fix)
    - Log the technical details for developers
    - Keep user messages simple and clear
    """
    # Log the technical error for developers
    logger.error(f"Database error during {operation}: {str(error)}", exc_info=True)
    
    # Convert to user-friendly message based on error type
    error_str = str(error).lower()
    
    if isinstance(error, sqlite3.IntegrityError):
        # Constraint violations
        if "unique constraint failed" in error_str:
            # Extract field name if possible
            if ":" in str(error):
                field = str(error).split(":")[-1].strip()
                return f"This {field} already exists. Please use a different value."
            return "This record already exists. Please use different values."
        
        elif "foreign key constraint failed" in error_str:
            return "Cannot complete operation: referenced record does not exist. Please check your input."
        
        elif "not null constraint failed" in error_str:
            # Extract field name if possible
            if ":" in str(error):
                field = str(error).split(":")[-1].strip().split(".")[-1]
                return f"The field '{field}' is required and cannot be empty."
            return "A required field is missing. Please provide all required information."
        
        elif "check constraint failed" in error_str:
            return "Invalid value provided. Please check that your input meets the requirements."
        
        else:
            return "Database constraint violation. Please check your input values."
    
    elif isinstance(error, sqlite3.OperationalError):
        # Operational errors (syntax, locked database, etc.)
        if "locked" in error_str:
            return "Database is currently busy. Please try again in a moment."
        
        elif "no such table" in error_str:
            return "Database is not properly initialized. Please run the setup script."
        
        elif "no such column" in error_str:
            return "Database schema is outdated. Please update your database."
        
        else:
            return f"Database operation failed. Please check your input and try again."
    
    elif isinstance(error, sqlite3.DatabaseError):
        # General database errors
        return "A database error occurred. Please try again or contact support."
    
    elif isinstance(error, ValidationError):
        # Our custom validation errors already have good messages
        return str(error)
    
    elif isinstance(error, DuplicateError):
        # Our custom duplicate errors already have good messages
        return str(error)
    
    elif isinstance(error, NotFoundError):
        # Our custom not found errors already have good messages
        return str(error)
    
    elif isinstance(error, ForeignKeyError):
        # Our custom foreign key errors already have good messages
        return str(error)
    
    else:
        # Unknown error type
        logger.error(f"Unexpected error type during {operation}: {type(error).__name__}")
        return "An unexpected error occurred. Please try again."


def safe_execute(operation_func, operation_name: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Safely execute an operation with comprehensive error handling.
    
    This is a wrapper function that handles all the error handling boilerplate.
    It executes a function and returns a standardized result dictionary.
    
    Args:
        operation_func: The function to execute
        operation_name: Description of the operation (for logging)
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
    
    Returns:
        Dict with keys:
        - success (bool): Whether operation succeeded
        - data (Any): Result data if successful
        - error (str): Error message if failed
        - error_type (str): Type of error if failed
    
    Example:
        def create_book(title, author, isbn):
            # ... implementation ...
            return book_id
        
        result = safe_execute(create_book, "create book", title, author, isbn)
        if result['success']:
            print(f"Book created with ID: {result['data']}")
        else:
            print(f"Error: {result['error']}")
    
    Learning Notes:
    - This pattern centralizes error handling
    - Returns consistent result format
    - Makes it easy to handle errors in calling code
    - Reduces code duplication
    """
    try:
        # Execute the operation
        logger.info(f"Starting operation: {operation_name}")
        data = operation_func(*args, **kwargs)
        logger.info(f"Operation completed successfully: {operation_name}")
        
        return {
            'success': True,
            'data': data,
            'error': None,
            'error_type': None
        }
    
    except ValidationError as e:
        # Validation errors - user input problem
        logger.warning(f"Validation error in {operation_name}: {e}")
        return {
            'success': False,
            'data': None,
            'error': str(e),
            'error_type': 'validation'
        }
    
    except DuplicateError as e:
        # Duplicate record - user trying to create existing record
        logger.warning(f"Duplicate error in {operation_name}: {e}")
        return {
            'success': False,
            'data': None,
            'error': str(e),
            'error_type': 'duplicate'
        }
    
    except NotFoundError as e:
        # Record not found - user used wrong ID
        logger.warning(f"Not found error in {operation_name}: {e}")
        return {
            'success': False,
            'data': None,
            'error': str(e),
            'error_type': 'not_found'
        }
    
    except ForeignKeyError as e:
        # Foreign key violation - referenced record doesn't exist
        logger.warning(f"Foreign key error in {operation_name}: {e}")
        return {
            'success': False,
            'data': None,
            'error': str(e),
            'error_type': 'foreign_key'
        }
    
    except (DatabaseConnectionError, QueryExecutionError) as e:
        # Database errors - technical problem
        logger.error(f"Database error in {operation_name}: {e}", exc_info=True)
        return {
            'success': False,
            'data': None,
            'error': handle_database_error(e, operation_name),
            'error_type': 'database'
        }
    
    except Exception as e:
        # Unexpected error - bug in code
        logger.exception(f"Unexpected error in {operation_name}")
        return {
            'success': False,
            'data': None,
            'error': "An unexpected error occurred. Please try again.",
            'error_type': 'unexpected'
        }


# ============================================================================
# TRY-EXCEPT PATTERN EXAMPLES
# ============================================================================

def example_basic_error_handling():
    """
    Example 1: Basic try-except pattern.
    
    This is the simplest error handling pattern.
    Use this when you want to catch and handle a specific error.
    """
    from database.connection import execute_query
    
    try:
        # Try to execute a query
        books = execute_query("SELECT * FROM books")
        print(f"Found {len(books)} books")
        
    except QueryExecutionError as e:
        # Handle query errors specifically
        print(f"Query failed: {e}")
        logger.error(f"Query execution failed: {e}")
        
    except DatabaseConnectionError as e:
        # Handle connection errors specifically
        print(f"Cannot connect to database: {e}")
        logger.error(f"Database connection failed: {e}")


def example_multiple_exceptions():
    """
    Example 2: Handling multiple exception types.
    
    Use this when different errors need different handling.
    Order matters - put more specific exceptions first!
    """
    from models.library import Book
    
    try:
        # Try to create a book
        book_id = Book.create(
            title="Python Crash Course",
            author="Eric Matthes",
            isbn="978-1593279288"
        )
        print(f"Book created with ID: {book_id}")
        
    except ValidationError as e:
        # Handle validation errors (user input problem)
        print(f"❌ Invalid input: {e}")
        print("Please check your input and try again.")
        
    except DuplicateError as e:
        # Handle duplicate errors (record already exists)
        print(f"❌ {e}")
        print("Would you like to update the existing book instead?")
        
    except DatabaseConnectionError as e:
        # Handle connection errors (technical problem)
        print(f"❌ Cannot connect to database: {e}")
        print("Please check that the database is set up correctly.")
        logger.error(f"Database connection failed: {e}")
        
    except Exception as e:
        # Catch any other unexpected errors
        print(f"❌ An unexpected error occurred")
        logger.exception("Unexpected error creating book")


def example_try_except_else_finally():
    """
    Example 3: Complete try-except-else-finally pattern.
    
    This shows all parts of exception handling:
    - try: Code that might raise an exception
    - except: Handle specific exceptions
    - else: Code to run if NO exception occurred
    - finally: Code that ALWAYS runs (cleanup)
    """
    from database.connection import execute_query
    
    connection = None
    
    try:
        # Try to execute operation
        books = execute_query("SELECT * FROM books WHERE available = ?", (True,))
        
    except QueryExecutionError as e:
        # Handle errors
        print(f"Query failed: {e}")
        logger.error(f"Query failed: {e}")
        books = []  # Return empty list on error
        
    else:
        # This runs only if NO exception occurred
        print(f"Successfully retrieved {len(books)} books")
        logger.info(f"Retrieved {len(books)} available books")
        
    finally:
        # This ALWAYS runs, even if there was an error or return statement
        # Use for cleanup (closing files, connections, etc.)
        if connection:
            connection.close()
        logger.debug("Cleanup completed")
    
    return books


def example_raising_custom_exceptions():
    """
    Example 4: Raising custom exceptions.
    
    This shows how to raise your own exceptions with meaningful messages.
    """
    def validate_book_data(title: str, author: str, isbn: str):
        """Validate book data and raise exceptions if invalid."""
        
        # Check for empty fields
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")
        
        if not author or not author.strip():
            raise ValidationError("Author cannot be empty")
        
        if not isbn or not isbn.strip():
            raise ValidationError("ISBN cannot be empty")
        
        # Check length constraints
        if len(title) > 200:
            raise ValidationError("Title must be at most 200 characters")
        
        if len(author) > 100:
            raise ValidationError("Author must be at most 100 characters")
        
        # Check ISBN format (simplified)
        isbn_clean = isbn.replace("-", "").replace(" ", "")
        if not isbn_clean.isdigit():
            raise ValidationError("ISBN must contain only digits and hyphens")
        
        if len(isbn_clean) not in [10, 13]:
            raise ValidationError("ISBN must be 10 or 13 digits")
    
    # Usage
    try:
        validate_book_data("", "Author", "123")
    except ValidationError as e:
        print(f"Validation failed: {e}")


def example_error_recovery():
    """
    Example 5: Error recovery with retry logic.
    
    This shows how to recover from errors by retrying the operation.
    Useful for temporary errors like database locks.
    """
    import time
    from database.connection import execute_query
    
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            # Try the operation
            books = execute_query("SELECT * FROM books")
            print(f"Success on attempt {attempt + 1}")
            return books
            
        except QueryExecutionError as e:
            if "locked" in str(e).lower() and attempt < max_retries - 1:
                # Database is locked, wait and retry
                print(f"Database locked, retrying in {retry_delay} seconds...")
                logger.warning(f"Database locked on attempt {attempt + 1}, retrying...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                # Not a lock error, or out of retries
                print(f"Operation failed after {attempt + 1} attempts")
                logger.error(f"Operation failed after {attempt + 1} attempts: {e}")
                raise


def example_context_manager_error_handling():
    """
    Example 6: Error handling with context managers.
    
    Context managers (with statement) automatically handle cleanup,
    even if an error occurs.
    """
    from database.connection import DatabaseConnection
    
    try:
        # The 'with' statement ensures connection is closed automatically
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            
            # Even if an error occurs here, connection will be closed
            for book in books:
                print(f"- {book['title']}")
                
    except QueryExecutionError as e:
        print(f"Query failed: {e}")
        logger.error(f"Query failed: {e}")
    
    # Connection is automatically closed here, even if there was an error


# ============================================================================
# BEST PRACTICES DOCUMENTATION
# ============================================================================

"""
ERROR HANDLING BEST PRACTICES:

1. Be Specific with Exceptions:
   ✓ Catch specific exception types
   ✗ Don't use bare 'except:' (catches everything, even KeyboardInterrupt!)
   
   Good:
       except ValidationError as e:
           handle_validation_error(e)
   
   Bad:
       except:  # Catches EVERYTHING, including system exits!
           pass

2. Provide Helpful Error Messages:
   ✓ Tell user what went wrong
   ✓ Tell user how to fix it
   ✓ Include relevant context (field name, value, etc.)
   ✗ Don't expose technical details to users
   ✗ Don't expose sensitive information
   
   Good:
       "Title cannot be empty. Please provide a book title."
   
   Bad:
       "NoneType object has no attribute 'strip'"

3. Log Errors for Debugging:
   ✓ Log technical details for developers
   ✓ Include stack traces for unexpected errors
   ✓ Log at appropriate level (ERROR for errors, WARNING for validation)
   ✗ Don't log sensitive data (passwords, credit cards)
   
   Good:
       logger.error(f"Failed to create book: {e}", exc_info=True)

4. Handle Errors at the Right Level:
   ✓ Handle errors where you can do something about them
   ✓ Let errors propagate if you can't handle them
   ✗ Don't catch and ignore errors
   ✗ Don't catch errors just to re-raise them unchanged

5. Clean Up Resources:
   ✓ Use try-finally to ensure cleanup
   ✓ Use context managers (with statement) when possible
   ✓ Close connections, files, etc. even if errors occur
   
   Good:
       try:
           conn = get_connection()
           # use connection
       finally:
           conn.close()

6. Validate Early:
   ✓ Validate input before database operations
   ✓ Fail fast with clear error messages
   ✓ Prevent invalid data from reaching database
   
   Good:
       validate_book_data(title, author, isbn)
       book_id = execute_insert(query, params)

7. Don't Swallow Exceptions:
   ✗ Don't catch exceptions and do nothing
   ✗ Don't return None or False without logging
   
   Bad:
       try:
           do_something()
       except Exception:
           pass  # Error is lost!

8. Use Custom Exceptions:
   ✓ Create meaningful exception types
   ✓ Organize exceptions in a hierarchy
   ✓ Makes error handling more precise
   
   Good:
       raise ValidationError("Title cannot be empty")
   
   Instead of:
       raise Exception("Title cannot be empty")

COMMON PATTERNS:

Pattern 1: Validate-Then-Execute
    # Validate all inputs first
    validate_title(title)
    validate_author(author)
    validate_isbn(isbn)
    
    # Then execute operation
    book_id = execute_insert(query, params)

Pattern 2: Try-Except-Log-Reraise
    try:
        result = risky_operation()
    except SomeError as e:
        logger.error(f"Operation failed: {e}", exc_info=True)
        raise  # Re-raise for caller to handle

Pattern 3: Convert-And-Handle
    try:
        result = database_operation()
    except sqlite3.IntegrityError as e:
        # Convert to our custom exception
        raise DuplicateError("Record already exists")

Pattern 4: Graceful Degradation
    try:
        data = fetch_data()
    except FetchError:
        logger.warning("Could not fetch data, using cached version")
        data = get_cached_data()

EXERCISES FOR STUDENTS:

1. Add error handling to your Todo model:
   - Wrap database operations in try-except
   - Raise ValidationError for invalid input
   - Raise NotFoundError when task doesn't exist
   - Log all errors appropriately

2. Create user-friendly error messages:
   - Test your application with invalid input
   - Ensure error messages are clear and helpful
   - Don't expose technical details to users

3. Practice different exception types:
   - Trigger a ValidationError
   - Trigger a DuplicateError
   - Trigger a NotFoundError
   - See how each is handled differently

4. Implement retry logic:
   - Add retry logic for database lock errors
   - Use exponential backoff
   - Log each retry attempt

5. Use the safe_execute wrapper:
   - Wrap your CRUD operations with safe_execute
   - Handle the returned result dictionary
   - Display appropriate messages based on error_type

NEXT STEPS:
- Review the example functions in this file
- Add error handling to your model functions
- Test error scenarios (invalid input, duplicates, etc.)
- Practice writing clear error messages
- Learn about exception hierarchies and when to create custom exceptions
"""


# If this file is run directly, show examples
if __name__ == "__main__":
    print("=== Error Handling Examples ===\n")
    
    print("Example 1: Basic error handling")
    example_basic_error_handling()
    
    print("\nExample 4: Raising custom exceptions")
    example_raising_custom_exceptions()
    
    print("\n=== Examples Complete ===")
    print("Review the code to see more patterns!")
    print("Check the logs/ directory for error logs.")

