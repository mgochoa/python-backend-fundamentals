"""
Todo System Models - Complete Solution

This is the COMPLETE SOLUTION for the Todo System guided exercise.
Students should attempt to implement models/todo.py themselves before
looking at this solution.

This solution demonstrates:
- Complete CRUD operations for the Task model
- Proper input validation before database operations
- Comprehensive error handling with clear messages
- Use of parameterized queries to prevent SQL injection
- Consistent patterns across all operations
- Clear documentation and comments explaining the approach

Learning Value:
- Compare your implementation to this solution
- Understand different approaches to solving the same problem
- Learn best practices for backend development
- See how all the pieces fit together

Note: This solution assumes the todo_schema.sql has been completed with
status, priority, and due_date fields. If your schema is incomplete,
some parts may need adjustment.

Requirements Addressed:
- Requirement 8.3: Complete implementation for reference
- Requirement 3.1: All CRUD operations implemented
- Requirement 5.2: Validation before database operations
- Requirement 6.1: Comprehensive error handling

IMPORTANT: This solution file is meant for reference and study.
To use it in your project, you would integrate the patterns into models/todo.py
"""

import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# Import database connection utilities
# Note: These imports assume you're running from the project root directory
try:
    from database.connection import execute_query, execute_insert, execute_update, QueryExecutionError
except ModuleNotFoundError:
    # If running from a different directory, provide a helpful message
    import sys
    import os
    print("Note: This solution file should be studied, not run directly.")
    print("The patterns shown here should be integrated into models/todo.py")
    print("To test the Todo system, use the main.py or test files from the project root.")
    sys.exit(0)


# ============================================================================
# Custom Exception Classes
# ============================================================================

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


class DuplicateError(Exception):
    """Raised when attempting to create a record that already exists."""
    pass


class NotFoundError(Exception):
    """Raised when a requested record doesn't exist."""
    pass


# ============================================================================
# Validation Helper Functions
# ============================================================================

def validate_not_empty(value: str, field_name: str) -> None:
    """
    Validate that a string field is not empty or whitespace-only.
    
    Args:
        value: The string to validate
        field_name: Name of the field (for error messages)
        
    Raises:
        ValidationError: If value is None, empty, or only whitespace
    """
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")


def validate_status(status: str) -> None:
    """
    Validate that status is one of the allowed values.
    
    Args:
        status: The status value to validate
        
    Raises:
        ValidationError: If status is not one of the allowed values
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
    
    SOLUTION: This implements the validation pattern for priority.
    
    Args:
        priority: The priority value to validate
        
    Raises:
        ValidationError: If priority is not one of the allowed values
    """
    # Define the allowed priority values
    allowed_priorities = ["low", "medium", "high"]
    
    # Check if the provided priority is in the allowed list
    if priority not in allowed_priorities:
        # Raise a clear error message showing what values are allowed
        raise ValidationError(
            f"Priority must be one of: {', '.join(allowed_priorities)}. "
            f"Got: '{priority}'"
        )


def validate_title_length(title: str) -> None:
    """
    Validate that title length is within acceptable range.
    
    SOLUTION: This checks both minimum and maximum length constraints.
    
    Args:
        title: The title to validate
        
    Raises:
        ValidationError: If title length is invalid
    """
    # Check minimum length (at least 1 character after stripping)
    if len(title.strip()) < 1:
        raise ValidationError("Title must be at least 1 character long")
    
    # Check maximum length (at most 200 characters)
    if len(title) > 200:
        raise ValidationError("Title must be at most 200 characters long")


def validate_due_date(due_date: str) -> None:
    """
    Validate that due_date is in the correct format and is a valid date.
    
    BONUS: This is an additional validation not required in the exercise.
    It shows how to validate date formats.
    
    Args:
        due_date: Date string in YYYY-MM-DD format
        
    Raises:
        ValidationError: If date format is invalid
    """
    try:
        # Try to parse the date string
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Due date must be in YYYY-MM-DD format")


