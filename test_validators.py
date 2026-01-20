"""
Test script for validation functions.

This script tests the validation functions to ensure they work correctly.
"""

from validation.validators import (
    ValidationError,
    validate_not_empty,
    validate_length,
    validate_choice,
    validate_email,
    validate_isbn
)


def test_validate_not_empty():
    """Test validate_not_empty function."""
    print("Testing validate_not_empty...")
    
    # Should pass
    try:
        validate_not_empty("Hello", "Test")
        print("  ✓ Valid non-empty string passes")
    except ValidationError as e:
        print(f"  ✗ Unexpected error: {e}")
    
    # Should fail - empty string
    try:
        validate_not_empty("", "Test")
        print("  ✗ Empty string should fail")
    except ValidationError as e:
        print(f"  ✓ Empty string fails correctly: {e}")
    
    # Should fail - whitespace only
    try:
        validate_not_empty("   ", "Test")
        print("  ✗ Whitespace-only string should fail")
    except ValidationError as e:
        print(f"  ✓ Whitespace-only string fails correctly: {e}")


def test_validate_length():
    """Test validate_length function."""
    print("\nTesting validate_length...")
    
    # Should pass
    try:
        validate_length("Hello", "Test", min_len=3, max_len=10)
        print("  ✓ Valid length passes")
    except ValidationError as e:
        print(f"  ✗ Unexpected error: {e}")
    
    # Should fail - too short
    try:
        validate_length("Hi", "Test", min_len=3)
        print("  ✗ Too short string should fail")
    except ValidationError as e:
        print(f"  ✓ Too short string fails correctly: {e}")
    
    # Should fail - too long
    try:
        validate_length("A" * 200, "Test", max_len=100)
        print("  ✗ Too long string should fail")
    except ValidationError as e:
        print(f"  ✓ Too long string fails correctly: {e}")


def test_validate_choice():
    """Test validate_choice function."""
    print("\nTesting validate_choice...")
    
    # Should pass
    try:
        validate_choice("pending", "Status", ["pending", "completed"])
        print("  ✓ Valid choice passes")
    except ValidationError as e:
        print(f"  ✗ Unexpected error: {e}")
    
    # Should fail - invalid choice
    try:
        validate_choice("done", "Status", ["pending", "completed"])
        print("  ✗ Invalid choice should fail")
    except ValidationError as e:
        print(f"  ✓ Invalid choice fails correctly: {e}")


def test_validate_email():
    """Test validate_email function."""
    print("\nTesting validate_email...")
    
    # Should pass
    valid_emails = [
        "user@example.com",
        "test.user@domain.org",
        "name+tag@company.co.uk"
    ]
    for email in valid_emails:
        try:
            validate_email(email)
            print(f"  ✓ Valid email passes: {email}")
        except ValidationError as e:
            print(f"  ✗ Unexpected error for {email}: {e}")
    
    # Should fail
    invalid_emails = [
        "invalid.email",
        "@example.com",
        "user@",
        "user@domain",
        "user domain@example.com"
    ]
    for email in invalid_emails:
        try:
            validate_email(email)
            print(f"  ✗ Invalid email should fail: {email}")
        except ValidationError as e:
            print(f"  ✓ Invalid email fails correctly: {email}")


def test_validate_isbn():
    """Test validate_isbn function."""
    print("\nTesting validate_isbn...")
    
    # Should pass
    valid_isbns = [
        "1234567890",           # 10 digits
        "1234567890123",        # 13 digits
        "978-0-123-45678-9",    # 13 digits with hyphens
        "1-234-56789-0"         # 10 digits with hyphens
    ]
    for isbn in valid_isbns:
        try:
            validate_isbn(isbn)
            print(f"  ✓ Valid ISBN passes: {isbn}")
        except ValidationError as e:
            print(f"  ✗ Unexpected error for {isbn}: {e}")
    
    # Should fail
    invalid_isbns = [
        "123456789",            # Too short
        "12345678901234",       # Too long
        "123-456-789X",         # Contains letter (simplified validation)
        "12345 67890 12"        # Wrong length after cleaning
    ]
    for isbn in invalid_isbns:
        try:
            validate_isbn(isbn)
            print(f"  ✗ Invalid ISBN should fail: {isbn}")
        except ValidationError as e:
            print(f"  ✓ Invalid ISBN fails correctly: {isbn}")


if __name__ == "__main__":
    print("=" * 60)
    print("Validation Functions Test Suite")
    print("=" * 60)
    
    test_validate_not_empty()
    test_validate_length()
    test_validate_choice()
    test_validate_email()
    test_validate_isbn()
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)
