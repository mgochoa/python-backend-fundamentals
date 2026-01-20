# Design Document: Python Backend Learning Project

## Overview

The Python Backend Learning Project is an educational scaffolding system designed to teach beginners Python and SQL fundamentals through hands-on practice. The system provides a structured learning environment with three distinct topic areas at varying complexity levels: a complete reference implementation (Library System), a guided implementation with exercises (Todo App), and a challenge implementation (Inventory Management).

The project uses SQLite for database operations and provides simple Python scripts or optional CLI/API interfaces for interaction. The design emphasizes clarity, progressive difficulty, and comprehensive documentation to support self-directed learning.

### Learning Philosophy

The project follows a "learn by doing" approach with three levels of support:
1. **Reference Level**: Complete working implementation students can study
2. **Guided Level**: Partial implementation with clear TODOs and scaffolding
3. **Challenge Level**: Minimal scaffolding for independent practice

## Use Cases for Students

These use cases describe what students will be able to build and learn through this project. Each use case is written in agile user story format and maps to specific learning objectives.

### Library System Use Cases (Reference Implementation - Study These)

**UC-1: Add a Book to the Library**
- **As a** librarian
- **I want to** add new books to the library database
- **So that** patrons can discover and borrow them
- **Acceptance Criteria:**
  - Book must have title, author, and ISBN
  - ISBN must be unique
  - System validates all required fields
  - System returns confirmation with book ID
- **Learning Objectives:** INSERT operations, data validation, unique constraints

**UC-2: Search for Books**
- **As a** patron
- **I want to** search for books by title or author
- **So that** I can find books I'm interested in
- **Acceptance Criteria:**
  - Search works with partial matches
  - Results are sorted alphabetically
  - Shows availability status
- **Learning Objectives:** SELECT queries, WHERE clauses, ORDER BY, filtering

**UC-3: Borrow a Book**
- **As a** patron
- **I want to** borrow an available book
- **So that** I can read it
- **Acceptance Criteria:**
  - Only available books can be borrowed
  - System records loan date and due date
  - Book status changes to unavailable
  - System links loan to patron and book
- **Learning Objectives:** UPDATE operations, foreign keys, relationships, transactions

**UC-4: Return a Book**
- **As a** patron
- **I want to** return a borrowed book
- **So that** others can borrow it
- **Acceptance Criteria:**
  - System records return date
  - Book status changes to available
  - Loan record is updated
- **Learning Objectives:** UPDATE operations, date handling

**UC-5: View Patron Borrowing History**
- **As a** librarian
- **I want to** see all books a patron has borrowed
- **So that** I can track their borrowing activity
- **Acceptance Criteria:**
  - Shows all loans for a specific patron
  - Includes book details
  - Shows loan dates and return dates
  - Sorted by most recent first
- **Learning Objectives:** JOIN operations, multi-table queries

### Todo System Use Cases (Guided Implementation - You Build These)

**UC-6: Create a Task**
- **As a** user
- **I want to** create a new task with a title and description
- **So that** I can track things I need to do
- **Acceptance Criteria:**
  - Task must have a non-empty title
  - Description is optional
  - Task starts with 'pending' status
  - Task has a priority (low/medium/high)
  - System returns task ID
- **Learning Objectives:** INSERT operations, default values, validation
- **Implementation Status:** TODO - Students implement with guidance

**UC-7: List All Tasks**
- **As a** user
- **I want to** see all my tasks
- **So that** I know what I need to do
- **Acceptance Criteria:**
  - Shows all tasks with their details
  - Can filter by status (pending/in_progress/completed)
  - Sorted by creation date (newest first)
- **Learning Objectives:** SELECT queries, optional filtering, sorting
- **Implementation Status:** TODO - Students implement with guidance

**UC-8: Update Task Status**
- **As a** user
- **I want to** mark a task as in progress or completed
- **So that** I can track my progress
- **Acceptance Criteria:**
  - Can change status to any valid value
  - System validates status values
  - Returns error if task doesn't exist
