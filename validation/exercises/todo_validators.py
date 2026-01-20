"""
Todo System Validation Exercises

This module contains validation exercises for the Todo system. Your task is to
implement validation functions for task fields using the validation utilities
from the validators module.

Learning Objectives:
- Practice using existing validation functions
- Understand how to validate enum-like fields
- Learn to compose multiple validation checks
- Write clear, reusable validation logic

Instructions:
1. Study the validation functions in validation/validators.py
2. Import the functions you need
3. Implement each validation function below
4. Test your validators with both valid and invalid inputs
5. Make sure error messages are clear and helpful

Requirements Reference:
- Requirement 1.5: Clear TODO comments explaining what to implement
- Requirement 5.3: Validation exercises for students
- Requirement 7.4: Detailed documentation with hints and requirements
"""

# TODO: Import the validation functions you need from validators.py
# Hint: You'll need validate_not_empty, validate_length, and validate_choice
# Example: from validation.validators import validate_not_empty, ValidationError


def validate_task_title(title: str) -> None:
    """
    Validate that a task title meets all requirements.
    
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
    
    TODO: Implement this function
    
    Step-by-step hints:
    1. First, check if the title is not empty using validate_not_empty()
       - Pass the title and the field name "Title" as arguments
       - This will raise ValidationError if the title is empty
    
    2. Then, check the length constraints using validate_length()
       - Pass the title, field name "Title", min_len=1, and max_len=200
       - This will raise ValidationError if the title is too short or too long
    
    3. If both validations pass, the function completes successfully
       - No need to return anything (returns None implicitly)
    
    Why these validations?
    - Not empty: Every task needs a title to identify it
    - Max 200 chars: Keeps titles concise and fits database column limits
    - Min 1 char: Ensures title has actual content after stripping whitespace
    
    Testing your implementation:
        # Test with valid input
        try:
            validate_task_title("Buy groceries")
            print("✓ Valid title passed")
        except ValidationError as e:
            print(f"✗ Unexpected error: {e}")
        
        # Test with empty input
        try:
            validate_task_title("")
            print("✗ Should have raised ValidationError")
        except ValidationError as e:
            print(f"✓ Empty title caught: {e}")
        
        # Test with too long input
        try:
            validate_task_title("A" * 250)
            print("✗ Should have raised ValidationError")
        except ValidationError as e:
            print(f"✓ Long title caught: {e}")
    """
    # TODO: Add your validation code here
    # Remember to import the necessary functions at the top of the file first!
    pass


def validate_task_status(status: str) -> None:
    """
    Validate that a task status is one of the allowed values.
    
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
    
    TODO: Implement this function
    
    Step-by-step hints:
    1. Define a list of allowed status values
       - Create a list: allowed_statuses = ["pending", "in_progress", "completed"]
       - These are the only valid status values for tasks
    
    2. Use validate_choice() to check if status is in the allowed list
       - Pass the status, field name "Status", and the allowed_statuses list
       - This will raise ValidationError if status is not in the list
    
    3. The function completes successfully if validation passes
    
    Why this validation?
    - Ensures data consistency: Only valid statuses in the database
    - Prevents typos: "done" instead of "completed" would be caught
    - Makes queries reliable: You can filter by status knowing values are valid
    - Supports UI: Dropdown menus can use the same allowed values
    
    Design note:
    - Status values are lowercase with underscores (snake_case)
    - This is a common convention in Python and databases
    - Case-sensitive validation prevents inconsistencies
    
    Testing your implementation:
        # Test with valid statuses
        for status in ["pending", "in_progress", "completed"]:
            try:
                validate_task_status(status)
                print(f"✓ Valid status '{status}' passed")
            except ValidationError as e:
                print(f"✗ Unexpected error: {e}")
        
        # Test with invalid status
        try:
            validate_task_status("done")
            print("✗ Should have raised ValidationError")
        except ValidationError as e:
            print(f"✓ Invalid status caught: {e}")
        
        # Test with wrong case
        try:
            validate_task_status("PENDING")
            print("✗ Should have raised ValidationError")
        except ValidationError as e:
            print(f"✓ Wrong case caught: {e}")
    """
    # TODO: Add your validation code here
    # Hint: Define allowed_statuses list first, then use validate_choice()
    pass


