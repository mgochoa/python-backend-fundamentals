"""
Validation Utilities

This module provides reusable validation functions that check user input
before it reaches the database. Validation is a critical part of backend
development because it:

1. Prevents invalid data from corrupting your database
2. Provides clear, helpful error messages to users
3. Catches problems early before they cause bigger issues
4. Makes your code more maintainable and testable

Key Validation Concepts:
- **Fail Fast**: Check inputs immediately and raise errors early
- **Clear Messages**: Tell users exactly what's wrong and how to fix it
- **Reusable Functions**: Write validation once, use it everywhere
- **Separation of Concerns**: Keep validation logic separate from business logic

Common Validation Patterns:
- Required fields (not empty)
- Length constraints (min/max characters)
- Format validation (email, phone, ISBN)
- Choice validation (must be one of allowed values)
- Range validation (numbers within bounds)

Example Usage:
    from validation.validators import validate_not_empty, validate_email
    
    # Validate user input before creating a record
    validate_not_empty(username, "Username")
    validate_email(email)
    
    # If validation passes, proceed with database operation
    user_id = create_user(username, email)
"""

import re
from typing import List


# Custom exception for validation errors
# This makes it easy to catch validation-specific errors separately from other errors
class ValidationError(Exception):
    """
    Raised when input validation fails.
    
    This exception should include a clear, user-friendly message explaining
    what validation rule was violated and how to fix it.
    
    Example:
        raise ValidationError("Email cannot be empty")
        raise ValidationError("Password must be at least 8 characters")
    """
    pass


def validate_not_empty(value: str, field_name: str) -> None:
    """
    Validate that a string is not empty or only whitespace.
    
    This is one of the most common validations - ensuring required fields
    actually have content. We check both for None/empty strings and for
    strings that only contain whitespace (spaces, tabs, newlines).
    
    Args:
        value: The string to validate
        field_name: Name of the field (used in error message)
    
    Raises:
        ValidationError: If value is None, empty, or only whitespace
    
    Example:
        validate_not_empty("John", "Name")  # Passes
        validate_not_empty("", "Name")      # Raises ValidationError
        validate_not_empty("   ", "Name")   # Raises ValidationError (only spaces)
        validate_not_empty(None, "Name")    # Raises ValidationError
    
    Learning Notes:
        - The 'strip()' method removes leading/trailing whitespace
        - We use 'not value' to check for None or empty string
        - We use 'not value.strip()' to catch whitespace-only strings
        - Clear error messages help users understand what went wrong
    """
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")


def validate_length(value: str, field_name: str, min_len: int = None, max_len: int = None) -> None:
    """
    Validate that a string meets length constraints.
    
    Length validation is important for:
    - Database column size limits (e.g., VARCHAR(100))
    - User experience (titles shouldn't be too long)
    - Security (prevent extremely long inputs)
    - Business rules (ISBN must be exactly 10 or 13 digits)
    
    Args:
        value: The string to validate
        field_name: Name of the field (used in error message)
        min_len: Minimum allowed length (optional)
        max_len: Maximum allowed length (optional)
    
    Raises:
        ValidationError: If value is shorter than min_len or longer than max_len
    
    Example:
        validate_length("Hello", "Title", min_len=3, max_len=100)  # Passes
        validate_length("Hi", "Title", min_len=3)                  # Raises ValidationError
        validate_length("A" * 200, "Title", max_len=100)           # Raises ValidationError
        validate_length("Test", "Name", min_len=5, max_len=10)     # Raises ValidationError
    
    Learning Notes:
        - Optional parameters (min_len, max_len) make this function flexible
        - We check 'if min_len' to see if a minimum was specified
        - The len() function returns the number of characters in a string
        - We can validate just minimum, just maximum, or both
    """
    if min_len is not None and len(value) < min_len:
        raise ValidationError(f"{field_name} must be at least {min_len} characters")
    
    if max_len is not None and len(value) > max_len:
        raise ValidationError(f"{field_name} must be at most {max_len} characters")


def validate_choice(value: str, field_name: str, allowed_values: List[str]) -> None:
    """
    Validate that a value is one of the allowed choices.
    
    This is useful for enum-like fields where only specific values are valid,
    such as:
    - Status fields: 'pending', 'in_progress', 'completed'
    - Priority levels: 'low', 'medium', 'high'
    - User roles: 'admin', 'user', 'guest'
    
    This validation prevents typos and ensures data consistency.
    
    Args:
        value: The value to validate
        field_name: Name of the field (used in error message)
        allowed_values: List of valid choices
    
    Raises:
        ValidationError: If value is not in allowed_values
    
    Example:
        validate_choice("pending", "Status", ["pending", "completed"])  # Passes
        validate_choice("done", "Status", ["pending", "completed"])     # Raises ValidationError
        validate_choice("high", "Priority", ["low", "medium", "high"])  # Passes
    
    Learning Notes:
        - The 'in' operator checks if a value exists in a list
        - We use ', '.join() to create a readable list in the error message
        - This pattern is better than using if/elif chains for multiple values
        - Consider using Python's Enum class for more complex scenarios
    """
    if value not in allowed_values:
        raise ValidationError(
            f"{field_name} must be one of: {', '.join(allowed_values)}"
        )