- **Learning Objectives:** UPDATE operations, validation, error handling
- **Implementation Status:** TODO - Students implement with guidance

**UC-9: Delete a Task**
- **As a** user
- **I want to** delete a task I no longer need
- **So that** my task list stays clean
- **Acceptance Criteria:**
  - Task is permanently removed
  - Returns success if deleted
  - Returns error if task doesn't exist
- **Learning Objectives:** DELETE operations, error handling
- **Implementation Status:** TODO - Students implement with guidance

**UC-10: Organize Tasks by Category**
- **As a** user
- **I want to** assign tasks to categories
- **So that** I can organize related tasks together
- **Acceptance Criteria:**
  - Can create categories
  - Can assign a task to a category
  - Can list tasks by category
  - Can list all categories
- **Learning Objectives:** Foreign keys, relationships, JOIN operations
- **Implementation Status:** TODO - Students design and implement

### Inventory System Use Cases (Challenge Implementation - Design and Build Yourself)

**UC-11: Add a Product**
- **As a** store manager
- **I want to** add new products to inventory
- **So that** I can track what's in stock
- **Acceptance Criteria:**
  - Product has name, description, price, stock quantity
  - Product belongs to at least one category
  - Product has a supplier
  - Price must be positive
  - Stock quantity must be non-negative
- **Learning Objectives:** Complex validation, multiple relationships
- **Implementation Status:** CHALLENGE - Students design and implement independently

**UC-12: Update Stock Levels**
- **As a** store manager
- **I want to** update product stock quantities
- **So that** inventory reflects current levels
- **Acceptance Criteria:**
  - Can increase or decrease stock
  - Stock cannot go negative
  - System tracks stock changes
- **Learning Objectives:** UPDATE operations, constraints, business logic
- **Implementation Status:** CHALLENGE - Students design and implement independently

**UC-13: Search Products by Category**
- **As a** customer
- **I want to** browse products by category
- **So that** I can find what I'm looking for
- **Acceptance Criteria:**
  - Shows all products in a category
  - Includes product details and price
  - Shows stock availability
  - Can filter to show only in-stock items
- **Learning Objectives:** JOIN operations, many-to-many relationships
- **Implementation Status:** CHALLENGE - Students design and implement independently

**UC-14: Find Products by Supplier**
- **As a** store manager
- **I want to** see all products from a specific supplier
- **So that** I can manage supplier relationships
- **Acceptance Criteria:**
  - Lists all products from supplier
  - Shows product details and stock levels
  - Sorted by product name
- **Learning Objectives:** JOIN operations, filtering
- **Implementation Status:** CHALLENGE - Students design and implement independently

**UC-15: Low Stock Alert**
- **As a** store manager
- **I want to** see products with low stock
- **So that** I can reorder before running out
- **Acceptance Criteria:**
  - Shows products below a threshold (e.g., < 10 units)
  - Includes supplier information
  - Sorted by stock level (lowest first)
- **Learning Objectives:** Complex queries, business logic, JOIN operations
- **Implementation Status:** CHALLENGE - Students design and implement independently

### Learning Path

Students should work through use cases in this order:

1. **Study Phase**: Read and understand Library System use cases (UC-1 through UC-5)
2. **Guided Phase**: Implement Todo System use cases (UC-6 through UC-10) with scaffolding
3. **Challenge Phase**: Design and implement Inventory System use cases (UC-11 through UC-15) independently

Each phase builds on concepts from the previous phase, ensuring progressive skill development.

## Architecture

### High-Level Structure