def validate_task_priority(priority: str) -> None:
    """
    Validate that a task priority is one of the allowed values.
    
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
    
    TODO: Implement this function
    
    Step-by-step hints:
    1. Define a list of allowed priority values
       - Create a list: allowed_priorities = ["low", "medium", "high"]
       - These represent the three priority levels for tasks
    
    2. Use validate_choice() to check if priority is in the allowed list
       - Pass the priority, field name "Priority", and the allowed_priorities list
       - This will raise ValidationError if priority is not in the list
    
    3. The function completes successfully if validation passes
    
    Why this validation?
    - Ensures consistent priority levels across all tasks
    - Prevents invalid values like "urgent", "critical", "normal"
    - Makes sorting and filtering by priority reliable
    - Supports UI: Can display priority badges with consistent values
    
    Design considerations:
    - Three levels (low/medium/high) is simple and sufficient for most use cases
    - More levels (like 1-5 or critical/high/medium/low/trivial) can be confusing
    - Lowercase convention matches status field for consistency
    
    Extension ideas (optional challenges):
    - Add a 'critical' priority level for extremely urgent tasks
    - Implement priority_to_number() to convert priorities to sortable integers
    - Add validation for numeric priorities (1-5) as an alternative
    
    Testing your implementation:
        # Test with valid priorities
        for priority in ["low", "medium", "high"]:
            try:
                validate_task_priority(priority)
                print(f"✓ Valid priority '{priority}' passed")
            except ValidationError as e:
                print(f"✗ Unexpected error: {e}")
        
        # Test with invalid priority
        try:
            validate_task_priority("urgent")
            print("✗ Should have raised ValidationError")
        except ValidationError as e:
            print(f"✓ Invalid priority caught: {e}")
        
        # Test with wrong case
        try:
            validate_task_priority("HIGH")
            print("✗ Should have raised ValidationError")
        except ValidationError as e:
            print(f"✓ Wrong case caught: {e}")
    """
    # TODO: Add your validation code here
    # Hint: This is very similar to validate_task_status()
    pass


# ============================================================================
# BONUS EXERCISES (Optional - Try these after completing the above functions)
# ============================================================================

def validate_task_description(description: str) -> None:
    """
    BONUS: Validate that a task description meets requirements.
    
    A valid task description:
    - Can be empty (description is optional)
    - If provided, must not exceed 1000 characters
    
    Args:
        description: The task description to validate (can be empty)
    
    Raises:
        ValidationError: If description exceeds maximum length
    
    TODO: Implement this function
    
    Hints:
    - Description is optional, so empty strings should be allowed
    - Only validate length if description is not empty
    - Use validate_length() with only max_len parameter
    
    Challenge: How do you handle None vs empty string?
    """
    pass


def validate_complete_task(title: str, status: str, priority: str, description: str = None) -> None:
    """
    BONUS: Validate all task fields at once.
    
    This function demonstrates how to compose multiple validation functions
    to validate an entire task object before creating or updating it.
    
    Args:
        title: Task title
        status: Task status
        priority: Task priority
        description: Task description (optional)
    
    Raises:
        ValidationError: If any field validation fails
    
    TODO: Implement this function
    
    Hints:
    - Call each validation function in sequence
    - If any validation fails, the error will propagate up
    - This is a common pattern: validate all fields before database operations
    
    Example usage in a model:
        def create_task(title, status, priority, description=None):
            # Validate everything first
            validate_complete_task(title, status, priority, description)
            
            # Only proceed if validation passed
            query = "INSERT INTO tasks (...) VALUES (...)"
            execute_update(query, (...))
    """
    pass


# ============================================================================
# TESTING SECTION
# ============================================================================

def run_tests():
    """
    Test all validation functions with various inputs.
    
    Run this function to test your implementations:
        python -c "from validation.exercises.todo_validators import run_tests; run_tests()"
    
    Or add this at the bottom of the file:
        if __name__ == "__main__":
            run_tests()
    """
    print("\n" + "=" * 70)
    print("TESTING TODO VALIDATORS")
    print("=" * 70)
    
    # Import ValidationError for testing
    # TODO: Uncomment this when you've imported ValidationError at the top
    # from validation.validators import ValidationError
    
    # Test validate_task_title
    print("\n--- Testing validate_task_title() ---")
    # TODO: Add your test cases here
    print("TODO: Implement tests for validate_task_title()")
    
    # Test validate_task_status
    print("\n--- Testing validate_task_status() ---")
    # TODO: Add your test cases here
    print("TODO: Implement tests for validate_task_status()")
    
    # Test validate_task_priority
    print("\n--- Testing validate_task_priority() ---")
    # TODO: Add your test cases here
    print("TODO: Implement tests for validate_task_priority()")
    
    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Implement the validation functions above")
    print("2. Add test cases to this run_tests() function")
    print("3. Run the tests to verify your implementations")
    print("4. Try the bonus exercises for extra practice")
    print()


# Uncomment this to run tests when executing this file directly
# if __name__ == "__main__":
#     run_tests()
