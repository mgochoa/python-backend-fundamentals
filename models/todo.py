"""
Todo System Models - Guided Exercise Implementation

This module provides a PARTIAL implementation of CRUD operations for the
Todo System. This is a GUIDED EXERCISE where you'll complete the implementation
yourself with hints and scaffolding provided.

Learning Approach:
- Study the complete Book model in models/library.py first
- One method (get_by_id) is provided as a complete reference
- Other methods have function signatures, docstrings, and TODO comments
- Follow the patterns from the library system to complete each method

The Todo System includes two main entities:
1. Task: Represents todo items that users need to complete
2. Category: Represents groups/categories for organizing tasks (optional exercise)

This is a GUIDED IMPLEMENTATION - you'll write the code with help from:
- Detailed docstrings explaining what each method should do
- TODO comments with step-by-step hints
- References to similar methods in the library system
- Clear requirements and examples

Key Learning Objectives:
- Practice implementing CRUD operations yourself
- Apply validation patterns you've learned
- Handle errors gracefully
- Use parameterized queries safely
- Build confidence in backend development

Requirements Addressed:
- Requirement 1.5: Clear TODO markers with explanations
- Requirement 3.2: Partial implementations with TODO markers
- Requirement 3.3: Function signatures and docstrings
- Requirement 7.4: Detailed hints for each TODO
"""

import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# Import database connection utilities
from database.connection import execute_query, execute_insert, execute_update, QueryExecutionError


# ============================================================================
# Custom Exception Classes
# ============================================================================
# These are the same exceptions used in the library system
# Study how they're used in models/library.py

class ValidationError(Exception):
    """
    Raised when input validation fails.
    
    Examples:
    - Empty required fields
    - Invalid data formats
    - Out-of-range values
    """
    pass


class DuplicateError(Exception):
    """
    Raised when attempting to create a record that already exists.
    
    Note: The todo system doesn't have unique constraints like ISBN,
    but this is included for consistency and potential future use.
    """
    pass


class NotFoundError(Exception):
    """
    Raised when a requested record doesn't exist.
    
    Examples:
    - Trying to get a task with non-existent ID
    - Trying to update a task that doesn't exist
    """
    pass


# ============================================================================
# Validation Helper Functions
# ============================================================================
# TODO: You'll use these in your Task.create() implementation
# Study how similar functions are used in models/library.py

def validate_not_empty(value: str, field_name: str) -> None:
    """
    Validate that a string field is not empty or whitespace-only.
    
    This is the same validation function from the library system.
    You'll use this to validate the task title.
    
    Args:
        value: The string to validate
        field_name: Name of the field (for error messages)
        
    Raises:
        ValidationError: If value is None, empty, or only whitespace
        
    Example:
        >>> validate_not_empty("Buy groceries", "Title")  # OK
        >>> validate_not_empty("", "Title")  # Raises ValidationError
        >>> validate_not_empty("   ", "Title")  # Raises ValidationError
    """
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")


def validate_status(status: str) -> None:
    """
    Validate that status is one of the allowed values.
    
    TODO: This function is COMPLETE as a reference example.
    Study how it works - you'll write similar validation for priority.
    
    Args:
        status: The status value to validate
        
    Raises:
        ValidationError: If status is not one of the allowed values
        
    Example:
        >>> validate_status("pending")  # OK
        >>> validate_status("completed")  # OK
        >>> validate_status("invalid")  # Raises ValidationError
    """
    allowed_statuses = ["pending", "in_progress", "completed"]
    if status not in allowed_statuses:
        raise ValidationError(
            f"Status must be one of: {', '.join(allowed_statuses)}. "
            f"Got: '{status}'"
        )