```
python-backend-learning-project/
├── README.md                          # Main documentation
├── CONCEPTS.md                        # Educational content on backend concepts
├── setup.py                           # Database initialization script
├── requirements.txt                   # Python dependencies
├── config/
│   └── database.py                    # Database configuration
├── database/
│   ├── connection.py                  # Database connection management
│   ├── schemas/
│   │   ├── library_schema.sql         # Complete example schema
│   │   ├── todo_schema.sql            # Guided exercise schema
│   │   └── inventory_schema.sql       # Challenge schema
│   └── migrations/
│       └── init_db.py                 # Database initialization
├── models/
│   ├── library.py                     # Complete CRUD implementation (reference)
│   ├── todo.py                        # Partial implementation with TODOs (guided)
│   └── inventory.py                   # Function signatures only (challenge)
├── validation/
│   ├── validators.py                  # Example validation functions
│   └── exercises/
│       └── todo_validators.py         # Validation exercises for students
├── interface/
│   ├── cli.py                         # Command-line interface
│   └── api.py                         # Optional Flask API (alternative)
├── utils/
│   ├── error_handlers.py              # Error handling utilities
│   └── logger.py                      # Logging configuration
└── exercises/
    ├── EXERCISES.md                   # Detailed exercise instructions
    └── solutions/                     # Optional solution files
        └── todo_complete.py
```

### Component Layers

1. **Database Layer**: Connection management, schema definitions, and migrations
2. **Model Layer**: CRUD operations and business logic for each topic area
3. **Validation Layer**: Input validation and data integrity checks
4. **Utility Layer**: Error handling, logging, and helper functions

## Components and Interfaces

### 1. Database Connection Management

**Purpose**: Provide a simple, reusable interface for database operations with proper resource management.

**Module**: `database/connection.py`

**Key Functions**:

```python
def get_connection() -> sqlite3.Connection:
    """
    Create and return a database connection.
    
    Returns:
        sqlite3.Connection: Active database connection
    
    Raises:
        DatabaseConnectionError: If connection fails
    """
    pass

def execute_query(query: str, params: tuple = ()) -> List[sqlite3.Row]:
    """
    Execute a SELECT query and return results.
    
    Args:
        query: SQL SELECT statement
        params: Query parameters for safe parameterization
    
    Returns:
        List of rows as sqlite3.Row objects
    
    Raises:
        QueryExecutionError: If query fails
    """
    pass

def execute_update(query: str, params: tuple = ()) -> int:
    """
    Execute an INSERT, UPDATE, or DELETE query.
    
    Args:
        query: SQL modification statement
        params: Query parameters for safe parameterization
    
    Returns:
        Number of affected rows
    
    Raises:
        QueryExecutionError: If query fails
    """
    pass
```

**Design Notes**:
- Uses context managers for automatic connection cleanup
- Implements parameterized queries to prevent SQL injection
- Provides row factory for dictionary-like access to results
- Includes comprehensive error handling with clear messages

### 2. Schema Definitions

**Purpose**: Define database structures for each topic area with appropriate constraints and relationships.

**Library Schema (Complete Reference)**:

```sql
-- Books table with full constraints
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    published_year INTEGER,
    available BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Members table
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    join_date DATE DEFAULT CURRENT_DATE
);

-- Loans table (demonstrates relationships)
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date DATE DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);
```

**Todo Schema (Guided Exercise)**:

```sql
-- Tasks table (students complete constraints)
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    -- TODO: Add status field (e.g., 'pending', 'completed')
    -- TODO: Add priority field (e.g., 'low', 'medium', 'high')
    -- TODO: Add due_date field
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table (students create from scratch)
-- TODO: Create a categories table with id and name fields
-- TODO: Add a foreign key relationship to tasks table
```

**Inventory Schema (Challenge)**:

```sql
-- Students design complete schema for:
-- - Products (id, name, description, price, stock_quantity)
-- - Categories (id, name)
-- - Suppliers (id, name, contact_info)
-- - Product-Category relationship (many-to-many)
-- - Product-Supplier relationship
```

### 3. Model Layer - CRUD Operations

**Purpose**: Implement database operations with proper error handling and validation.

**Library Model (Complete Reference)**:

```python
class Book:
    """Complete implementation demonstrating all CRUD operations."""
    
    @staticmethod
    def create(title: str, author: str, isbn: str, published_year: int = None) -> int:
        """
        Create a new book record.
        
        Args:
            title: Book title
            author: Author name
            isbn: ISBN number (must be unique)
            published_year: Year of publication (optional)
        
        Returns:
            ID of newly created book
        
        Raises:
            ValidationError: If input validation fails
            DuplicateError: If ISBN already exists
        """
        # Validate inputs
        if not title or not author or not isbn:
            raise ValidationError("Title, author, and ISBN are required")
        
        if not is_valid_isbn(isbn):
            raise ValidationError("Invalid ISBN format")
        
        # Execute insert
        query = """
            INSERT INTO books (title, author, isbn, published_year)
            VALUES (?, ?, ?, ?)
        """
        try:
            return execute_update(query, (title, author, isbn, published_year))
        except sqlite3.IntegrityError:
            raise DuplicateError(f"Book with ISBN {isbn} already exists")
    
    @staticmethod
    def get_by_id(book_id: int) -> Optional[Dict]:
        """Retrieve a book by ID."""
        query = "SELECT * FROM books WHERE id = ?"
        results = execute_query(query, (book_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_all(available_only: bool = False) -> List[Dict]:
        """Retrieve all books, optionally filtering by availability."""
        query = "SELECT * FROM books"
        if available_only:
            query += " WHERE available = 1"
        query += " ORDER BY title"
        return execute_query(query)
    
    @staticmethod
    def update(book_id: int, **kwargs) -> bool:
        """Update book fields."""
        # Implementation with dynamic field updates
        pass
    
    @staticmethod
    def delete(book_id: int) -> bool:
        """Delete a book record."""
        query = "DELETE FROM books WHERE id = ?"
        affected = execute_update(query, (book_id,))
        return affected > 0
```

**Todo Model (Guided Exercise)**:

```python
class Task:
    """Partial implementation with TODOs for students."""
    
    @staticmethod
    def create(title: str, description: str = None) -> int:
        """
        Create a new task.
        
        TODO: Add validation for title (not empty, max length)
        TODO: Add status parameter with default value 'pending'
        TODO: Add priority parameter with default value 'medium'
        TODO: Validate status and priority against allowed values
        """
        # TODO: Implement validation
        
        query = """
            INSERT INTO tasks (title, description)
            VALUES (?, ?)
        """
        # TODO: Update query to include status and priority fields
        
        return execute_update(query, (title, description))
    
    @staticmethod
    def get_by_id(task_id: int) -> Optional[Dict]:
        """
        Retrieve a task by ID.
        
        This is a complete example - study how it works!
        """
        query = "SELECT * FROM tasks WHERE id = ?"
        results = execute_query(query, (task_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_all(status: str = None) -> List[Dict]:
        """
        Retrieve all tasks, optionally filtered by status.
        
        TODO: Implement this function following the pattern from get_by_id
        TODO: Add filtering by status if provided
        TODO: Order results by created_at descending
        """
        pass
    
    @staticmethod
    def update_status(task_id: int, new_status: str) -> bool:
        """
        Update task status.
        
        TODO: Validate new_status against allowed values
        TODO: Execute UPDATE query
        TODO: Return True if task was updated, False if not found
        """
        pass
    
    @staticmethod
    def delete(task_id: int) -> bool:
        """
        Delete a task.
        
        TODO: Implement following the pattern from Book.delete()
        """
        pass
```

**Inventory Model (Challenge)**:

```python
class Product:
    """
    Challenge: Implement complete CRUD operations for products.
    
    Requirements:
    - create(name, description, price, stock_quantity, category_id, supplier_id)
    - get_by_id(product_id)
    - get_all(category_id=None, in_stock_only=False)
    - update(product_id, **kwargs)
    - delete(product_id)
    - update_stock(product_id, quantity_change)
    
    Hints:
    - Study the Book and Task models for patterns
    - Remember to validate all inputs
    - Handle foreign key constraints properly
    - Consider what happens when stock goes negative
    """
    pass
```

### 4. Validation Layer

**Purpose**: Ensure data integrity and provide clear error messages for invalid inputs.

**Validator Module** (`validation/validators.py`):