def validate_email(email: str) -> None:
    """
    Validate email format using a regular expression.
    
    Email validation is a common requirement in web applications. This function
    uses a regex pattern to check for basic email format:
    - username part (letters, numbers, dots, underscores, etc.)
    - @ symbol
    - domain name
    - top-level domain (.com, .org, etc.)
    
    Note: This is a simplified validation. Real-world email validation is
    complex, and the only way to truly validate an email is to send a
    confirmation message to it.
    
    Args:
        email: The email address to validate
    
    Raises:
        ValidationError: If email format is invalid
    
    Example:
        validate_email("user@example.com")      # Passes
        validate_email("test.user@domain.org")  # Passes
        validate_email("invalid.email")         # Raises ValidationError
        validate_email("@example.com")          # Raises ValidationError
        validate_email("user@")                 # Raises ValidationError
    
    Learning Notes:
        - Regular expressions (regex) are patterns for matching text
        - The 're' module provides regex functionality in Python
        - ^ means "start of string", $ means "end of string"
        - [a-zA-Z0-9._%+-]+ matches one or more allowed characters
        - The pattern is simplified for learning purposes
        - In production, consider using a library like 'email-validator'
    
    Regex Pattern Breakdown:
        ^                   Start of string
        [a-zA-Z0-9._%+-]+   Username: letters, numbers, and special chars
        @                   Literal @ symbol
        [a-zA-Z0-9.-]+      Domain: letters, numbers, dots, hyphens
        \\.                 Literal dot (escaped)
        [a-zA-Z]{2,}        TLD: at least 2 letters (.com, .org, etc.)
        $                   End of string
    """
    # Define the email pattern
    # This is a simplified pattern for educational purposes
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use re.match() to check if the email matches the pattern
    # re.match() returns a match object if successful, None if not
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")


def validate_isbn(isbn: str) -> None:
    """
    Validate ISBN (International Standard Book Number) format.
    
    ISBNs come in two formats:
    - ISBN-10: 10 digits (older format)
    - ISBN-13: 13 digits (current standard)
    
    ISBNs may include hyphens or spaces for readability (e.g., 978-0-123-45678-9),
    but we remove these for validation.
    
    This function validates the format and length. The checksum validation
    (verifying the last digit is correct) is left as a TODO for students
    to implement as an advanced exercise.
    
    Args:
        isbn: The ISBN to validate
    
    Raises:
        ValidationError: If ISBN format is invalid
    
    Example:
        validate_isbn("1234567890")           # Passes (10 digits)
        validate_isbn("978-0-123-45678-9")    # Passes (13 digits with hyphens)
        validate_isbn("123456789")            # Raises ValidationError (too short)
        validate_isbn("12345678901234")       # Raises ValidationError (too long)
        validate_isbn("123-456-789X")         # Raises ValidationError (contains letter)
    
    Learning Notes:
        - The replace() method removes characters from a string
        - We chain multiple replace() calls to remove both hyphens and spaces
        - The isdigit() method checks if all characters are digits
        - ISBNs have a checksum digit for error detection (advanced topic)
    
    TODO for Students (Advanced Exercise):
        Implement checksum validation for ISBN-10 and ISBN-13:
        
        ISBN-10 Checksum:
        - Multiply each of the first 9 digits by its position (1-9)
        - Sum all products
        - The 10th digit should make the sum divisible by 11
        - The 10th digit can be 'X' representing 10
        
        ISBN-13 Checksum:
        - Multiply digits alternately by 1 and 3
        - Sum all products
        - The 13th digit should make the sum divisible by 10
        
        Resources:
        - https://en.wikipedia.org/wiki/ISBN#ISBN-10_check_digits
        - https://en.wikipedia.org/wiki/ISBN#ISBN-13_check_digit_calculation
    """
    # Remove hyphens and spaces that are often used for readability
    # Example: "978-0-123-45678-9" becomes "9780123456789"
    cleaned_isbn = isbn.replace('-', '').replace(' ', '')
    
    # Check if the length is valid (10 or 13 digits)
    if len(cleaned_isbn) not in [10, 13]:
        raise ValidationError("ISBN must be 10 or 13 digits")
    
    # Check if all characters are digits
    # Note: ISBN-10 can end with 'X', but we're keeping this simple for now
    if not cleaned_isbn.isdigit():
        raise ValidationError("ISBN must contain only digits")
    
    # TODO: Add checksum validation
    # This is an advanced exercise for students who want to learn more
    # about validation algorithms and mathematical checks
    # 
    # Hints:
    # - For ISBN-10: sum = (d1*1 + d2*2 + ... + d9*9) % 11 should equal d10
    # - For ISBN-13: sum = (d1*1 + d2*3 + d3*1 + ... + d13*1) % 10 should equal 0
    # - You'll need to convert string digits to integers: int(digit)
    # - Consider writing separate functions: _validate_isbn10_checksum() and _validate_isbn13_checksum()


# Additional validation functions students might implement:
#
# def validate_positive_number(value: float, field_name: str) -> None:
#     """Validate that a number is positive (> 0)."""
#     pass
#
# def validate_non_negative(value: int, field_name: str) -> None:
#     """Validate that a number is non-negative (>= 0)."""
#     pass
#
# def validate_date_format(date_str: str, field_name: str) -> None:
#     """Validate that a string matches YYYY-MM-DD format."""
#     pass
#
# def validate_phone_number(phone: str) -> None:
#     """Validate phone number format."""
#     pass
#
# def validate_url(url: str) -> None:
#     """Validate URL format."""
#     pass