def validate_priority(priority: str) -> None:
    """
    Validate that priority is one of the allowed values.
    
    TODO: Implement this function following the pattern from validate_status().
    
    Requirements:
    - Allowed priority values: "low", "medium", "high"
    - Raise ValidationError if priority is not in the allowed list
    - Include a helpful error message showing allowed values
    
    Args:
        priority: The priority value to validate
        
    Raises:
        ValidationError: If priority is not one of the allowed values
        
    Example:
        >>> validate_priority("high")  # Should work
        >>> validate_priority("urgent")  # Should raise ValidationError
        
    Hint: Copy the validate_status() function and modify it for priority.
    """
    # TODO: Implement priority validation
    # Step 1: Define the list of allowed priority values
    # Step 2: Check if the provided priority is in the allowed list
    # Step 3: If not, raise ValidationError with a helpful message
    pass


def validate_title_length(title: str) -> None:
    """
    Validate that title length is within acceptable range.
    
    TODO: Implement this function to check title length.
    
    Requirements:
    - Title must be at least 1 character (after stripping whitespace)
    - Title must be at most 200 characters
    - Raise ValidationError if length is invalid
    
    Args:
        title: The title to validate
        
    Raises:
        ValidationError: If title length is invalid
        
    Example:
        >>> validate_title_length("Buy milk")  # OK
        >>> validate_title_length("A" * 300)  # Should raise ValidationError (too long)
        
    Hint: Use len() to get string length, and check against min/max values.
    """
    # TODO: Implement title length validation
    # Step 1: Check if title is too short (less than 1 character)
    # Step 2: Check if title is too long (more than 200 characters)
    # Step 3: Raise ValidationError with appropriate message if invalid
    pass


# ============================================================================
# Task Model Class
# ============================================================================

