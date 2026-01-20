"""
Todo System Validation - Complete Solution

This is the COMPLETE SOLUTION for the Todo validation exercises.
Students should attempt to implement validation/exercises/todo_validators.py
themselves before looking at this solution.

This solution demonstrates:
- Using existing validation utilities from validators.py
- Implementing enum-like validation with validate_choice()
- Composing multiple validation checks
- Writing clear, reusable validation functions
- Proper error handling and messaging

Learning Value:
- Compare your implementation to this solution
- Understand how to reuse validation utilities
- Learn patterns for composing validations
- See how validation integrates with models

Requirements Addressed:
- Requirement 8.3: Complete validation implementation for reference
- Requirement 5.1: Example validation functions
- Requirement 5.4: Clear error messages

IMPORTANT: Run this file from the project root directory:
    python exercises/solutions/todo_validators_complete.py

Or run the tests using:
    python -c "from exercises.solutions.todo_validators_complete import run_tests; run_tests()"
"""

# Import the validation utilities we need
# Note: These imports assume you're running from the project root directory
try:
    from validation.validators import (
        validate_not_empty,
        validate_length,
        validate_choice,
        ValidationError
    )
except ModuleNotFoundError:
    # If running from a different directory, try adding parent directories to path
    import sys
    import os
    # Add project root to path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from validation.validators import (
        validate_not_empty,
        validate_length,
        validate_choice,
        ValidationError
    )


# ============================================================================
# Task Field Validation Functions
# ============================================================================

def validate_task_title(title: str) -> None:
    """
    Validate that a task title meets all requirements.
    
    SOLUTION: This demonstrates composing multiple validation checks.
    
    A valid task title must:
    - Not be empty or only whitespace
    - Be between 1 and 200 characters long
    
    Args:
        title: The task title to validate
    
    Raises:
        ValidationError: If title validation fails
    
    Example Usage:
        validate_task_title("Complete Python tutorial")  # Passes
        validate_task_title("")                          # Raises ValidationError
        validate_task_title("A" * 250)                   # Raises ValidationError
    
    Implementation Notes:
    - We call validate_not_empty() first to catch empty strings
    - Then we call validate_length() to check the length constraints
    - If either validation fails, ValidationError is raised automatically
    - We don't need to catch and re-raise - let the errors propagate
    - The error messages from the utility functions are already clear
    """
    # Check that title is not empty or whitespace-only
    # This will raise ValidationError with message: "Title cannot be empty"
    validate_not_empty(title, "Title")
    
    # Check that title length is within acceptable range
    # This will raise ValidationError if too short or too long
    validate_length(title, "Title", min_len=1, max_len=200)


def validate_task_status(status: str) -> None:
    """
    Validate that a task status is one of the allowed values.
    
    SOLUTION: This demonstrates enum-like validation using validate_choice().
    
    A valid task status must be one of:
    - 'pending': Task has not been started yet
    - 'in_progress': Task is currently being worked on
    - 'completed': Task has been finished
    
    Args:
        status: The task status to validate
    
    Raises:
        ValidationError: If status is not one of the allowed values
    
    Example Usage:
        validate_task_status("pending")      # Passes
        validate_task_status("in_progress")  # Passes
        validate_task_status("completed")    # Passes
        validate_task_status("done")         # Raises ValidationError
        validate_task_status("PENDING")      # Raises ValidationError (case-sensitive)
    
    Implementation Notes:
    - We define the allowed values as a list
    - We use validate_choice() to check if status is in the list
    - The validation is case-sensitive (by design)
    - The error message will show all allowed values
    - This pattern works for any enum-like field
    """
    # Define the allowed status values
    allowed_statuses = ["pending", "in_progress", "completed"]
    
    # Use validate_choice() to check if status is in the allowed list
    # This will raise ValidationError with a message like:
    # "Status must be one of: pending, in_progress, completed"
    validate_choice(status, "Status", allowed_statuses)