```python
def validate_not_empty(value: str, field_name: str) -> None:
    """
    Validate that a string is not empty or whitespace.
    
    Args:
        value: String to validate
        field_name: Name of field for error message
    
    Raises:
        ValidationError: If value is empty or whitespace
    """
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")

def validate_length(value: str, field_name: str, min_len: int = None, max_len: int = None) -> None:
    """Validate string length constraints."""
    if min_len and len(value) < min_len:
        raise ValidationError(f"{field_name} must be at least {min_len} characters")
    if max_len and len(value) > max_len:
        raise ValidationError(f"{field_name} must be at most {max_len} characters")

def validate_choice(value: str, field_name: str, allowed_values: List[str]) -> None:
    """Validate that value is in allowed set."""
    if value not in allowed_values:
        raise ValidationError(
            f"{field_name} must be one of: {', '.join(allowed_values)}"
        )

def validate_email(email: str) -> None:
    """
    Validate email format.
    
    Example implementation using simple regex.
    Students learn about format validation.
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")

def validate_isbn(isbn: str) -> None:
    """
    Validate ISBN format (ISBN-10 or ISBN-13).
    
    TODO for students: Implement ISBN checksum validation
    """
    # Remove hyphens and spaces
    isbn = isbn.replace('-', '').replace(' ', '')
    
    if len(isbn) not in [10, 13]:
        raise ValidationError("ISBN must be 10 or 13 digits")
    
    if not isbn.isdigit():
        raise ValidationError("ISBN must contain only digits")
    
    # TODO: Add checksum validation for ISBN-10 and ISBN-13
```

**Exercise Validators** (`validation/exercises/todo_validators.py`):

```python
def validate_task_title(title: str) -> None:
    """
    TODO: Implement validation for task title.
    
    Requirements:
    - Must not be empty
    - Must be between 1 and 200 characters
    - Should use validate_not_empty and validate_length functions
    """
    pass

def validate_task_status(status: str) -> None:
    """
    TODO: Implement validation for task status.
    
    Requirements:
    - Must be one of: 'pending', 'in_progress', 'completed'
    - Should use validate_choice function
    """
    pass

def validate_task_priority(priority: str) -> None:
    """
    TODO: Implement validation for task priority.
    
    Requirements:
    - Must be one of: 'low', 'medium', 'high'
    - Should use validate_choice function
    """
    pass
```

### 5. Interface Layer

**Purpose**: Provide a simple way for students to interact with their backend code and see results.

**Note**: The interface layer can be implemented in multiple ways depending on learning goals:

**Option 1: Simple Python Script**
Students can create a simple `main.py` that imports and calls model functions directly:

```python
# main.py - Simple script approach
from models.library import Book
from models.todo import Task

def main():
    print("=== Library System Demo ===")
    
    # Create a book
    book_id = Book.create(
        title="Python Crash Course",
        author="Eric Matthes",
        isbn="978-1593279288"
    )
    print(f"Created book with ID: {book_id}")
    
    # List all books
    books = Book.get_all()
    for book in books:
        print(f"- {book['title']} by {book['author']}")
    
    print("\n=== Todo System Demo ===")
    # TODO: Students add their todo operations here

if __name__ == "__main__":
    main()
```

**Option 2: Interactive Python REPL**
Students can use the Python interactive shell to experiment:

```python
>>> from models.library import Book
>>> book_id = Book.create("Test Book", "Test Author", "1234567890")
>>> book = Book.get_by_id(book_id)
>>> print(book)
```

**Option 3: CLI with argparse** (Optional, more advanced)
For students who want to learn command-line interfaces, provide a basic CLI structure:

```python
# cli.py - Optional CLI approach
import argparse
from models.library import Book

def main():
    parser = argparse.ArgumentParser(description="Backend Learning Project")
    parser.add_argument('action', choices=['add-book', 'list-books'])
    parser.add_argument('--title')
    parser.add_argument('--author')
    parser.add_argument('--isbn')
    
    args = parser.parse_args()
    
    if args.action == 'add-book':
        book_id = Book.create(args.title, args.author, args.isbn)
        print(f"✓ Book added (ID: {book_id})")
    elif args.action == 'list-books':
        books = Book.get_all()
        for book in books:
            print(f"[{book['id']}] {book['title']}")

if __name__ == "__main__":
    main()
```