class Task:
    """
    Model class for Task entity - Guided Exercise Implementation.
    
    This class provides CRUD operations for tasks in the todo system.
    Some methods are complete (for reference), others have TODOs for you to complete.
    
    Database Table: tasks
    Fields (as defined in database/schemas/todo_schema.sql):
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - title: TEXT NOT NULL
    - description: TEXT (optional)
    - status: TEXT NOT NULL DEFAULT 'pending'
    - priority: TEXT NOT NULL DEFAULT 'medium'
    - due_date: DATE (optional)
    - category_id: INTEGER (optional, foreign key to categories)
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    Note: If you haven't completed the schema TODOs yet, some fields may not exist.
    For this exercise, we'll work with the basic fields: id, title, description, created_at.
    
    Learning Objectives:
    - Implement CRUD operations with guidance
    - Apply validation before database operations
    - Handle errors gracefully
    - Use parameterized queries
    - Build on patterns from the library system
    """
    
    @staticmethod
    def get_by_id(task_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single task by its ID.
        
        *** THIS METHOD IS COMPLETE - STUDY IT AS A REFERENCE! ***
        
        This is a fully implemented example for you to study and use as a
        reference when implementing other methods. Pay attention to:
        
        1. How the SQL query is structured with a WHERE clause
        2. How we use parameterized queries (?) for safety
        3. How we handle the case when no task is found (return None)
        4. How we catch and re-raise exceptions with context
        5. The pattern: query → execute → return result or None
        
        This method demonstrates:
        - Simple SELECT query with WHERE clause
        - Using parameterized queries for filtering
        - Returning None when record doesn't exist
        - Converting database row to dictionary
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            Dictionary containing task data if found, None if not found
            Dictionary keys: id, title, description, created_at
                           (and status, priority, due_date if schema is complete)
            
        Raises:
            QueryExecutionError: If database operation fails
            
        Example:
            >>> task = Task.get_by_id(1)
            >>> if task:
            ...     print(f"Task: {task['title']}")
            ...     print(f"Description: {task['description']}")
            ...     print(f"Created: {task['created_at']}")
            ... else:
            ...     print("Task not found")
            
        Learning Notes:
        - This follows the exact same pattern as Book.get_by_id()
        - SELECT queries return a list, even if only one row matches
        - We return the first result if found, None if the list is empty
        - This is a common Python pattern: results[0] if results else None
        - Always use parameterized queries to prevent SQL injection
        
        Compare this to Book.get_by_id() in models/library.py - they're almost identical!
        This shows how CRUD patterns are consistent across different entities.
        """
        # Step 1: Prepare the SELECT query with WHERE clause
        # The ? placeholder will be safely replaced with task_id
        query = "SELECT * FROM tasks WHERE id = ?"
        
        try:
            # Step 2: Execute the query with the task_id parameter
            # execute_query returns a list of dictionaries (rows)
            results = execute_query(query, (task_id,))
            
            # Step 3: Return the first result if found, None if list is empty
            # If results is empty [], results[0] would cause an error
            # So we use: results[0] if results else None
            return results[0] if results else None
            
        except QueryExecutionError as e:
            # Step 4: Catch database errors and re-raise with context
            # This helps with debugging by providing more information
            raise QueryExecutionError(f"Failed to retrieve task: {str(e)}")
    
    @staticmethod
    def create(title: str, description: str = None) -> int:
        """
        Create a new task record in the database.
        
        *** THIS METHOD HAS TODOs FOR YOU TO COMPLETE! ***
        
        This method is partially implemented with TODO comments guiding you
        through the completion. Follow the steps and hints provided.
        
        This method should demonstrate:
        1. Input validation before database operations
        2. Using parameterized queries to prevent SQL injection
        3. Returning the ID of the newly created record
        4. Comprehensive error handling
        
        Args:
            title: Task title (required, cannot be empty, max 200 characters)
            description: Detailed description of the task (optional)
            
        Returns:
            int: The ID of the newly created task record
            
        Raises:
            ValidationError: If any input validation fails
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Create a task with just a title
            >>> task_id = Task.create("Buy groceries")
            >>> print(f"Created task with ID: {task_id}")
            
            >>> # Create a task with title and description
            >>> task_id = Task.create(
            ...     title="Finish project report",
            ...     description="Complete the Q4 analysis and submit by Friday"
            ... )
            
        Learning Notes:
        - Compare this to Book.create() in models/library.py
        - The pattern is: validate → prepare query → execute → return ID
        - Always validate input BEFORE executing database operations
        - Use ? placeholders for values to prevent SQL injection
        
        Reference: Study Book.create() in models/library.py for the complete pattern.
        """
        # ====================================================================
        # TODO 1: Validate the title
        # ====================================================================
        # The title is required and must meet certain criteria.
        # 
        # Steps:
        # 1. Call validate_not_empty() to ensure title is not empty
        # 2. Call validate_title_length() to ensure title is not too long
        # 3. Wrap validation in try-except to catch ValidationError
        # 4. Re-raise with additional context if validation fails
        #
        # Hint: Look at Book.create() to see how multiple validations are called
        # Hint: Use try-except to catch ValidationError and re-raise with context
        #
        # Example pattern:
        # try:
        #     validate_not_empty(title, "Title")
        #     validate_title_length(title)
        # except ValidationError as e:
        #     raise ValidationError(f"Invalid task data: {str(e)}")
        
        # TODO: Add your validation code here
        
        # ====================================================================
        # TODO 2: Prepare the SQL INSERT query
        # ====================================================================
        # Create an INSERT query to add a new task to the database.
        #
        # Requirements:
        # - Insert into the 'tasks' table
        # - Include fields: title, description
        # - Use ? placeholders for values (NEVER use f-strings or string formatting!)
        # - If you've completed the schema TODOs, you can also include:
        #   status (default 'pending'), priority (default 'medium')
        #
        # Basic version (works with incomplete schema):
        # query = """
        #     INSERT INTO tasks (title, description)
        #     VALUES (?, ?)
        # """
        #
        # Advanced version (if schema is complete with status and priority):
        # query = """
        #     INSERT INTO tasks (title, description, status, priority)
        #     VALUES (?, ?, ?, ?)
        # """
        #
        # Hint: Start with the basic version, then enhance it later
        # Hint: Look at Book.create() for the INSERT query pattern
        
        # TODO: Add your query here
        query = """
            INSERT INTO tasks (title, description)
            VALUES (?, ?)
        """
        
        # ====================================================================
        # TODO 3: Execute the query and return the new task ID
        # ====================================================================
        # Execute the INSERT query and return the ID of the new task.
        #
        # Steps:
        # 1. Call execute_insert() with the query and parameters
        # 2. The parameters should be a tuple: (title, description)
        # 3. If using advanced version with status/priority, include those too
        # 4. Wrap in try-except to catch QueryExecutionError
        # 5. Return the task_id from execute_insert()
        #
        # Basic version parameters:
        # params = (title, description)
        #
        # Advanced version parameters (if schema is complete):
        # params = (title, description, 'pending', 'medium')
        #
        # Hint: execute_insert() returns the ID of the newly created record
        # Hint: Look at Book.create() for the execution pattern
        
        # TODO: Add your execution code here
        try:
            task_id = execute_insert(query, (title, description))
            return task_id
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to create task: {str(e)}")
    
    @staticmethod
    def get_all(status: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks, optionally filtered by status.
        
        *** THIS METHOD IS FOR YOU TO IMPLEMENT! ***
        
        This method should demonstrate:
        1. SELECT query with optional WHERE clause
        2. Dynamic query building based on parameters
        3. ORDER BY clause for sorting results
        4. Returning empty list when no results
        
        Args:
            status: Optional status filter - if provided, only return tasks with this status
                   Valid values: "pending", "in_progress", "completed"
                   If None, return all tasks regardless of status
            
        Returns:
            List of dictionaries, each containing task data
            Returns empty list [] if no tasks found
            Sorted by created_at descending (newest first)
            
        Raises:
            ValidationError: If status is provided but invalid
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Get all tasks
            >>> all_tasks = Task.get_all()
            >>> for task in all_tasks:
            ...     print(f"- {task['title']}")
            
            >>> # Get only pending tasks
            >>> pending = Task.get_all(status="pending")
            >>> print(f"You have {len(pending)} pending tasks")
            
            >>> # Get completed tasks
            >>> completed = Task.get_all(status="completed")
            
        Learning Notes:
        - This is similar to Book.get_all() but simpler (no sort_by parameter)
        - Build the query dynamically based on whether status is provided
        - Always validate the status parameter if it's provided
        - Use ORDER BY to sort results (newest first)
        
        Implementation Steps:
        
        TODO 1: Validate the status parameter (if provided)
        - If status is not None, call validate_status(status)
        - Wrap in try-except to catch ValidationError
        
        TODO 2: Build the query dynamically
        - Start with: query = "SELECT * FROM tasks"
        - If status is provided, add: " WHERE status = ?"
        - Add ORDER BY: " ORDER BY created_at DESC"
        - Create params list: [] if no status, [status] if status provided
        
        TODO 3: Execute the query
        - Call execute_query(query, tuple(params))
        - Wrap in try-except to catch QueryExecutionError
        - Return the results (will be empty list if no tasks found)
        
        Hint: Study Book.get_all() in models/library.py for the pattern
        Hint: Use an empty list for params if no filtering is needed
        Hint: Convert params list to tuple when calling execute_query
        
        Reference: Book.get_all() shows how to build dynamic queries with optional filtering.
        """
        # TODO: Implement this method following the steps above
        # Your code here
        pass
    
    @staticmethod
    def update_status(task_id: int, new_status: str) -> bool:
        """
        Update the status of a task.
        
        *** THIS METHOD IS FOR YOU TO IMPLEMENT! ***
        
        This method should demonstrate:
        1. Validating input before database operations
        2. Simple UPDATE query with WHERE clause
        3. Checking if update actually affected any rows
        4. Returning boolean to indicate success
        
        Args:
            task_id: ID of the task to update
            new_status: New status value ("pending", "in_progress", or "completed")
            
        Returns:
            bool: True if task was updated, False if task not found
            
        Raises:
            ValidationError: If new_status is invalid
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Mark a task as in progress
            >>> if Task.update_status(1, "in_progress"):
            ...     print("Task status updated")
            ... else:
            ...     print("Task not found")
            
            >>> # Mark a task as completed
            >>> Task.update_status(1, "completed")
            
            >>> # Try to update with invalid status
            >>> try:
            ...     Task.update_status(1, "invalid")
            ... except ValidationError as e:
            ...     print(f"Error: {e}")
            
        Learning Notes:
        - This is simpler than Book.update() because we only update one field
        - Always validate the new status before executing the query
        - Check affected_rows to see if the task_id existed
        - Return False for "not found" rather than raising an exception
        
        Implementation Steps:
        
        TODO 1: Validate the new_status
        - Call validate_status(new_status)
        - Wrap in try-except to catch and re-raise ValidationError
        
        TODO 2: Prepare the UPDATE query
        - UPDATE tasks SET status = ? WHERE id = ?
        - Use ? placeholders for both status and task_id
        
        TODO 3: Execute the update
        - Call execute_update(query, (new_status, task_id))
        - This returns the number of affected rows
        - Wrap in try-except to catch QueryExecutionError
        
        TODO 4: Return success indicator
        - Return True if affected_rows > 0 (task was updated)
        - Return False if affected_rows == 0 (task_id not found)
        
        Hint: Study Book.update() and Book.delete() for similar patterns
        Hint: execute_update() returns the number of rows affected
        Hint: If 0 rows were affected, the task_id didn't exist
        
        Reference: Book.delete() shows the pattern of checking affected_rows.
        """
        # TODO: Implement this method following the steps above
        # Your code here
        pass
    
    @staticmethod
    def delete(task_id: int) -> bool:
        """
        Delete a task record from the database.
        
        *** THIS METHOD IS FOR YOU TO IMPLEMENT! ***
        
        This method should demonstrate:
        1. Simple DELETE query with WHERE clause
        2. Checking if deletion actually removed a row
        3. Returning boolean to indicate success
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            bool: True if task was deleted, False if task not found
            
        Raises:
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Delete a task
            >>> if Task.delete(1):
            ...     print("Task deleted successfully")
            ... else:
            ...     print("Task not found")
            
            >>> # Try to delete non-existent task
            >>> result = Task.delete(999)
            >>> print(result)  # False
            
        Learning Notes:
        - DELETE is permanent - there's no undo!
        - Always use WHERE clause (DELETE without WHERE removes ALL rows!)
        - Check affected rows to see if anything was actually deleted
        - This is one of the simpler CRUD operations
        
        Implementation Steps:
        
        TODO 1: Prepare the DELETE query
        - DELETE FROM tasks WHERE id = ?
        - CRITICAL: Always include WHERE clause!
        - Use ? placeholder for task_id
        
        TODO 2: Execute the deletion
        - Call execute_update(query, (task_id,))
        - This returns the number of affected rows
        - Wrap in try-except to catch QueryExecutionError
        
        TODO 3: Return success indicator
        - Return True if affected_rows > 0 (task was deleted)
        - Return False if affected_rows == 0 (task_id not found)
        
        Hint: This is almost identical to Book.delete()
        Hint: execute_update() works for DELETE queries too
        Hint: The pattern is: prepare query → execute → check affected_rows
        
        Reference: Book.delete() in models/library.py - this method should be very similar!
        """
        # TODO: Implement this method following the steps above
        # Your code here
        pass


# ============================================================================
# Module-level documentation for students
# ============================================================================

"""
SUMMARY - Task Model Implementation Guide:

This module is a GUIDED EXERCISE where you implement CRUD operations for tasks.
You have one complete example (get_by_id) and several methods to implement yourself.

What's Provided:

1. COMPLETE REFERENCE (get_by_id):
   - Fully implemented method to study
   - Shows the complete pattern for READ operations
   - Use this as a reference when implementing other methods

2. PARTIAL IMPLEMENTATION (create):
   - Function signature and docstring provided
   - TODO comments with step-by-step instructions
   - Hints and examples for each step
   - Some code provided, you fill in the gaps

3. FUNCTION SIGNATURES (get_all, update_status, delete):
   - Complete docstrings explaining requirements
   - Implementation steps outlined in comments
   - References to similar methods in library system
   - You write the complete implementation

How to Approach This Exercise:

Step 1: Study the Reference
- Read get_by_id() carefully
- Understand each line and why it's there
- Compare it to Book.get_by_id() in models/library.py
- Note the pattern: query → execute → return result

Step 2: Complete the Partial Implementation
- Work on Task.create() first
- Follow the TODO comments step by step
- Implement the validation functions (validate_priority, validate_title_length)
- Test your implementation before moving on

Step 3: Implement the Function Signatures
- Start with Task.delete() (simplest)
- Then Task.update_status() (medium complexity)
- Finally Task.get_all() (most complex with optional filtering)
- Use the library system as a reference for each

Step 4: Test Your Implementation
- Create a simple test script to try each method
- Test success cases (valid input)
- Test error cases (invalid input, non-existent IDs)
- Make sure error messages are clear and helpful

Common Patterns to Remember:

CREATE Pattern:
1. Validate input
2. Prepare INSERT query with ? placeholders
3. Execute with execute_insert()
4. Return the new record's ID

READ Pattern:
1. Prepare SELECT query with optional WHERE
2. Execute with execute_query()
3. Return result(s) or None/empty list

UPDATE Pattern:
1. Validate input
2. Prepare UPDATE query with WHERE clause
3. Execute with execute_update()
4. Check affected_rows and return boolean

DELETE Pattern:
1. Prepare DELETE query with WHERE clause
2. Execute with execute_update()
3. Check affected_rows and return boolean

Key Principles:

✓ Always validate input before database operations
✓ Always use parameterized queries (? placeholders)
✓ Always handle errors with try-except
✓ Always provide clear error messages
✓ Return None for "not found" in get operations
✓ Return False for "not found" in update/delete operations
✓ Return empty list for "no results" in list operations

Getting Help:

If you get stuck:
1. Review the complete Book model in models/library.py
2. Look at the specific method that's similar to what you're implementing
3. Check the TODO comments for hints and steps
4. Make sure you understand the pattern before writing code
5. Test frequently - don't write all methods before testing

Next Steps:

After completing this module:
1. Test all your methods thoroughly
2. Try creating a simple script that uses your Task model
3. Experiment with different inputs and edge cases
4. Move on to implementing the Category model (optional challenge)
5. Try the Inventory system for independent practice

Remember: The goal is to learn the patterns, not just to complete the code.
Take your time, understand each step, and don't hesitate to refer back to
the library system examples. You're building real backend development skills!

Good luck! 🚀
"""


# ============================================================================
# Optional Challenge: Category Model
# ============================================================================

class Category:
    """
    Model class for Category entity - Optional Challenge.
    
    *** THIS IS AN OPTIONAL CHALLENGE FOR ADVANCED STUDENTS! ***
    
    If you've completed the Task model and want more practice, try implementing
    the Category model. This will help you organize tasks into groups.
    
    Database Table: categories
    Fields (if you completed the schema TODOs):
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - name: TEXT NOT NULL UNIQUE
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    Methods to Implement:
    - create(name: str) -> int
    - get_by_id(category_id: int) -> Optional[Dict[str, Any]]
    - get_all() -> List[Dict[str, Any]]
    - update(category_id: int, name: str) -> bool
    - delete(category_id: int) -> bool
    - get_tasks(category_id: int) -> List[Dict[str, Any]]  # Returns tasks in this category
    
    Hints:
    - Follow the same patterns as the Task model
    - Validate that category name is not empty
    - Handle the UNIQUE constraint on name (like ISBN in books)
    - The get_tasks() method will need a JOIN (like Loan.get_by_member())
    
    This is completely optional - only attempt if you're comfortable with
    the Task model implementation and want extra practice!
    """
    pass


# ============================================================================
# End of Module
# ============================================================================
