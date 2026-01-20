"""
Validation Demo Script

This script demonstrates how to use the validation functions in a real scenario.
It shows how validation helps catch errors before they reach the database.

Run this script to see validation in action:
    python validation/demo_validators.py
"""

from validators import (
    ValidationError,
    validate_not_empty,
    validate_length,
    validate_choice,
    validate_email,
    validate_isbn
)


def create_book_example():
    """
    Example: Creating a book with validation.
    
    This shows how validation functions are used before database operations.
    """
    print("\n" + "=" * 60)
    print("Example 1: Creating a Book with Validation")
    print("=" * 60)
    
    # Example 1: Valid book data
    print("\n--- Attempt 1: Valid book data ---")
    try:
        title = "Python Crash Course"
        author = "Eric Matthes"
        isbn = "978-1593279288"
        
        # Validate all fields before creating the book
        validate_not_empty(title, "Title")
        validate_not_empty(author, "Author")
        validate_isbn(isbn)
        
        print(f"✓ All validations passed!")
        print(f"  Title: {title}")
        print(f"  Author: {author}")
        print(f"  ISBN: {isbn}")
        print("  → Book would be created in database")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
    
    # Example 2: Invalid book data (empty title)
    print("\n--- Attempt 2: Empty title ---")
    try:
        title = ""
        author = "Eric Matthes"
        isbn = "978-1593279288"
        
        validate_not_empty(title, "Title")
        validate_not_empty(author, "Author")
        validate_isbn(isbn)
        
        print("✓ All validations passed!")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
        print("  → Book was NOT created (validation caught the error)")
    
    # Example 3: Invalid ISBN
    print("\n--- Attempt 3: Invalid ISBN ---")
    try:
        title = "Python Crash Course"
        author = "Eric Matthes"
        isbn = "123"  # Too short
        
        validate_not_empty(title, "Title")
        validate_not_empty(author, "Author")
        validate_isbn(isbn)
        
        print("✓ All validations passed!")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
        print("  → Book was NOT created (validation caught the error)")


def create_task_example():
    """
    Example: Creating a task with validation.
    
    This shows validation for enum-like fields (status, priority).
    """
    print("\n" + "=" * 60)
    print("Example 2: Creating a Task with Validation")
    print("=" * 60)
    
    # Example 1: Valid task data
    print("\n--- Attempt 1: Valid task data ---")
    try:
        title = "Complete Python tutorial"
        status = "pending"
        priority = "high"
        
        # Validate all fields
        validate_not_empty(title, "Title")
        validate_length(title, "Title", min_len=1, max_len=200)
        validate_choice(status, "Status", ["pending", "in_progress", "completed"])
        validate_choice(priority, "Priority", ["low", "medium", "high"])
        
        print(f"✓ All validations passed!")
        print(f"  Title: {title}")
        print(f"  Status: {status}")
        print(f"  Priority: {priority}")
        print("  → Task would be created in database")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
    
    # Example 2: Invalid status
    print("\n--- Attempt 2: Invalid status ---")
    try:
        title = "Complete Python tutorial"
        status = "done"  # Not in allowed values
        priority = "high"
        
        validate_not_empty(title, "Title")
        validate_length(title, "Title", min_len=1, max_len=200)
        validate_choice(status, "Status", ["pending", "in_progress", "completed"])
        validate_choice(priority, "Priority", ["low", "medium", "high"])
        
        print("✓ All validations passed!")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
        print("  → Task was NOT created (validation caught the error)")
    
    # Example 3: Title too long
    print("\n--- Attempt 3: Title too long ---")
    try:
        title = "A" * 250  # Exceeds max length
        status = "pending"
        priority = "high"
        
        validate_not_empty(title, "Title")
        validate_length(title, "Title", min_len=1, max_len=200)
        validate_choice(status, "Status", ["pending", "in_progress", "completed"])
        validate_choice(priority, "Priority", ["low", "medium", "high"])
        
        print("✓ All validations passed!")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
        print("  → Task was NOT created (validation caught the error)")


def create_member_example():
    """
    Example: Creating a library member with email validation.
    
    This shows format validation using regex.
    """
    print("\n" + "=" * 60)
    print("Example 3: Creating a Library Member with Email Validation")
    print("=" * 60)
    
    # Example 1: Valid member data
    print("\n--- Attempt 1: Valid member data ---")
    try:
        name = "John Doe"
        email = "john.doe@example.com"
        
        validate_not_empty(name, "Name")
        validate_email(email)
        
        print(f"✓ All validations passed!")
        print(f"  Name: {name}")
        print(f"  Email: {email}")
        print("  → Member would be created in database")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
    
    # Example 2: Invalid email format
    print("\n--- Attempt 2: Invalid email format ---")
    try:
        name = "Jane Smith"
        email = "jane.smith@invalid"  # Missing TLD
        
        validate_not_empty(name, "Name")
        validate_email(email)
        
        print("✓ All validations passed!")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
        print("  → Member was NOT created (validation caught the error)")
    
    # Example 3: Another invalid email
    print("\n--- Attempt 3: Email without @ symbol ---")
    try:
        name = "Bob Johnson"
        email = "bob.johnson.example.com"  # Missing @
        
        validate_not_empty(name, "Name")
        validate_email(email)
        
        print("✓ All validations passed!")
        
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
        print("  → Member was NOT created (validation caught the error)")


def main():
    """Run all validation examples."""
    print("\n" + "=" * 60)
    print("VALIDATION DEMONSTRATION")
    print("=" * 60)
    print("\nThis demo shows how validation functions catch errors")
    print("BEFORE they reach the database, preventing data corruption")
    print("and providing clear error messages to users.")
    
    create_book_example()
    create_task_example()
    create_member_example()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. Always validate input BEFORE database operations")
    print("2. Use clear, specific error messages")
    print("3. Reusable validation functions make code cleaner")
    print("4. Validation prevents bad data from corrupting your database")
    print("5. Failed validation should stop the operation immediately")
    print("\n")


if __name__ == "__main__":
    main()