**Option 4: Flask API** (Optional, for web-focused learning)
For students interested in web APIs, provide a minimal Flask setup:

```python
# api.py - Optional Flask approach
from flask import Flask, request, jsonify
from models.library import Book

app = Flask(__name__)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.get_all()
    return jsonify(books)

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book_id = Book.create(data['title'], data['author'], data['isbn'])
    return jsonify({'id': book_id}), 201

if __name__ == "__main__":
    app.run(debug=True)
```

**Recommendation**: Start with Option 1 (simple script) or Option 2 (REPL) for beginners. Options 3 and 4 can be introduced later as students progress.

### 6. Error Handling

**Error Handler Module** (`utils/error_handlers.py`):

```python
class BackendError(Exception):
    """Base exception for all backend errors."""
    pass

class ValidationError(BackendError):
    """Raised when input validation fails."""
    pass

class DatabaseConnectionError(BackendError):
    """Raised when database connection fails."""
    pass

class QueryExecutionError(BackendError):
    """Raised when query execution fails."""
    pass

class DuplicateError(BackendError):
    """Raised when attempting to create duplicate record."""
    pass

class NotFoundError(BackendError):
    """Raised when requested resource doesn't exist."""
    pass

def handle_database_error(error: Exception) -> str:
    """
    Convert database errors to user-friendly messages.
    
    Example of error handling pattern for students to learn.
    """
    if isinstance(error, sqlite3.IntegrityError):
        if 'UNIQUE constraint failed' in str(error):
            return "This record already exists"
        elif 'FOREIGN KEY constraint failed' in str(error):
            return "Referenced record does not exist"
        else:
            return "Database integrity error"
    elif isinstance(error, sqlite3.OperationalError):
        return "Database operation failed - check your query"
    else:
        return f"Database error: {str(error)}"
```

## Data Models

### Library System (Reference Implementation)

**Books**:
- `id`: Integer, primary key, auto-increment
- `title`: Text, required
- `author`: Text, required
- `isbn`: Text, unique, required
- `published_year`: Integer, optional
- `available`: Boolean, default true
- `created_at`: Timestamp, auto-generated

**Members**:
- `id`: Integer, primary key
- `name`: Text, required
- `email`: Text, unique, required
- `join_date`: Date, default current date

**Loans**:
- `id`: Integer, primary key
- `book_id`: Integer, foreign key to books
- `member_id`: Integer, foreign key to members
- `loan_date`: Date, default current date
- `due_date`: Date, required
- `return_date`: Date, nullable

### Todo System (Guided Exercise)

**Tasks**:
- `id`: Integer, primary key
- `title`: Text, required
- `description`: Text, optional
- `status`: Text, required (pending/in_progress/completed)
- `priority`: Text, required (low/medium/high)
- `due_date`: Date, optional
- `created_at`: Timestamp, auto-generated

**Categories** (students design):
- Students create schema and relationships

### Inventory System (Challenge)

Students design complete data model including:
- Products with pricing and stock
- Categories (many-to-many with products)
- Suppliers
- Appropriate relationships and constraints


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system - essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: TODO Markers Include Explanations

*For any* template file or exercise file containing TODO markers, each TODO comment should include explanatory text describing what the student needs to implement and why.

**Validates: Requirements 1.3, 1.5**

### Property 2: Schema Files Contain Valid SQL

*For any* example schema file (library_schema.sql, todo_schema.sql), it should contain syntactically valid CREATE TABLE statements that can be executed by SQLite without errors.

**Validates: Requirements 2.2**

### Property 3: Example Code Demonstrates SQL Query Patterns

