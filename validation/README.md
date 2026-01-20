# Validation Module

This module provides reusable validation functions for the Python Backend Learning Project.

## Overview

Validation is a critical part of backend development. It ensures that:
- Invalid data never reaches your database
- Users receive clear, helpful error messages
- Data integrity is maintained
- Security vulnerabilities (like SQL injection) are prevented

## Files in This Module

### `validators.py`
Contains example validation functions that demonstrate common validation patterns:

- **`validate_not_empty(value, field_name)`** - Ensures required fields have content
- **`validate_length(value, field_name, min_len, max_len)`** - Checks string length constraints
- **`validate_choice(value, field_name, allowed_values)`** - Validates enum-like fields
- **`validate_email(email)`** - Validates email format using regex
- **`validate_isbn(isbn)`** - Validates ISBN format (10 or 13 digits)

### `demo_validators.py`
A demonstration script showing how to use validation functions in real scenarios. Run it with:
```bash
python validation/demo_validators.py
```

### `exercises/` (Coming Soon)
Will contain validation exercises for students to practice implementing their own validators.

## Usage Examples

### Basic Validation

```python
from validation import validate_not_empty, validate_email, ValidationError

try:
    # Validate user input
    validate_not_empty(username, "Username")
    validate_email(email)
    
    # If validation passes, proceed with database operation
    user_id = create_user(username, email)
    print(f"✓ User created with ID: {user_id}")
    
except ValidationError as e:
    print(f"✗ Validation failed: {e}")
```

### Validating Before Database Operations

```python
from validation import validate_not_empty, validate_isbn, ValidationError

def create_book(title: str, author: str, isbn: str) -> int:
    """Create a new book with validation."""
    
    # Step 1: Validate ALL inputs first
    try:
        validate_not_empty(title, "Title")
        validate_not_empty(author, "Author")
        validate_isbn(isbn)
    except ValidationError as e:
        # Validation failed - don't proceed to database
        raise e
    
    # Step 2: Only execute database operation if validation passed
    query = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)"
    cursor.execute(query, (title, author, isbn))
    return cursor.lastrowid
```

### Enum-like Validation

```python
from validation import validate_choice, ValidationError

def update_task_status(task_id: int, new_status: str) -> bool:
    """Update task status with validation."""
    
    # Validate status is one of allowed values
    allowed_statuses = ["pending", "in_progress", "completed"]
    validate_choice(new_status, "Status", allowed_statuses)
    
    # Proceed with update
    query = "UPDATE tasks SET status = ? WHERE id = ?"
    cursor.execute(query, (new_status, task_id))
    return cursor.rowcount > 0
```

## Key Concepts

### 1. Fail Fast
Validate inputs immediately and raise errors early, before any database operations.

### 2. Clear Error Messages
Error messages should tell users:
- What field failed validation
- Why it failed
- How to fix it (when possible)

**Good:** "Email cannot be empty"
**Bad:** "Invalid input"

### 3. Reusable Functions
Write validation logic once, use it everywhere. This makes your code:
- More maintainable
- More consistent
- Easier to test

### 4. Separation of Concerns
Keep validation logic separate from business logic. This makes code:
- Easier to understand
- Easier to modify
- More testable

## Learning Path

1. **Study** the validation functions in `validators.py`
   - Read the docstrings and comments
   - Understand what each function validates
   - Note the error messages

2. **Run** the demo script
   ```bash
   python validation/demo_validators.py
   ```
   - See validation in action
   - Observe how errors are caught
   - Notice the clear error messages

3. **Practice** using validators in your own code
   - Import validators into your models
   - Add validation before database operations
   - Test with both valid and invalid inputs

4. **Implement** your own validators (exercises coming soon)
   - Create validators for the Todo system
   - Write validators for the Inventory system
   - Add custom validation logic

## Common Validation Patterns

### Required Fields
```python
validate_not_empty(value, "FieldName")
```

### Length Constraints
```python
validate_length(value, "FieldName", min_len=3, max_len=100)
```

### Enum Values
```python
validate_choice(value, "FieldName", ["option1", "option2", "option3"])
```

### Format Validation
```python
validate_email(email)
validate_isbn(isbn)
```

### Custom Validation
```python
def validate_positive_number(value: float, field_name: str) -> None:
    """Validate that a number is positive."""
    if value <= 0:
        raise ValidationError(f"{field_name} must be positive")
```

## Testing Your Validators

Always test validators with:
1. **Valid inputs** - Should pass without errors
2. **Invalid inputs** - Should raise ValidationError
3. **Edge cases** - Empty strings, whitespace, boundary values

Example test:
```python
# Test valid input
try:
    validate_not_empty("Hello", "Test")
    print("✓ Valid input passed")
except ValidationError:
    print("✗ Should not have failed")

# Test invalid input
try:
    validate_not_empty("", "Test")
    print("✗ Should have failed")
except ValidationError as e:
    print(f"✓ Invalid input caught: {e}")
```

## Next Steps

- Complete the validation exercises in `exercises/`
- Add validation to your Todo system implementation
- Create custom validators for the Inventory system
- Implement the ISBN checksum validation (advanced)

## Resources

- [Python Regular Expressions](https://docs.python.org/3/library/re.html)
- [ISBN Validation Algorithm](https://en.wikipedia.org/wiki/ISBN#Check_digits)
- [Data Validation Best Practices](https://owasp.org/www-project-proactive-controls/v3/en/c5-validate-inputs)