# ============================================================================
# Task Model Class - Complete Implementation
# ============================================================================

class Task:
    """
    Complete implementation of the Task model with all CRUD operations.
    
    This solution demonstrates best practices for:
    - Input validation before database operations
    - Parameterized queries for security
    - Error handling with clear messages
    - Consistent patterns across all methods
    - Comprehensive documentation
    """
    
    @staticmethod
    def get_by_id(task_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single task by its ID.
        
        This method is the same as in the exercise file - it's provided
        as a complete reference example.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            Dictionary containing task data if found, None if not found
            
        Raises:
            QueryExecutionError: If database operation fails
        """
        query = "SELECT * FROM tasks WHERE id = ?"
        
        try:
            results = execute_query(query, (task_id,))
            return results[0] if results else None
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve task: {str(e)}")
    
    @staticmethod
    def create(
        title: str,
        description: str = None,
        status: str = "pending",
        priority: str = "medium",
        due_date: str = None
    ) -> int:
        """
        Create a new task record in the database.
        
        SOLUTION: This is the complete implementation of the create method.
        
        Key points in this solution:
        1. All validation happens BEFORE the database operation
        2. We use try-except to catch validation errors and add context
        3. The query uses ? placeholders for all values
        4. We return the ID of the newly created task
        5. Error messages are clear and helpful
        
        Args:
            title: Task title (required, 1-200 characters)
            description: Detailed description (optional)
            status: Task status (default: "pending")
            priority: Task priority (default: "medium")
            due_date: Due date in YYYY-MM-DD format (optional)
            
        Returns:
            int: The ID of the newly created task
            
        Raises:
            ValidationError: If any input validation fails
            QueryExecutionError: If database operation fails
        """
        # ====================================================================
        # STEP 1: Validate all inputs
        # ====================================================================
        # We validate everything before touching the database.
        # This prevents invalid data from ever reaching the database.
        
        try:
            # Validate title (required field)
            validate_not_empty(title, "Title")
            validate_title_length(title)
            
            # Validate status (must be one of allowed values)
            validate_status(status)
            
            # Validate priority (must be one of allowed values)
            validate_priority(priority)
            
            # Validate due_date if provided (optional field)
            if due_date is not None:
                validate_due_date(due_date)
                
        except ValidationError as e:
            # Re-raise with additional context
            # This helps identify that the error came from task creation
            raise ValidationError(f"Invalid task data: {str(e)}")
        
        # ====================================================================
        # STEP 2: Prepare the SQL INSERT query
        # ====================================================================
        # We use ? placeholders for all values to prevent SQL injection.
        # NEVER use f-strings or string concatenation for SQL queries!
        
        query = """
            INSERT INTO tasks (title, description, status, priority, due_date)
            VALUES (?, ?, ?, ?, ?)
        """
        
        # ====================================================================
        # STEP 3: Execute the query and return the new task ID
        # ====================================================================
        # We wrap the database operation in try-except to handle errors.
        
        try:
            # Execute the insert and get the new task's ID
            task_id = execute_insert(query, (title, description, status, priority, due_date))
            return task_id
            
        except QueryExecutionError as e:
            # Provide context about what operation failed
            raise QueryExecutionError(f"Failed to create task: {str(e)}")
    
    @staticmethod
    def get_all(status: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks, optionally filtered by status.
        
        SOLUTION: This demonstrates dynamic query building with optional filtering.
        
        Key points in this solution:
        1. We validate the status parameter if it's provided
        2. We build the query dynamically based on whether filtering is needed
        3. We use a list for parameters and convert to tuple when executing
        4. We always sort by created_at descending (newest first)
        5. We return an empty list if no tasks are found (not None)
        
        Args:
            status: Optional status filter
            
        Returns:
            List of task dictionaries, empty list if no tasks found
            
        Raises:
            ValidationError: If status is provided but invalid
            QueryExecutionError: If database operation fails
        """
        # ====================================================================
        # STEP 1: Validate the status parameter if provided
        # ====================================================================
        if status is not None:
            try:
                validate_status(status)
            except ValidationError as e:
                raise ValidationError(f"Invalid filter: {str(e)}")
        
        # ====================================================================
        # STEP 2: Build the query dynamically
        # ====================================================================
        # Start with the base query
        query = "SELECT * FROM tasks"
        
        # Add WHERE clause if filtering by status
        params = []
        if status is not None:
            query += " WHERE status = ?"
            params.append(status)
        
        # Always sort by created_at descending (newest first)
        query += " ORDER BY created_at DESC"
        
        # ====================================================================
        # STEP 3: Execute the query and return results
        # ====================================================================
        try:
            # Convert params list to tuple for execute_query
            results = execute_query(query, tuple(params))
            return results  # Returns empty list [] if no results
            
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve tasks: {str(e)}")
    
    @staticmethod
    def update_status(task_id: int, new_status: str) -> bool:
        """
        Update the status of a task.
        
        SOLUTION: This demonstrates a simple UPDATE operation with validation.
        
        Key points in this solution:
        1. We validate the new status before updating
        2. We use an UPDATE query with WHERE clause
        3. We check affected_rows to see if the task existed
        4. We return True/False instead of raising an exception for "not found"
        5. This is a common pattern: return boolean for success/failure
        
        Args:
            task_id: ID of the task to update
            new_status: New status value
            
        Returns:
            bool: True if task was updated, False if task not found
            
        Raises:
            ValidationError: If new_status is invalid
            QueryExecutionError: If database operation fails
        """
        # ====================================================================
        # STEP 1: Validate the new status
        # ====================================================================
        try:
            validate_status(new_status)
        except ValidationError as e:
            raise ValidationError(f"Invalid status: {str(e)}")
        
        # ====================================================================
        # STEP 2: Prepare the UPDATE query
        # ====================================================================
        # Update the status field for the task with the given ID
        query = """
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """
        
        # ====================================================================
        # STEP 3: Execute the update and check if task was found
        # ====================================================================
        try:
            # Execute the update
            affected_rows = execute_update(query, (new_status, task_id))
            
            # If affected_rows is 0, the task_id didn't exist
            # If affected_rows is 1, the task was updated successfully
            return affected_rows > 0
            
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to update task status: {str(e)}")
    
    @staticmethod
    def update(task_id: int, **kwargs) -> bool:
        """
        Update multiple fields of a task.
        
        BONUS: This is an advanced method that allows updating any combination
        of fields. This demonstrates dynamic UPDATE query building.
        
        Args:
            task_id: ID of the task to update
            **kwargs: Field names and values to update
                     Allowed fields: title, description, status, priority, due_date
            
        Returns:
            bool: True if task was updated, False if task not found
            
        Raises:
            ValidationError: If any field validation fails
            QueryExecutionError: If database operation fails
            
        Example:
            # Update just the title
            Task.update(1, title="New title")
            
            # Update multiple fields
            Task.update(1, title="New title", status="completed", priority="high")
        """
        # Define allowed fields that can be updated
        allowed_fields = ["title", "description", "status", "priority", "due_date"]
        
        # Filter kwargs to only include allowed fields
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            raise ValidationError("No valid fields provided for update")
        
        # Validate each field being updated
        try:
            if "title" in updates:
                validate_not_empty(updates["title"], "Title")
                validate_title_length(updates["title"])
            
            if "status" in updates:
                validate_status(updates["status"])
            
            if "priority" in updates:
                validate_priority(updates["priority"])
            
            if "due_date" in updates and updates["due_date"] is not None:
                validate_due_date(updates["due_date"])
                
        except ValidationError as e:
            raise ValidationError(f"Invalid update data: {str(e)}")
        
        # Build the UPDATE query dynamically
        set_clauses = [f"{field} = ?" for field in updates.keys()]
        query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = ?"
        
        # Build parameters list: field values + task_id
        params = list(updates.values()) + [task_id]
        
        try:
            affected_rows = execute_update(query, tuple(params))
            return affected_rows > 0
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to update task: {str(e)}")
    
    @staticmethod
    def delete(task_id: int) -> bool:
        """
        Delete a task record from the database.
        
        SOLUTION: This demonstrates a simple DELETE operation.
        
        Key points in this solution:
        1. DELETE queries are simple but dangerous - always use WHERE!
        2. We check affected_rows to see if the task existed
        3. We return True/False for success/failure
        4. No validation needed - we're just deleting by ID
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            bool: True if task was deleted, False if task not found
            
        Raises:
            QueryExecutionError: If database operation fails
        """
        # ====================================================================
        # STEP 1: Prepare the DELETE query
        # ====================================================================
        # CRITICAL: Always include WHERE clause!
        # DELETE without WHERE would delete ALL tasks!
        query = "DELETE FROM tasks WHERE id = ?"
        
        # ====================================================================
        # STEP 2: Execute the deletion and check if task was found
        # ====================================================================
        try:
            # Execute the delete
            affected_rows = execute_update(query, (task_id,))
            
            # If affected_rows is 0, the task_id didn't exist
            # If affected_rows is 1, the task was deleted successfully
            return affected_rows > 0
            
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to delete task: {str(e)}")
    
    @staticmethod
    def get_by_priority(priority: str) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks with a specific priority.
        
        BONUS: This is an additional method showing another filtering pattern.
        
        Args:
            priority: Priority level to filter by
            
        Returns:
            List of task dictionaries
            
        Raises:
            ValidationError: If priority is invalid
            QueryExecutionError: If database operation fails
        """
        # Validate the priority
        try:
            validate_priority(priority)
        except ValidationError as e:
            raise ValidationError(f"Invalid priority: {str(e)}")
        
        # Query for tasks with the specified priority
        query = """
            SELECT * FROM tasks
            WHERE priority = ?
            ORDER BY created_at DESC
        """
        
        try:
            results = execute_query(query, (priority,))
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve tasks by priority: {str(e)}")
    
    @staticmethod
    def get_overdue() -> List[Dict[str, Any]]:
        """
        Retrieve all tasks that are overdue (due_date in the past and not completed).
        
        BONUS: This demonstrates date comparison in SQL queries.
        
        Returns:
            List of overdue task dictionaries
            
        Raises:
            QueryExecutionError: If database operation fails
        """
        query = """
            SELECT * FROM tasks
            WHERE due_date < date('now')
            AND status != 'completed'
            ORDER BY due_date ASC
        """
        
        try:
            results = execute_query(query, ())
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve overdue tasks: {str(e)}")


# ============================================================================
# Category Model - Optional Challenge Solution
# ============================================================================

class Category:
    """
    Complete implementation of the Category model.
    
    BONUS: This is the solution for the optional Category challenge.
    It demonstrates relationships between tables using foreign keys.
    """
    
    @staticmethod
    def create(name: str) -> int:
        """
        Create a new category.
        
        Args:
            name: Category name (required, must be unique)
            
        Returns:
            int: The ID of the newly created category
            
        Raises:
            ValidationError: If name is empty
            DuplicateError: If category name already exists
            QueryExecutionError: If database operation fails
        """
        # Validate the name
        try:
            validate_not_empty(name, "Category name")
        except ValidationError as e:
            raise ValidationError(f"Invalid category data: {str(e)}")
        
        # Prepare the INSERT query
        query = "INSERT INTO categories (name) VALUES (?)"
        
        try:
            category_id = execute_insert(query, (name,))
            return category_id
        except sqlite3.IntegrityError:
            # UNIQUE constraint failed - category name already exists
            raise DuplicateError(f"Category '{name}' already exists")
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to create category: {str(e)}")
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a category by ID."""
        query = "SELECT * FROM categories WHERE id = ?"
        
        try:
            results = execute_query(query, (category_id,))
            return results[0] if results else None
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve category: {str(e)}")
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Retrieve all categories."""
        query = "SELECT * FROM categories ORDER BY name"
        
        try:
            results = execute_query(query, ())
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve categories: {str(e)}")
    
    @staticmethod
    def get_tasks(category_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks in a specific category.
        
        This demonstrates a JOIN operation between tasks and categories.
        
        Args:
            category_id: ID of the category
            
        Returns:
            List of task dictionaries in this category
            
        Raises:
            QueryExecutionError: If database operation fails
        """
        query = """
            SELECT tasks.*
            FROM tasks
            WHERE tasks.category_id = ?
            ORDER BY tasks.created_at DESC
        """
        
        try:
            results = execute_query(query, (category_id,))
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve tasks for category: {str(e)}")
    
    @staticmethod
    def delete(category_id: int) -> bool:
        """
        Delete a category.
        
        Note: This will fail if there are tasks assigned to this category
        due to foreign key constraints. You would need to either:
        1. Delete or reassign all tasks first
        2. Use ON DELETE CASCADE in the schema
        3. Set category_id to NULL in tasks (if allowed)
        
        Args:
            category_id: ID of the category to delete
            
        Returns:
            bool: True if deleted, False if not found
            
        Raises:
            QueryExecutionError: If database operation fails (e.g., foreign key constraint)
        """
        query = "DELETE FROM categories WHERE id = ?"
        
        try:
            affected_rows = execute_update(query, (category_id,))
            return affected_rows > 0
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to delete category: {str(e)}")


# ============================================================================
# Solution Summary and Learning Notes
# ============================================================================

"""
SOLUTION SUMMARY:

This complete solution demonstrates all the key concepts for the Todo System:

1. **CRUD Operations**:
   - CREATE: Task.create() with full validation
   - READ: Task.get_by_id(), Task.get_all() with optional filtering
   - UPDATE: Task.update_status() for simple updates, Task.update() for complex updates
   - DELETE: Task.delete() with proper error handling

2. **Validation Patterns**:
   - Always validate BEFORE database operations
   - Use specific validation functions for each field type
   - Provide clear, helpful error messages
   - Re-raise exceptions with additional context

3. **Query Patterns**:
   - Always use parameterized queries (? placeholders)
   - Build queries dynamically when needed (optional filtering)
   - Use ORDER BY for consistent result ordering
   - Check affected_rows to determine success

4. **Error Handling**:
   - Wrap database operations in try-except
   - Catch specific exceptions (ValidationError, QueryExecutionError)
   - Provide context in error messages
   - Return False for "not found" instead of raising exceptions

5. **Code Organization**:
   - Group related functions together
   - Use clear, descriptive names
   - Document with comprehensive docstrings
   - Include examples in documentation

Key Differences from the Exercise File:

- All TODO sections are completed with working code
- Validation functions (validate_priority, validate_title_length) are implemented
- All CRUD methods (get_all, update_status, delete) are fully implemented
- Additional bonus methods are included (update, get_by_priority, get_overdue)
- Category model is included as an optional challenge solution

How to Use This Solution:

1. **Compare**: Look at your implementation vs. this solution
2. **Understand**: Read the comments to understand the approach
3. **Learn**: Identify patterns you can apply to other models
4. **Experiment**: Try modifying this code to add new features
5. **Practice**: Use these patterns in the Inventory system challenge

Next Steps:

- Test this solution with various inputs
- Try adding new methods (e.g., search by title, bulk operations)
- Implement the Category model if you haven't already
- Move on to the Inventory system for independent practice
- Consider adding more advanced features (pagination, sorting options)

Remember: There are often multiple correct ways to implement these operations.
This solution shows one approach, but your solution might be different and
equally valid. The key is understanding the patterns and principles!
"""