*For any* complete example model file (e.g., library.py), it should demonstrate SELECT queries with filtering (WHERE clause), sorting (ORDER BY clause), and relationships (JOIN operations where applicable).

**Validates: Requirements 2.3**

### Property 4: CRUD Operations Use Parameterized Queries

*For any* database operation function (INSERT, UPDATE, DELETE, SELECT) in example or template code, it should use parameterized queries with placeholders (?) rather than string concatenation to prevent SQL injection.

**Validates: Requirements 2.4, 3.5**

### Property 5: Student Implementation Functions Have Docstrings

*For any* function marked with TODO for student implementation, it should include a docstring explaining the function's purpose, parameters, return value, and any exceptions raised.

**Validates: Requirements 3.3**

### Property 6: Database Operations Manage Connections Properly

*For any* database operation in example code, it should properly manage database connections using context managers (with statements) or explicit try/finally blocks to ensure connections are closed.

**Validates: Requirements 3.4**

### Property 7: CRUD Functions Validate Before Executing Queries

*For any* complete CRUD function implementation in example code, it should call validation functions to check input data before executing database queries.

**Validates: Requirements 5.2**

### Property 8: Validation Failures Provide Clear Error Messages

*For any* validation function that raises an exception, the exception message should clearly identify which field failed validation and why, avoiding technical jargon.

**Validates: Requirements 5.4**

### Property 9: Database Operations Use Try-Except Blocks

*For any* database operation in example code, it should be wrapped in a try-except block to catch and handle potential database errors gracefully.

**Validates: Requirements 6.1**

### Property 10: Error Handlers Include Logging

*For any* error handling block in example code, it should include logging statements to record error details for debugging purposes.

**Validates: Requirements 6.3**

### Property 11: Error Messages Are User-Friendly

*For any* error handler that converts exceptions to user messages, the output message should be understandable by non-technical users and avoid exposing internal implementation details.

**Validates: Requirements 6.5**

### Property 12: Code Files Contain Explanatory Comments

*For any* example implementation file or exercise file, it should contain inline comments explaining key concepts, design decisions, and learning points relevant to the code section.

**Validates: Requirements 7.2, 7.4**

## Error Handling

### Error Categories

1. **Setup Errors**:
   - Database file creation failures
   - Schema initialization errors
   - Missing dependencies

2. **Validation Errors**:
   - Empty required fields
   - Invalid data formats
   - Out-of-range values
   - Invalid choice values

3. **Database Errors**:
   - Connection failures
   - Constraint violations (unique, foreign key)
   - Query syntax errors
   - Transaction failures

4. **Runtime Errors**:
   - Record not found
   - Permission errors
   - File I/O errors

### Error Handling Patterns

**Pattern 1: Validation Before Execution**
```python
def create_book(title: str, author: str, isbn: str) -> int:
    # Validate first
    validate_not_empty(title, "Title")
    validate_not_empty(author, "Author")
    validate_isbn(isbn)
    
    # Then execute
    try:
        return execute_update(query, params)
    except sqlite3.IntegrityError as e:
        raise DuplicateError(f"Book with ISBN {isbn} already exists")
```

**Pattern 2: Graceful Degradation**
```python
def get_all_books():
    try:
        return execute_query("SELECT * FROM books")
    except DatabaseConnectionError:
        logger.error("Database connection failed")
        return []  # Return empty list rather than crashing
```

**Pattern 3: User-Friendly Error Conversion**
```python
try:
    book_id = Book.create(title, author, isbn)
except ValidationError as e:
    print(f"✗ Invalid input: {e}")
except DuplicateError as e:
    print(f"✗ {e}")
except Exception as e:
    print(f"✗ Unexpected error occurred. Please try again.")
    logger.error(f"Unexpected error: {e}", exc_info=True)
```

### Error Recovery Strategies

1. **Database Connection Failures**: Retry with exponential backoff (teaching concept)
2. **Validation Failures**: Prompt user for corrected input
3. **Duplicate Records**: Offer to update existing record instead
4. **Missing Records**: Suggest similar records or list all available
