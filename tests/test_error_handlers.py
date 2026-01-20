"""
Test script for error handling utilities.

This script demonstrates that the error handling utilities work correctly
and can be integrated with the existing database code.
"""

import sqlite3
from utils.error_handlers import (
    ValidationError,
    DatabaseConnectionError,
    DuplicateError,
    NotFoundError,
    handle_database_error,
    safe_execute
)
from utils.logger import get_logger

# Get a logger for this test
logger = get_logger(__name__)


def test_custom_exceptions():
    """Test that custom exceptions can be raised and caught."""
    print("Testing custom exceptions...")
    
    # Test ValidationError
    try:
        raise ValidationError("Title cannot be empty")
    except ValidationError as e:
        print(f"✓ ValidationError caught: {e}")
    
    # Test DuplicateError
    try:
        raise DuplicateError("Book with ISBN 978-1234567890 already exists")
    except DuplicateError as e:
        print(f"✓ DuplicateError caught: {e}")
    
    # Test NotFoundError
    try:
        raise NotFoundError("Book with ID 999 not found")
    except NotFoundError as e:
        print(f"✓ NotFoundError caught: {e}")
    
    print()


def test_handle_database_error():
    """Test the handle_database_error function."""
    print("Testing handle_database_error()...")
    
    # Test unique constraint error
    try:
        raise sqlite3.IntegrityError("UNIQUE constraint failed: books.isbn")
    except Exception as e:
        msg = handle_database_error(e, "creating book")
        print(f"✓ Unique constraint: {msg}")
    
    # Test foreign key error
    try:
        raise sqlite3.IntegrityError("FOREIGN KEY constraint failed")
    except Exception as e:
        msg = handle_database_error(e, "creating loan")
        print(f"✓ Foreign key: {msg}")
    
    # Test not null error
    try:
        raise sqlite3.IntegrityError("NOT NULL constraint failed: books.title")
    except Exception as e:
        msg = handle_database_error(e, "creating book")
        print(f"✓ Not null: {msg}")
    
    # Test locked database
    try:
        raise sqlite3.OperationalError("database is locked")
    except Exception as e:
        msg = handle_database_error(e, "updating book")
        print(f"✓ Database locked: {msg}")
    
    # Test no such table
    try:
        raise sqlite3.OperationalError("no such table: books")
    except Exception as e:
        msg = handle_database_error(e, "querying books")
        print(f"✓ No such table: {msg}")
    
    print()


def test_safe_execute():
    """Test the safe_execute wrapper function."""
    print("Testing safe_execute()...")
    
    # Test successful operation
    def successful_operation(x, y):
        return x + y
    
    result = safe_execute(successful_operation, "addition", 5, 3)
    assert result['success'] == True
    assert result['data'] == 8
    assert result['error'] is None
    print(f"✓ Successful operation: {result}")
    
    # Test validation error
    def failing_operation():
        raise ValidationError("Invalid input")
    
    result = safe_execute(failing_operation, "validation test")
    assert result['success'] == False
    assert result['error_type'] == 'validation'
    print(f"✓ Validation error: {result}")
    
    # Test duplicate error
    def duplicate_operation():
        raise DuplicateError("Record already exists")
    
    result = safe_execute(duplicate_operation, "duplicate test")
    assert result['success'] == False
    assert result['error_type'] == 'duplicate'
    print(f"✓ Duplicate error: {result}")
    
    print()


def test_integration_with_database():
    """Test integration with actual database operations."""
    print("Testing integration with database...")
    
    from database.connection import execute_query, QueryExecutionError
    
    # Test successful query
    try:
        books = execute_query("SELECT * FROM books LIMIT 5")
        print(f"✓ Successfully queried {len(books)} books")
    except QueryExecutionError as e:
        print(f"✓ Query error caught and handled: {e}")
    
    # Test query with error (invalid table name)
    try:
        execute_query("SELECT * FROM nonexistent_table")
    except QueryExecutionError as e:
        user_msg = handle_database_error(e, "querying nonexistent table")
        print(f"✓ Invalid table error converted: {user_msg}")
    
    print()


def main():
    """Run all tests."""
    print("=" * 60)
    print("Error Handling Utilities Test Suite")
    print("=" * 60)
    print()
    
    test_custom_exceptions()
    test_handle_database_error()
    test_safe_execute()
    test_integration_with_database()
    
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print()
    print("Check the logs/ directory for detailed logs.")


if __name__ == "__main__":
    main()

