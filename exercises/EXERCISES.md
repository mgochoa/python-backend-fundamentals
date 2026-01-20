# Exercise Guide - Python Backend Learning Project

This guide provides detailed instructions, learning objectives, hints, and success criteria for all exercises in the project. Work through these exercises in order to build your backend development skills progressively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Beginner Exercises](#beginner-exercises)
3. [Intermediate Exercises](#intermediate-exercises)
4. [Advanced Exercises](#advanced-exercises)
5. [Challenge Exercises](#challenge-exercises)
6. [Tips and Troubleshooting](#tips-and-troubleshooting)

---

## Getting Started

### Prerequisites

Before starting the exercises:

1. ✅ Read `README.md` to understand the project structure
2. ✅ Read `CONCEPTS.md` to learn fundamental concepts
3. ✅ Run `python setup.py` to initialize the database
4. ✅ Run `python main.py` to see the Library System in action
5. ✅ Study `models/library.py` to understand the reference implementation

### Learning Path

The exercises are organized by difficulty:

- **Beginner**: Learn basic patterns with heavy guidance
- **Intermediate**: Apply patterns with moderate guidance
- **Advanced**: Implement features with minimal guidance
- **Challenge**: Design and implement independently

---

## Beginner Exercises

These exercises introduce you to basic CRUD operations and validation patterns. Each exercise has detailed step-by-step instructions.

### Exercise 1: Implement Validation Functions

**File**: `validation/exercises/todo_validators.py`

**Learning Objectives**:
- Understand input validation patterns
- Learn to raise appropriate exceptions
- Practice writing clear error messages

**Use Cases**: Supports UC-6 (Create a Task), UC-8 (Update Task Status)

**Tasks**:

#### 1.1: Implement `validate_priority()`

**What to do**: Create a function that validates task priority values.

**Requirements**:
- Accept one parameter: `priority` (string)
- Allowed values: "low", "medium", "high"
- Raise `ValidationError` if priority is not in allowed list
- Include helpful error message showing allowed values

**Hints**:
- Study `validate_status()` in the same file - it's almost identical!
- Use a list to store allowed values: `allowed_priorities = ["low", "medium", "high"]`
- Check if priority is in the list: `if priority not in allowed_priorities:`
- Error message format: `f"Priority must be one of: {', '.join(allowed_priorities)}"`

**Example**:
```python
def validate_priority(priority: str) -> None:
    allowed_priorities = ["low", "medium", "high"]
    if priority not in allowed_priorities:
        raise ValidationError(
            f"Priority must be one of: {', '.join(allowed_priorities)}. "
            f"Got: '{priority}'"
        )
```

**Success Criteria**:
- ✅ Function accepts valid priorities without error
- ✅ Function raises `ValidationError` for invalid priorities
- ✅ Error message clearly states allowed values
- ✅ Error message shows what value was provided

**Test Your Code**:
```python
# In Python REPL or test script
from validation.exercises.todo_validators import validate_priority
from utils.error_handlers import ValidationError

# Should work
validate_priority("low")
validate_priority("medium")
validate_priority("high")

# Should raise ValidationError
try:
    validate_priority("urgent")
    print("ERROR: Should have raised ValidationError")
except ValidationError as e:
    print(f"✓ Correctly raised error: {e}")
```

---

#### 1.2: Implement `validate_title_length()`

**What to do**: Create a function that validates task title length.

**Requirements**:
- Accept one parameter: `title` (string)
- Title must be at least 1 character (after stripping whitespace)
- Title must be at most 200 characters
- Raise `ValidationError` if length is invalid

**Hints**:
- Use `len(title)` to get the length
- Check minimum: `if len(title) < 1:`
- Check maximum: `if len(title) > 200:`
- Provide specific error messages for each case

**Example**:
```python
def validate_title_length(title: str) -> None:
    if len(title) < 1:
        raise ValidationError("Title must be at least 1 character")
    if len(title) > 200:
        raise ValidationError("Title must be at most 200 characters")
```

**Success Criteria**:
- ✅ Accepts titles between 1 and 200 characters
- ✅ Rejects empty titles
- ✅ Rejects titles over 200 characters
- ✅ Error messages specify the length requirement

**Test Your Code**:
```python
# Should work
validate_title_length("Buy milk")
validate_title_length("A" * 200)  # Exactly 200 characters

# Should raise ValidationError
try:
    validate_title_length("")
except ValidationError as e:
    print(f"✓ Correctly rejected empty title: {e}")

try:
    validate_title_length("A" * 201)  # Too long
except ValidationError as e:
    print(f"✓ Correctly rejected long title: {e}")
```

---

### Exercise 2: Complete Task.create()

**File**: `models/todo.py`

**Learning Objectives**:
- Implement CREATE operation with validation
- Use parameterized queries safely
- Handle database errors appropriately
- Return the ID of newly created records

**Use Case**: UC-6 (Create a Task)

**What to do**: Complete the `Task.create()` method by following the TODO comments.

**Requirements**:
1. Validate the title (not empty, correct length)
2. Prepare an INSERT query with parameterized values
3. Execute the query and return the new task ID
4. Handle errors gracefully

**Step-by-Step Guide**:

#### Step 1: Add Validation

Find the TODO comment for validation and add:

```python
try:
    validate_not_empty(title, "Title")
    validate_title_length(title)
except ValidationError as e:
    raise ValidationError(f"Invalid task data: {str(e)}")
```

**Why?**: Always validate input before database operations to catch errors early.

#### Step 2: Prepare the Query

The basic query is already provided:
```python
query = """
    INSERT INTO tasks (title, description)
    VALUES (?, ?, ?)
"""
```

**Note**: If you've completed the schema TODOs and added status/priority fields, you can enhance this:
```python
query = """
    INSERT INTO tasks (title, description, status, priority)
    VALUES (?, ?, ?, ?)
"""
```

#### Step 3: Execute and Return ID

Find the TODO for execution and complete:

```python
try:
    task_id = execute_insert(query, (title, description))
    return task_id
except QueryExecutionError as e:
    raise QueryExecutionError(f"Failed to create task: {str(e)}")
```

**Success Criteria**:
- ✅ Creates tasks with valid input
- ✅ Rejects empty titles
- ✅ Rejects titles over 200 characters
- ✅ Returns the ID of the new task
- ✅ Provides clear error messages

**Test Your Code**:
```python
from models.todo import Task

# Should work
task_id = Task.create("Buy groceries", "Milk, eggs, bread")
print(f"✓ Created task with ID: {task_id}")

# Should raise ValidationError
try:
    Task.create("", "Empty title")
    print("ERROR: Should have raised ValidationError")
except ValidationError as e:
    print(f"✓ Correctly rejected empty title: {e}")
```

---

## Intermediate Exercises

These exercises require you to apply the patterns you've learned with less guidance. You'll implement complete methods based on requirements and examples.

### Exercise 3: Implement Task.get_all()

**File**: `models/todo.py`

**Learning Objectives**:
- Implement READ operation with optional filtering
- Build dynamic SQL queries
- Handle query parameters correctly
- Return appropriate data structures

**Use Case**: UC-7 (List All Tasks)

**What to do**: Implement the `Task.get_all()` method that retrieves all tasks with optional status filtering.

**Requirements**:
1. Accept optional `status` parameter for filtering
2. Validate status if provided
3. Build query dynamically (with or without WHERE clause)
4. Sort results by created_at descending (newest first)
5. Return list of task dictionaries (empty list if no tasks)

**Implementation Guide**:

```python
@staticmethod
def get_all(status: str = None) -> List[Dict[str, Any]]:
    # Step 1: Validate status if provided
    if status is not None:
        try:
            validate_status(status)
        except ValidationError as e:
            raise ValidationError(f"Invalid status: {str(e)}")
    
    # Step 2: Build query dynamically
    query = "SELECT * FROM tasks"
    params = []
    
    if status is not None:
        query += " WHERE status = ?"
        params.append(status)
    
    query += " ORDER BY created_at DESC"
    
    # Step 3: Execute and return results
    try:
        results = execute_query(query, tuple(params))
        return results
    except QueryExecutionError as e:
        raise QueryExecutionError(f"Failed to retrieve tasks: {str(e)}")
```

**Hints**:
- Study `Book.get_all()` in `models/library.py` for the pattern
- Start with base query, then add WHERE clause conditionally
- Use a list for params, convert to tuple when executing
- Remember to validate the status parameter

**Success Criteria**:
- ✅ Returns all tasks when no status provided
- ✅ Filters by status when provided
- ✅ Rejects invalid status values
- ✅ Returns empty list when no tasks found
- ✅ Results are sorted newest first

**Test Your Code**:
```python
# Create some test tasks first
Task.create("Task 1", "Description 1")
Task.create("Task 2", "Description 2")

# Get all tasks
all_tasks = Task.get_all()
print(f"✓ Found {len(all_tasks)} tasks")

# Filter by status (if schema is complete)
pending = Task.get_all(status="pending")
print(f"✓ Found {len(pending)} pending tasks")

# Test invalid status
try:
    Task.get_all(status="invalid")
    print("ERROR: Should have raised ValidationError")
except ValidationError as e:
    print(f"✓ Correctly rejected invalid status: {e}")
```

---

### Exercise 4: Implement Task.update_status()

**File**: `models/todo.py`

**Learning Objectives**:
- Implement UPDATE operation
- Validate before updating
- Check if record exists
- Return boolean success indicator

**Use Case**: UC-8 (Update Task Status)

**What to do**: Implement the `Task.update_status()` method that changes a task's status.

**Requirements**:
1. Validate the new_status parameter
2. Execute UPDATE query with WHERE clause
3. Return True if task was updated, False if not found
4. Handle errors appropriately

**Implementation Guide**:

```python
@staticmethod
def update_status(task_id: int, new_status: str) -> bool:
    # Step 1: Validate new status
    try:
        validate_status(new_status)
    except ValidationError as e:
        raise ValidationError(f"Invalid status: {str(e)}")
    
    # Step 2: Prepare UPDATE query
    query = "UPDATE tasks SET status = ? WHERE id = ?"
    
    # Step 3: Execute and check affected rows
    try:
        affected_rows = execute_update(query, (new_status, task_id))
        return affected_rows > 0
    except QueryExecutionError as e:
        raise QueryExecutionError(f"Failed to update task: {str(e)}")
```

**Hints**:
- Study `Book.delete()` for the pattern of checking affected rows
- `execute_update()` returns the number of rows affected
- If 0 rows affected, the task_id didn't exist
- Always validate before executing the query

**Success Criteria**:
- ✅ Updates status for existing tasks
- ✅ Returns True when task is updated
- ✅ Returns False when task doesn't exist
- ✅ Rejects invalid status values
- ✅ Provides clear error messages

**Test Your Code**:
```python
# Create a test task
task_id = Task.create("Test task", "For testing")

# Update status
success = Task.update_status(task_id, "in_progress")
print(f"✓ Update {'succeeded' if success else 'failed'}")

# Verify update
task = Task.get_by_id(task_id)
print(f"✓ Status is now: {task['status']}")

# Try non-existent task
success = Task.update_status(99999, "completed")
print(f"✓ Non-existent task returned: {success}")  # Should be False

# Try invalid status
try:
    Task.update_status(task_id, "invalid")
    print("ERROR: Should have raised ValidationError")
except ValidationError as e:
    print(f"✓ Correctly rejected invalid status: {e}")
```

---

### Exercise 5: Implement Task.delete()

**File**: `models/todo.py`

**Learning Objectives**:
- Implement DELETE operation
- Use WHERE clause correctly
- Check if record was deleted
- Return boolean success indicator

**Use Case**: UC-9 (Delete a Task)

**What to do**: Implement the `Task.delete()` method that removes a task from the database.

**Requirements**:
1. Execute DELETE query with WHERE clause
2. Return True if task was deleted, False if not found
3. Handle errors appropriately

**Implementation Guide**:

```python
@staticmethod
def delete(task_id: int) -> bool:
    # Prepare DELETE query with WHERE clause
    query = "DELETE FROM tasks WHERE id = ?"
    
    # Execute and check affected rows
    try:
        affected_rows = execute_update(query, (task_id,))
        return affected_rows > 0
    except QueryExecutionError as e:
        raise QueryExecutionError(f"Failed to delete task: {str(e)}")
```

**Hints**:
- This is almost identical to `Book.delete()` in `models/library.py`
- ALWAYS include WHERE clause (without it, deletes ALL rows!)
- Use `execute_update()` for DELETE queries
- Check affected_rows to see if anything was deleted

**Success Criteria**:
- ✅ Deletes existing tasks
- ✅ Returns True when task is deleted
- ✅ Returns False when task doesn't exist
- ✅ Doesn't affect other tasks

**Test Your Code**:
```python
# Create a test task
task_id = Task.create("Task to delete", "Will be deleted")

# Verify it exists
task = Task.get_by_id(task_id)
print(f"✓ Task exists: {task['title']}")

# Delete it
success = Task.delete(task_id)
print(f"✓ Delete {'succeeded' if success else 'failed'}")

# Verify it's gone
task = Task.get_by_id(task_id)
print(f"✓ Task after delete: {task}")  # Should be None

# Try deleting non-existent task
success = Task.delete(99999)
print(f"✓ Non-existent task returned: {success}")  # Should be False
```

---

## Advanced Exercises

These exercises require you to design and implement features with minimal guidance. You'll need to make decisions about implementation details.

### Exercise 6: Implement Category System

**Files**: `database/schemas/todo_schema.sql`, `models/todo.py`

**Learning Objectives**:
- Design database schema for relationships
- Implement foreign key relationships
- Create complete CRUD operations independently
- Handle related data appropriately

**Use Case**: UC-10 (Organize Tasks by Category)

**What to do**: Add category support to the Todo System.

**Requirements**:

#### Part 1: Design the Schema

Add to `database/schemas/todo_schema.sql`:

```sql
-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add category_id to tasks table
-- (You may need to recreate the tasks table or use ALTER TABLE)
ALTER TABLE tasks ADD COLUMN category_id INTEGER REFERENCES categories(id);
```

#### Part 2: Implement Category Model

In `models/todo.py`, implement the `Category` class:

**Methods to implement**:
1. `create(name, description=None)` - Create a new category
2. `get_by_id(category_id)` - Get category by ID
3. `get_all()` - Get all categories
4. `update(category_id, **kwargs)` - Update category
5. `delete(category_id)` - Delete category
6. `get_tasks(category_id)` - Get all tasks in a category

**Hints**:
- Follow the same patterns as the Task model
- Validate that category name is not empty and is unique
- For `get_tasks()`, use a JOIN or WHERE clause
- Consider what happens when you delete a category with tasks

**Success Criteria**:
- ✅ Can create categories with unique names
- ✅ Can retrieve categories by ID and get all
- ✅ Can update category information
- ✅ Can delete categories
- ✅ Can get all tasks in a category
- ✅ Handles errors appropriately

**Test Your Code**:
```python
from models.todo import Category, Task

# Create categories
work_id = Category.create("Work", "Work-related tasks")
personal_id = Category.create("Personal", "Personal tasks")

# Create tasks with categories
task1 = Task.create("Finish report", "Q4 analysis", category_id=work_id)
task2 = Task.create("Buy groceries", "Milk, eggs", category_id=personal_id)

# Get tasks by category
work_tasks = Category.get_tasks(work_id)
print(f"✓ Found {len(work_tasks)} work tasks")
```

---

### Exercise 7: Add Task Search and Filtering

**File**: `models/todo.py`

**Learning Objectives**:
- Implement complex queries with multiple filters
- Use LIKE for text search
- Combine multiple WHERE conditions
- Handle optional parameters

**What to do**: Add a `Task.search()` method with multiple filter options.

**Requirements**:
1. Search by title (partial match, case-insensitive)
2. Filter by status (optional)
3. Filter by priority (optional)
4. Filter by category (optional)
5. Sort results appropriately

**Implementation Guide**:

```python
@staticmethod
def search(search_term: str = None, status: str = None, 
           priority: str = None, category_id: int = None) -> List[Dict[str, Any]]:
    """
    Search and filter tasks.
    
    Args:
        search_term: Search in title (partial match)
        status: Filter by status
        priority: Filter by priority
        category_id: Filter by category
    
    Returns:
        List of matching tasks
    """
    # Build query dynamically
    query = "SELECT * FROM tasks WHERE 1=1"  # 1=1 makes adding conditions easier
    params = []
    
    if search_term:
        query += " AND title LIKE ?"
        params.append(f"%{search_term}%")
    
    if status:
        validate_status(status)
        query += " AND status = ?"
        params.append(status)
    
    if priority:
        validate_priority(priority)
        query += " AND priority = ?"
        params.append(priority)
    
    if category_id:
        query += " AND category_id = ?"
        params.append(category_id)
    
    query += " ORDER BY created_at DESC"
    
    try:
        return execute_query(query, tuple(params))
    except QueryExecutionError as e:
        raise QueryExecutionError(f"Failed to search tasks: {str(e)}")
```

**Success Criteria**:
- ✅ Searches by title with partial matches
- ✅ Filters by status, priority, category
- ✅ Combines multiple filters correctly
- ✅ Returns empty list when no matches
- ✅ Validates filter values

---

## Challenge Exercises

These exercises require you to design and implement complete systems independently. Minimal guidance is provided.

### Exercise 8: Implement Inventory System

**Files**: `database/schemas/inventory_schema.sql`, `models/inventory.py`

**Learning Objectives**:
- Design complete database schema independently
- Implement complex relationships (one-to-many, many-to-many)
- Add business logic (stock management)
- Handle edge cases and constraints

**Use Cases**: UC-11 through UC-15 (all Inventory System use cases)

**What to do**: Design and implement the complete Inventory Management System.

**Requirements**:

#### Part 1: Design the Schema

Create tables for:
1. **products**: id, name, description, price, stock_quantity, supplier_id, created_at, updated_at
2. **categories**: id, name, description, created_at
3. **suppliers**: id, name, contact_name, contact_email, contact_phone, address, created_at
4. **product_categories**: product_id, category_id (junction table for many-to-many)

**Constraints to consider**:
- Product names should be unique
- Prices must be positive
- Stock quantities must be non-negative
- Category names should be unique
- Supplier names should be unique
- Foreign keys with appropriate ON DELETE behavior

#### Part 2: Implement Product Model

Methods to implement:
1. `create()` - Add new product with validation
2. `get_by_id()` - Retrieve product by ID
3. `get_all()` - Get all products with optional filters
4. `get_by_supplier()` - Get products from a supplier
5. `get_low_stock()` - Get products below threshold
6. `update()` - Update product fields
7. `update_stock()` - Adjust stock quantity (prevent negative)
8. `delete()` - Remove product
9. `add_category()` - Link product to category
10. `remove_category()` - Unlink product from category
11. `get_categories()` - Get all categories for a product

#### Part 3: Implement Category Model

Methods to implement:
1. `create()` - Add new category
2. `get_by_id()` - Retrieve category
3. `get_all()` - Get all categories
4. `update()` - Update category
5. `delete()` - Remove category
6. `get_products()` - Get all products in category

#### Part 4: Implement Supplier Model

Methods to implement:
1. `create()` - Add new supplier
2. `get_by_id()` - Retrieve supplier
3. `get_all()` - Get all suppliers
4. `update()` - Update supplier
5. `delete()` - Remove supplier
6. `get_products()` - Get all products from supplier

**Hints**:
- Study the Library and Todo systems for patterns
- Start with the simplest operations (create, get_by_id)
- Test each method before moving to the next
- Handle the many-to-many relationship carefully
- Add business logic for stock management (prevent negative stock)
- Consider what happens when deleting records with relationships

**Success Criteria**:
- ✅ Complete schema with all tables and relationships
- ✅ All CRUD operations work correctly
- ✅ Stock management prevents negative quantities
- ✅ Many-to-many relationships work properly
- ✅ Low stock alerts function correctly
- ✅ Comprehensive error handling
- ✅ Clear validation messages

**Test Scenarios**:

```python
from models.inventory import Product, Category, Supplier

# Create supplier
supplier_id = Supplier.create(
    name="Tech Supplies Inc",
    contact_email="contact@techsupplies.com"
)

# Create category
electronics_id = Category.create("Electronics", "Electronic devices")

# Create product
product_id = Product.create(
    name="Wireless Mouse",
    description="Ergonomic wireless mouse",
    price=29.99,
    stock_quantity=50,
    supplier_id=supplier_id
)

# Add to category
Product.add_category(product_id, electronics_id)

# Update stock (sell 5 units)
Product.update_stock(product_id, -5)

# Check low stock
low_stock = Product.get_low_stock(threshold=100)
for product in low_stock:
    print(f"{product['name']}: {product['stock_quantity']} units")

# Get products by category
electronics = Category.get_products(electronics_id)
print(f"Found {len(electronics)} electronic products")
```

---

### Exercise 9: Add Due Dates and Reminders

**File**: `models/todo.py`

**Learning Objectives**:
- Work with date/time data
- Implement date-based queries
- Add computed fields
- Handle date validation

**What to do**: Add due date functionality to tasks.

**Requirements**:
1. Add `due_date` field to tasks table
2. Implement `set_due_date()` method
3. Implement `get_overdue()` method
4. Implement `get_due_soon()` method (within X days)
5. Validate that due dates are not in the past

**Hints**:
- Use Python's `datetime` module
- Store dates in ISO format (YYYY-MM-DD)
- Compare dates using SQL: `WHERE due_date < CURRENT_DATE`
- Consider time zones if needed

---

### Exercise 10: Add User Authentication (Advanced Challenge)

**Files**: New files in `models/` and `database/schemas/`

**Learning Objectives**:
- Design user authentication system
- Hash passwords securely
- Implement user sessions
- Add authorization checks

**What to do**: Add user accounts and authentication.

**Requirements**:
1. Create users table with hashed passwords
2. Implement user registration
3. Implement user login
4. Associate tasks with users
5. Ensure users can only see their own tasks

**Security Considerations**:
- NEVER store passwords in plain text
- Use bcrypt or similar for password hashing
- Validate password strength
- Implement session management

**Note**: This is an advanced exercise requiring additional libraries and security knowledge.

---

## Tips and Troubleshooting

### General Tips

1. **Read Error Messages**: They tell you exactly what's wrong
2. **Test Incrementally**: Test each method as you write it
3. **Use the REPL**: Python's interactive shell is great for testing
4. **Study Examples**: The Library System shows all the patterns
5. **Start Simple**: Get basic functionality working before adding features
6. **Ask Questions**: Review documentation and examples when stuck

### Common Issues

#### "No such table" Error
- Run `python setup.py` to create tables
- Check that your schema file has valid SQL
- Verify the table name matches your queries

#### "UNIQUE constraint failed"
- You're trying to create a duplicate record
- Check for existing records before inserting
- Handle `DuplicateError` appropriately

#### "FOREIGN KEY constraint failed"
- Referenced record doesn't exist
- Create parent records before child records
- Check that foreign key IDs are valid

#### Validation Errors
- Read the error message - it tells you what's wrong
- Check that required fields are not empty
- Verify values are in allowed ranges
- Ensure data types match expectations

### Debugging Strategies

1. **Print Statements**: Add print statements to see what's happening
   ```python
   print(f"Query: {query}")
   print(f"Params: {params}")
   ```

2. **Test in REPL**: Try operations interactively
   ```python
   >>> from models.todo import Task
   >>> task = Task.get_by_id(1)
   >>> print(task)
   ```

3. **Check the Database**: Use a SQLite browser to inspect data
   - DB Browser for SQLite (free tool)
   - View tables, run queries, check constraints

4. **Simplify**: If something doesn't work, simplify it
   - Remove optional parameters
   - Test with minimal data
   - Add complexity gradually

### Getting Help

If you're stuck:

1. Review the relevant section in `CONCEPTS.md`
2. Study the similar method in `models/library.py`
3. Check the TODO comments for hints
4. Test with simple inputs first
5. Read error messages carefully
6. Ask your instructor or mentor

---

## Summary

You now have a complete guide to all exercises in the project:

- **Beginner**: Validation functions and Task.create()
- **Intermediate**: Task.get_all(), update_status(), delete()
- **Advanced**: Category system, search and filtering
- **Challenge**: Complete Inventory System, due dates, authentication

**Remember**:
- Work through exercises in order
- Test each method before moving on
- Study the reference implementations
- Don't be afraid to make mistakes - that's how you learn!

**Next Steps**:
1. Complete the beginner exercises
2. Test your implementations thoroughly
3. Move on to intermediate exercises
4. Challenge yourself with advanced exercises
5. Build something new with your skills!

---

**Happy Coding! 🚀**