def validate_task_priority(priority: str) -> None:
    """
    Validate that a task priority is one of the allowed values.
    
    SOLUTION: This follows the same pattern as validate_task_status().
    
    A valid task priority must be one of:
    - 'low': Task is not urgent, can be done later
    - 'medium': Task has normal priority
    - 'high': Task is urgent and should be done soon
    
    Args:
        priority: The task priority to validate
    
    Raises:
        ValidationError: If priority is not one of the allowed values
    
    Example Usage:
        validate_task_priority("low")      # Passes
        validate_task_priority("medium")   # Passes
        validate_task_priority("high")     # Passes
        validate_task_priority("urgent")   # Raises ValidationError
        validate_task_priority("LOW")      # Raises ValidationError (case-sensitive)
    
    Implementation Notes:
    - This is almost identical to validate_task_status()
    - The only differences are the field name and allowed values
    - This shows how validation patterns are reusable
    - Consider creating a helper function if you have many enum fields
    """
    # Define the allowed priority values
    allowed_priorities = ["low", "medium", "high"]
    
    # Use validate_choice() to check if priority is in the allowed list
    # This will raise ValidationError with a message like:
    # "Priority must be one of: low, medium, high"
    validate_choice(priority, "Priority", allowed_priorities)


# ============================================================================
# BONUS EXERCISES - Complete Solutions
# ============================================================================

def validate_task_description(description: str) -> None:
    """
    Validate that a task description meets requirements.
    
    BONUS SOLUTION: This shows how to handle optional fields.
    
    A valid task description:
    - Can be empty (description is optional)
    - If provided, must not exceed 1000 characters
    
    Args:
        description: The task description to validate (can be empty)
    
    Raises:
        ValidationError: If description exceeds maximum length
    
    Implementation Notes:
    - We only validate if description is not empty
    - We use validate_length() with only max_len parameter
    - We don't use min_len because empty descriptions are allowed
    - This pattern works for any optional field with constraints
    """
    # Only validate length if description is provided and not empty
    # Empty strings and None are allowed for optional fields
    if description and description.strip():
        # Check maximum length only (no minimum for optional fields)
        validate_length(description, "Description", max_len=1000)


def validate_complete_task(
    title: str,
    status: str,
    priority: str,
    description: str = None
) -> None:
    """
    Validate all task fields at once.
    
    BONUS SOLUTION: This demonstrates composing multiple validation functions.
    
    This function validates an entire task object before creating or updating it.
    It's useful when you want to validate everything upfront and get all
    validation errors at once (though this simple version stops at first error).
    
    Args:
        title: Task title
        status: Task status
        priority: Task priority
        description: Task description (optional)
    
    Raises:
        ValidationError: If any field validation fails
    
    Example Usage:
        # Validate a complete task
        validate_complete_task(
            title="Buy groceries",
            status="pending",
            priority="medium",
            description="Get milk, eggs, and bread"
        )
        
        # This will raise ValidationError if any field is invalid
        validate_complete_task(
            title="",  # Invalid - empty title
            status="pending",
            priority="medium"
        )
    
    Implementation Notes:
    - We call each validation function in sequence
    - If any validation fails, the error propagates immediately
    - This is a simple approach - stops at first error
    - For better UX, you could collect all errors and return them together
    - This pattern is commonly used in model create/update methods
    
    Advanced Pattern (collecting all errors):
        errors = []
        try:
            validate_task_title(title)
        except ValidationError as e:
            errors.append(str(e))
        
        try:
            validate_task_status(status)
        except ValidationError as e:
            errors.append(str(e))
        
        if errors:
            raise ValidationError("; ".join(errors))
    """
    # Validate each field in sequence
    # If any validation fails, the error will propagate up
    
    # Validate required fields
    validate_task_title(title)
    validate_task_status(status)
    validate_task_priority(priority)
    
    # Validate optional fields if provided
    if description is not None:
        validate_task_description(description)


# ============================================================================
# Additional Validation Functions (Extra Practice)
# ============================================================================

