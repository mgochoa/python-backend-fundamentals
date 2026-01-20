"""
Validation Package

This package contains validation utilities and exercises:
- validators.py: Example validation functions for common patterns
- exercises/: Validation exercises for students to complete

Students will learn about:
- Input validation and data integrity
- Writing reusable validation functions
- Providing clear error messages
- Validating before database operations

Validation is crucial for:
- Preventing invalid data from entering the database
- Providing helpful feedback to users
- Maintaining data quality and consistency
"""

# Import validation functions for easy access
from validation.validators import (
    ValidationError,
    validate_not_empty,
    validate_length,
    validate_choice,
    validate_email,
    validate_isbn
)

__all__ = [
    'ValidationError',
    'validate_not_empty',
    'validate_length',
    'validate_choice',
    'validate_email',
    'validate_isbn'
]