def validate_task_due_date(due_date: str) -> None:
    """
    Validate that a due date is in the correct format.
    
    EXTRA: This demonstrates date format validation.
    
    Args:
        due_date: Date string in YYYY-MM-DD format
    
    Raises:
        ValidationError: If date format is invalid
    
    Example Usage:
        validate_task_due_date("2024-12-31")  # Passes
        validate_task_due_date("12/31/2024")  # Raises ValidationError
        validate_task_due_date("2024-13-01")  # Raises ValidationError (invalid month)
    """
    from datetime import datetime
    
    try:
        # Try to parse the date string
        # This will raise ValueError if the format is wrong or date is invalid
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(
            "Due date must be in YYYY-MM-DD format (e.g., 2024-12-31)"
        )


def validate_task_id(task_id: int) -> None:
    """
    Validate that a task ID is a positive integer.
    
    EXTRA: This demonstrates numeric validation.
    
    Args:
        task_id: The task ID to validate
    
    Raises:
        ValidationError: If task_id is not a positive integer
    
    Example Usage:
        validate_task_id(1)    # Passes
        validate_task_id(100)  # Passes
        validate_task_id(0)    # Raises ValidationError
        validate_task_id(-5)   # Raises ValidationError
    """
    if not isinstance(task_id, int):
        raise ValidationError("Task ID must be an integer")
    
    if task_id <= 0:
        raise ValidationError("Task ID must be a positive integer")


# ============================================================================
# Testing Functions
# ============================================================================

def run_tests():
    """
    Test all validation functions with various inputs.
    
    This function demonstrates how to test validation functions.
    Run it to verify that all validations work correctly.
    
    Usage:
        python -c "from exercises.solutions.todo_validators_complete import run_tests; run_tests()"
    
    Or add at the bottom of the file:
        if __name__ == "__main__":
            run_tests()
    """
    print("\n" + "=" * 70)
    print("TESTING TODO VALIDATORS - COMPLETE SOLUTION")
    print("=" * 70)
    
    # Test validate_task_title
    print("\n--- Testing validate_task_title() ---")
    
    # Test valid titles
    valid_titles = [
        "Buy groceries",
        "Complete Python tutorial",
        "A",  # Minimum length
        "X" * 200  # Maximum length
    ]
    
    for title in valid_titles:
        try:
            validate_task_title(title)
            print(f"✓ Valid title passed: '{title[:50]}...' " if len(title) > 50 else f"✓ Valid title passed: '{title}'")
        except ValidationError as e:
            print(f"✗ Unexpected error for '{title[:50]}...': {e}")
    
    # Test invalid titles
    invalid_titles = [
        ("", "empty string"),
        ("   ", "whitespace only"),
        ("X" * 201, "too long")
    ]
    
    for title, reason in invalid_titles:
        try:
            validate_task_title(title)
            print(f"✗ Should have raised ValidationError for {reason}")
        except ValidationError as e:
            print(f"✓ Invalid title caught ({reason}): {e}")
    
    # Test validate_task_status
    print("\n--- Testing validate_task_status() ---")
    
    # Test valid statuses
    valid_statuses = ["pending", "in_progress", "completed"]
    
    for status in valid_statuses:
        try:
            validate_task_status(status)
            print(f"✓ Valid status passed: '{status}'")
        except ValidationError as e:
            print(f"✗ Unexpected error for '{status}': {e}")
    
    # Test invalid statuses
    invalid_statuses = [
        ("done", "invalid value"),
        ("PENDING", "wrong case"),
        ("in progress", "space instead of underscore")
    ]
    
    for status, reason in invalid_statuses:
        try:
            validate_task_status(status)
            print(f"✗ Should have raised ValidationError for {reason}")
        except ValidationError as e:
            print(f"✓ Invalid status caught ({reason}): {e}")
    
    # Test validate_task_priority
    print("\n--- Testing validate_task_priority() ---")
    
    # Test valid priorities
    valid_priorities = ["low", "medium", "high"]
    
    for priority in valid_priorities:
        try:
            validate_task_priority(priority)
            print(f"✓ Valid priority passed: '{priority}'")
        except ValidationError as e:
            print(f"✗ Unexpected error for '{priority}': {e}")
    
    # Test invalid priorities
    invalid_priorities = [
        ("urgent", "invalid value"),
        ("HIGH", "wrong case"),
        ("normal", "not in allowed list")
    ]
    
    for priority, reason in invalid_priorities:
        try:
            validate_task_priority(priority)
            print(f"✗ Should have raised ValidationError for {reason}")
        except ValidationError as e:
            print(f"✓ Invalid priority caught ({reason}): {e}")
    
    # Test validate_task_description (bonus)
    print("\n--- Testing validate_task_description() (BONUS) ---")
    
    # Test valid descriptions
    valid_descriptions = [
        "",  # Empty is allowed
        "Short description",
        "X" * 1000  # Maximum length
    ]
    
    for desc in valid_descriptions:
        try:
            validate_task_description(desc)
            print(f"✓ Valid description passed: '{desc[:50]}...' " if len(desc) > 50 else f"✓ Valid description passed: '{desc}'")
        except ValidationError as e:
            print(f"✗ Unexpected error: {e}")
    
    # Test invalid descriptions
    try:
        validate_task_description("X" * 1001)  # Too long
        print("✗ Should have raised ValidationError for too long description")
    except ValidationError as e:
        print(f"✓ Invalid description caught (too long): {e}")
    
    # Test validate_complete_task (bonus)
    print("\n--- Testing validate_complete_task() (BONUS) ---")
    
    # Test valid complete task
    try:
        validate_complete_task(
            title="Buy groceries",
            status="pending",
            priority="medium",
            description="Get milk, eggs, and bread"
        )
        print("✓ Valid complete task passed")
    except ValidationError as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test invalid complete task (empty title)
    try:
        validate_complete_task(
            title="",
            status="pending",
            priority="medium"
        )
        print("✗ Should have raised ValidationError for empty title")
    except ValidationError as e:
        print(f"✓ Invalid complete task caught (empty title): {e}")
    
    # Test invalid complete task (invalid status)
    try:
        validate_complete_task(
            title="Valid title",
            status="done",  # Invalid
            priority="medium"
        )
        print("✗ Should have raised ValidationError for invalid status")
    except ValidationError as e:
        print(f"✓ Invalid complete task caught (invalid status): {e}")
    
    # Test validate_task_due_date (extra)
    print("\n--- Testing validate_task_due_date() (EXTRA) ---")
    
    # Test valid dates
    valid_dates = ["2024-12-31", "2025-01-01", "2024-02-29"]  # 2024 is a leap year
    
    for date_str in valid_dates:
        try:
            validate_task_due_date(date_str)
            print(f"✓ Valid date passed: '{date_str}'")
        except ValidationError as e:
            print(f"✗ Unexpected error for '{date_str}': {e}")
    
    # Test invalid dates
    invalid_dates = [
        ("12/31/2024", "wrong format"),
        ("2024-13-01", "invalid month"),
        ("2024-02-30", "invalid day"),
        ("not-a-date", "not a date")
    ]
    
    for date_str, reason in invalid_dates:
        try:
            validate_task_due_date(date_str)
            print(f"✗ Should have raised ValidationError for {reason}")
        except ValidationError as e:
            print(f"✓ Invalid date caught ({reason}): {e}")
    
    # Test validate_task_id (extra)
    print("\n--- Testing validate_task_id() (EXTRA) ---")
    
    # Test valid IDs
    valid_ids = [1, 100, 999999]
    
    for task_id in valid_ids:
        try:
            validate_task_id(task_id)
            print(f"✓ Valid ID passed: {task_id}")
        except ValidationError as e:
            print(f"✗ Unexpected error for {task_id}: {e}")
    
    # Test invalid IDs
    invalid_ids = [
        (0, "zero"),
        (-5, "negative"),
        ("1", "string instead of int")
    ]
    
    for task_id, reason in invalid_ids:
        try:
            validate_task_id(task_id)
            print(f"✗ Should have raised ValidationError for {reason}")
        except ValidationError as e:
            print(f"✓ Invalid ID caught ({reason}): {e}")
    
    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)
    print("\nAll validation functions are working correctly!")
    print("\nKey Takeaways:")
    print("1. Validation functions should be simple and focused")
    print("2. Reuse existing validation utilities when possible")
    print("3. Provide clear, helpful error messages")
    print("4. Compose simple validations to create complex ones")
    print("5. Test both valid and invalid inputs")
    print()


# ============================================================================
# Solution Summary and Learning Notes
# ============================================================================

"""
SOLUTION SUMMARY:

This complete solution demonstrates validation best practices:

1. **Reusing Validation Utilities**:
   - Import and use functions from validators.py
   - Don't reinvent the wheel - use existing tools
   - Compose simple validations to create complex ones

2. **Clear Function Names**:
   - validate_task_title, validate_task_status, etc.
   - Names clearly indicate what is being validated
   - Consistent naming pattern across all functions

3. **Comprehensive Documentation**:
   - Docstrings explain what the function does
   - Examples show valid and invalid inputs
   - Implementation notes explain the approach

4. **Error Messages**:
   - Let utility functions provide error messages
   - Don't catch and re-raise unless adding context
   - Error messages are clear and actionable

5. **Testing**:
   - Test both valid and invalid inputs
   - Test edge cases (empty, maximum length, etc.)
   - Verify error messages are helpful

Key Patterns Demonstrated:

1. **Simple Validation**:
   ```python
   def validate_field(value):
       validate_not_empty(value, "Field")
   ```

2. **Enum Validation**:
   ```python
   def validate_status(status):
       allowed = ["pending", "completed"]
       validate_choice(status, "Status", allowed)
   ```

3. **Composed Validation**:
   ```python
   def validate_title(title):
       validate_not_empty(title, "Title")
       validate_length(title, "Title", max_len=200)
   ```

4. **Optional Field Validation**:
   ```python
   def validate_description(desc):
       if desc and desc.strip():
           validate_length(desc, "Description", max_len=1000)
   ```

5. **Complete Object Validation**:
   ```python
   def validate_complete_task(title, status, priority):
       validate_task_title(title)
       validate_task_status(status)
       validate_task_priority(priority)
   ```

Comparison with Exercise File:

The exercise file (validation/exercises/todo_validators.py) has:
- Function signatures with TODO comments
- Detailed step-by-step hints
- Empty implementations (pass statements)

This solution file has:
- Complete implementations
- Additional bonus functions
- Comprehensive testing function
- Detailed explanations of the approach

How to Use This Solution:

1. **Compare**: Look at your implementation vs. this solution
2. **Understand**: Read the comments to understand the patterns
3. **Test**: Run the run_tests() function to see it in action
4. **Experiment**: Try modifying the validations
5. **Apply**: Use these patterns in your own projects

Integration with Models:

These validation functions are used in the Task model like this:

```python
class Task:
    @staticmethod
    def create(title, status, priority):
        # Validate all inputs first
        validate_task_title(title)
        validate_task_status(status)
        validate_task_priority(priority)
        
        # Only proceed if validation passed
        query = "INSERT INTO tasks (...) VALUES (...)"
        execute_insert(query, (...))
```

This separation of concerns makes code:
- More maintainable (validation logic in one place)
- More testable (can test validation independently)
- More reusable (same validation for create and update)
- Easier to understand (clear separation of responsibilities)

Next Steps:

1. Run the tests to see all validations in action
2. Try adding new validation functions
3. Integrate these validations into your Task model
4. Apply these patterns to the Inventory system
5. Consider more advanced validation (regex, custom rules)

Remember: Good validation is the first line of defense against bad data.
Always validate input before it reaches your database!
"""


# Uncomment this to run tests when executing this file directly
if __name__ == "__main__":
    run_tests()
