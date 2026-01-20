# Backend Development Concepts Guide

This guide explains the fundamental concepts you'll learn in this project. Read through this before starting the exercises to understand the "why" behind the code patterns you'll see.

## Table of Contents

1. [Database Design Fundamentals](#database-design-fundamentals)
2. [SQL Basics](#sql-basics)
3. [Python Database Interaction](#python-database-interaction)
4. [Data Validation](#data-validation)
5. [Error Handling](#error-handling)
6. [CRUD Operations](#crud-operations)
7. [Best Practices](#best-practices)

---

## Database Design Fundamentals

### What is a Database?

A **database** is an organized collection of data stored electronically. Think of it as a filing cabinet where information is stored in a structured way that makes it easy to find, update, and manage.

### Tables

A **table** is like a spreadsheet with rows and columns:
- **Columns** (fields) define what type of data is stored (e.g., name, email, price)
- **Rows** (records) contain the actual data (e.g., one row per book, one row per user)

**Example: Books Table**
```
+----+-------------------+------------------+----------------+
| id | title             | author           | isbn           |
+----+-------------------+------------------+----------------+
| 1  | Python Crash      | Eric Matthes     | 978-1593279288 |
| 2  | Clean Code        | Robert C. Martin | 978-0132350884 |
+----+-------------------+------------------+----------------+
```

### Primary Keys

A **primary key** is a unique identifier for each row in a table:
- Must be unique (no two rows can have the same primary key)
- Cannot be NULL (must have a value)
- Usually an auto-incrementing integer (1, 2, 3, ...)

**Why?** Primary keys let you reference specific records unambiguously.

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- This is the primary key
    title TEXT NOT NULL,
    author TEXT NOT NULL
);
```

### Foreign Keys

A **foreign key** is a column that references the primary key of another table:
- Creates relationships between tables
- Ensures data integrity (can't reference non-existent records)

**Example: Loans Table with Foreign Keys**
```sql
CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,              -- Foreign key to books table
    member_id INTEGER NOT NULL,            -- Foreign key to members table
    loan_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);
```

**Why?** Foreign keys ensure that:
- You can't create a loan for a book that doesn't exist
- You can't create a loan for a member that doesn't exist
- Data stays consistent across related tables

### Relationships

**One-to-Many**: One record in Table A relates to many records in Table B
- Example: One member can have many loans
- Example: One supplier can provide many products

**Many-to-Many**: Many records in Table A relate to many records in Table B
- Requires a "junction table" to connect them
- Example: Many products can belong to many categories
- Example: Many students can enroll in many courses

**Junction Table Example:**
```sql
-- Products can belong to multiple categories
-- Categories can contain multiple products
CREATE TABLE product_categories (
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### Constraints

**Constraints** are rules that enforce data integrity:

1. **NOT NULL**: Field must have a value
   ```sql
   title TEXT NOT NULL  -- Title cannot be empty
   ```

2. **UNIQUE**: Value must be unique across all rows
   ```sql
   email TEXT UNIQUE  -- No two users can have the same email
   ```

3. **DEFAULT**: Provides a default value if none is specified
   ```sql
   status TEXT DEFAULT 'pending'  -- New tasks start as pending
   ```

4. **CHECK**: Validates that values meet a condition
   ```sql
   price REAL CHECK(price > 0)  -- Price must be positive
   ```

### Data Types

Common SQLite data types:

- **INTEGER**: Whole numbers (1, 42, -5)
- **REAL**: Decimal numbers (3.14, 29.99)
- **TEXT**: Strings ("Hello", "user@example.com")
- **BLOB**: Binary data (images, files)
- **NULL**: Absence of a value

**Note**: SQLite is flexible with types, but it's good practice to specify them correctly.

---

## SQL Basics

SQL (Structured Query Language) is how you interact with databases. There are four main operations:

### SELECT - Reading Data

**SELECT** retrieves data from tables.

**Basic SELECT:**
```sql
-- Get all columns from all books
SELECT * FROM books;

-- Get specific columns
SELECT title, author FROM books;
```

**WHERE Clause - Filtering:**
```sql
-- Get books by a specific author
SELECT * FROM books WHERE author = 'Eric Matthes';

-- Get available books
SELECT * FROM books WHERE available = 1;

-- Get books published after 2015
SELECT * FROM books WHERE published_year > 2015;
```

**ORDER BY - Sorting:**
```sql
-- Sort books alphabetically by title
SELECT * FROM books ORDER BY title;

-- Sort by published year, newest first
SELECT * FROM books ORDER BY published_year DESC;
```

**LIKE - Pattern Matching:**
```sql
-- Find books with "Python" in the title
SELECT * FROM books WHERE title LIKE '%Python%';

-- Find authors whose name starts with "Eric"
SELECT * FROM books WHERE author LIKE 'Eric%';
```

**LIMIT - Restricting Results:**
```sql
-- Get the 5 most recent books
SELECT * FROM books ORDER BY created_at DESC LIMIT 5;
```

### INSERT - Creating Data

**INSERT** adds new rows to a table.

```sql
-- Insert a new book
INSERT INTO books (title, author, isbn, published_year)
VALUES ('Python Crash Course', 'Eric Matthes', '978-1593279288', 2019);

-- Insert with only required fields (others get defaults)
INSERT INTO books (title, author, isbn)
VALUES ('Clean Code', 'Robert C. Martin', '978-0132350884');
```

**Important**: Always use parameterized queries in Python (see below) to prevent SQL injection!

### UPDATE - Modifying Data

**UPDATE** changes existing rows.

```sql
-- Update a book's published year
UPDATE books SET published_year = 2023 WHERE id = 1;

-- Update multiple fields
UPDATE books 
SET title = 'New Title', author = 'New Author' 
WHERE id = 1;

-- Mark a book as unavailable
UPDATE books SET available = 0 WHERE id = 1;
```

**Warning**: Always include a WHERE clause! Without it, UPDATE changes ALL rows!

### DELETE - Removing Data

**DELETE** removes rows from a table.

```sql
-- Delete a specific book
DELETE FROM books WHERE id = 1;

-- Delete all books by an author
DELETE FROM books WHERE author = 'Test Author';
```

**Warning**: Always include a WHERE clause! Without it, DELETE removes ALL rows!

### JOIN - Combining Tables

**JOIN** combines data from multiple tables based on relationships.

**INNER JOIN** - Get matching records from both tables:
```sql
-- Get all loans with book and member information
SELECT 
    loans.id,
    books.title,
    members.name,
    loans.loan_date
FROM loans
INNER JOIN books ON loans.book_id = books.id
INNER JOIN members ON loans.member_id = members.id;
```

**LEFT JOIN** - Get all records from left table, matching from right:
```sql
-- Get all books, including those never loaned
SELECT 
    books.title,
    COUNT(loans.id) as loan_count
FROM books
LEFT JOIN loans ON books.id = loans.book_id
GROUP BY books.id;
```

**Practical Example:**
```sql
-- Get all products in a specific category (many-to-many)
SELECT p.*
FROM products p
INNER JOIN product_categories pc ON p.id = pc.product_id
WHERE pc.category_id = 1;
```

---

## Python Database Interaction

### The sqlite3 Module

Python includes the `sqlite3` module for working with SQLite databases.

**Basic Connection:**
```python
import sqlite3

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect('data/learning_project.db')

# Create a cursor for executing queries
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM books")

# Fetch results
results = cursor.fetchall()

# Always close the connection when done
conn.close()
```

### Context Managers (Better Way)

Use `with` statements to automatically close connections:

```python
with sqlite3.connect('data/learning_project.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
# Connection automatically closed here
```

### Parameterized Queries (CRITICAL!)

**NEVER** use string formatting or f-strings for SQL queries - this causes SQL injection vulnerabilities!

**❌ WRONG - Vulnerable to SQL Injection:**
```python
# DON'T DO THIS!
title = "Python Book"
query = f"SELECT * FROM books WHERE title = '{title}'"
cursor.execute(query)
```

**✅ CORRECT - Use Parameterized Queries:**
```python
# DO THIS!
title = "Python Book"
query = "SELECT * FROM books WHERE title = ?"
cursor.execute(query, (title,))
```

**Why?** Parameterized queries:
- Prevent SQL injection attacks
- Handle special characters correctly
- Are faster (query can be cached)
- Are the industry standard

**Multiple Parameters:**
```python
query = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)"
cursor.execute(query, (title, author, isbn))
```

### Row Factories

By default, `fetchall()` returns tuples. Use a row factory to get dictionaries:

```python
conn = sqlite3.connect('data/learning_project.db')
conn.row_factory = sqlite3.Row  # Enable dictionary-like access

cursor = conn.cursor()
cursor.execute("SELECT * FROM books WHERE id = 1")
book = cursor.fetchone()

# Access by column name
print(book['title'])
print(book['author'])
```

### Transactions

**Transactions** ensure data consistency:

```python
try:
    conn = sqlite3.connect('data/learning_project.db')
    cursor = conn.cursor()
    
    # Multiple operations in one transaction
    cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
    cursor.execute("INSERT INTO loans (book_id, member_id) VALUES (?, ?)", 
                   (book_id, member_id))
    
    # Commit if all operations succeed
    conn.commit()
    
except sqlite3.Error as e:
    # Rollback if any operation fails
    conn.rollback()
    print(f"Error: {e}")
    
finally:
    conn.close()
```

### Common Patterns

**Execute and Fetch One:**
```python
def get_book_by_id(book_id):
    with sqlite3.connect('data/learning_project.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        return cursor.fetchone()
```

**Execute and Fetch All:**
```python
def get_all_books():
    with sqlite3.connect('data/learning_project.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books ORDER BY title")
        return cursor.fetchall()
```

**Execute Insert and Get ID:**
```python
def create_book(title, author, isbn):
    with sqlite3.connect('data/learning_project.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
            (title, author, isbn)
        )
        conn.commit()
        return cursor.lastrowid  # ID of newly created record
```

---

## Data Validation

**Validation** ensures data meets requirements before it's saved to the database.

### Why Validate?

1. **Data Integrity**: Prevent invalid data from entering the database
2. **User Experience**: Provide clear error messages
3. **Security**: Prevent malicious input
4. **Business Rules**: Enforce application-specific requirements

### Validation Patterns

**Check for Empty Values:**
```python
def validate_not_empty(value, field_name):
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")

# Usage
validate_not_empty(title, "Title")
```

**Check Length:**
```python
def validate_length(value, field_name, min_len=None, max_len=None):
    if min_len and len(value) < min_len:
        raise ValidationError(f"{field_name} must be at least {min_len} characters")
    if max_len and len(value) > max_len:
        raise ValidationError(f"{field_name} must be at most {max_len} characters")

# Usage
validate_length(title, "Title", min_len=1, max_len=200)
```

**Check Allowed Values:**
```python
def validate_choice(value, field_name, allowed_values):
    if value not in allowed_values:
        raise ValidationError(
            f"{field_name} must be one of: {', '.join(allowed_values)}"
        )

# Usage
validate_choice(status, "Status", ["pending", "in_progress", "completed"])
```

**Check Numeric Ranges:**
```python
def validate_positive(value, field_name):
    if value <= 0:
        raise ValidationError(f"{field_name} must be positive")

# Usage
validate_positive(price, "Price")
```

**Format Validation (Email Example):**
```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")

# Usage
validate_email("user@example.com")
```

### When to Validate

**Always validate BEFORE database operations:**

```python
def create_book(title, author, isbn):
    # Step 1: Validate ALL inputs first
    validate_not_empty(title, "Title")
    validate_not_empty(author, "Author")
    validate_isbn(isbn)
    
    # Step 2: Only execute query if validation passes
    query = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)"
    cursor.execute(query, (title, author, isbn))
```

---

## Error Handling

**Error handling** makes your code robust and user-friendly.

### Exception Hierarchy

Create custom exceptions for different error types:

```python
class BackendError(Exception):
    """Base exception for all backend errors"""
    pass

class ValidationError(BackendError):
    """Raised when input validation fails"""
    pass

class NotFoundError(BackendError):
    """Raised when requested resource doesn't exist"""
    pass

class DuplicateError(BackendError):
    """Raised when attempting to create duplicate record"""
    pass
```

### Try-Except Pattern

**Basic Pattern:**
```python
try:
    # Code that might fail
    book = Book.create(title, author, isbn)
except ValidationError as e:
    print(f"Invalid input: {e}")
except DuplicateError as e:
    print(f"Duplicate record: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

**Database Error Handling:**
```python
try:
    cursor.execute(query, params)
    conn.commit()
except sqlite3.IntegrityError as e:
    # Handle constraint violations
    if "UNIQUE" in str(e):
        raise DuplicateError("Record already exists")
    elif "FOREIGN KEY" in str(e):
        raise ValidationError("Referenced record doesn't exist")
except sqlite3.OperationalError as e:
    # Handle query errors
    raise QueryExecutionError(f"Query failed: {e}")
```

### User-Friendly Error Messages

**❌ Bad - Technical jargon:**
```python
raise Exception("UNIQUE constraint failed: books.isbn")
```

**✅ Good - Clear explanation:**
```python
raise DuplicateError(
    f"A book with ISBN '{isbn}' already exists. "
    f"Each book must have a unique ISBN."
)
```

### Logging Errors

Use logging for debugging while showing user-friendly messages:

```python
import logging

try:
    # Database operation
    cursor.execute(query, params)
except Exception as e:
    # Log technical details for developers
    logging.error(f"Database error: {e}", exc_info=True)
    
    # Show user-friendly message to users
    print("An error occurred. Please try again later.")
```

---

## CRUD Operations

**CRUD** stands for Create, Read, Update, Delete - the four basic operations for managing data.

### CREATE - Adding New Records

**Pattern:**
1. Validate input
2. Prepare INSERT query
3. Execute with parameters
4. Return new record's ID

```python
def create(title, author, isbn):
    # 1. Validate
    validate_not_empty(title, "Title")
    validate_isbn(isbn)
    
    # 2. Prepare query
    query = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)"
    
    # 3. Execute
    try:
        cursor.execute(query, (title, author, isbn))
        conn.commit()
        
        # 4. Return ID
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise DuplicateError(f"Book with ISBN {isbn} already exists")
```

### READ - Retrieving Records

**Get One Record:**
```python
def get_by_id(book_id):
    query = "SELECT * FROM books WHERE id = ?"
    cursor.execute(query, (book_id,))
    result = cursor.fetchone()
    return result if result else None
```

**Get Multiple Records:**
```python
def get_all(available_only=False):
    query = "SELECT * FROM books"
    params = []
    
    if available_only:
        query += " WHERE available = ?"
        params.append(1)
    
    query += " ORDER BY title"
    
    cursor.execute(query, tuple(params))
    return cursor.fetchall()
```

### UPDATE - Modifying Records

**Pattern:**
1. Validate input
2. Prepare UPDATE query with WHERE clause
3. Execute with parameters
4. Check if any rows were affected

```python
def update(book_id, **kwargs):
    # 1. Validate
    if 'title' in kwargs:
        validate_not_empty(kwargs['title'], "Title")
    
    # 2. Build dynamic query
    fields = []
    values = []
    for field, value in kwargs.items():
        fields.append(f"{field} = ?")
        values.append(value)
    
    query = f"UPDATE books SET {', '.join(fields)} WHERE id = ?"
    values.append(book_id)
    
    # 3. Execute
    cursor.execute(query, tuple(values))
    conn.commit()
    
    # 4. Check if updated
    return cursor.rowcount > 0
```

### DELETE - Removing Records

**Pattern:**
1. Prepare DELETE query with WHERE clause
2. Execute with parameters
3. Check if any rows were affected

```python
def delete(book_id):
    query = "DELETE FROM books WHERE id = ?"
    cursor.execute(query, (book_id,))
    conn.commit()
    return cursor.rowcount > 0
```

---

## Best Practices

### 1. Always Use Parameterized Queries

**✅ DO:**
```python
cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
```

**❌ DON'T:**
```python
cursor.execute(f"SELECT * FROM books WHERE id = {book_id}")
```

### 2. Validate Before Database Operations

```python
# Validate first
validate_not_empty(title, "Title")
validate_isbn(isbn)

# Then execute
cursor.execute(query, params)
```

### 3. Handle Errors Gracefully

```python
try:
    # Operation
    result = perform_operation()
except ValidationError as e:
    # Specific error handling
    print(f"Invalid input: {e}")
except Exception as e:
    # General error handling
    logging.error(f"Unexpected error: {e}")
    print("An error occurred")
```

### 4. Use Transactions for Multiple Operations

```python
try:
    cursor.execute(query1, params1)
    cursor.execute(query2, params2)
    conn.commit()  # Commit if all succeed
except:
    conn.rollback()  # Rollback if any fail
    raise
```

### 5. Close Connections Properly

```python
# Use context managers
with sqlite3.connect('database.db') as conn:
    # Operations
    pass
# Connection automatically closed
```

### 6. Provide Clear Error Messages

```python
# Not helpful
raise Exception("Error")

# Helpful
raise ValidationError(
    "Title cannot be empty. Please provide a book title."
)
```

### 7. Document Your Code

```python
def create_book(title: str, author: str, isbn: str) -> int:
    """
    Create a new book record.
    
    Args:
        title: Book title (required, cannot be empty)
        author: Author name (required)
        isbn: ISBN number (must be unique)
    
    Returns:
        int: ID of newly created book
    
    Raises:
        ValidationError: If input validation fails
        DuplicateError: If ISBN already exists
    """
    # Implementation
```

### 8. Test Your Code

```python
# Test success case
book_id = Book.create("Test Book", "Test Author", "1234567890")
assert book_id > 0

# Test error case
try:
    Book.create("", "Author", "123")  # Empty title
    assert False, "Should have raised ValidationError"
except ValidationError:
    pass  # Expected
```

---

## Summary

You've learned the fundamental concepts of backend development:

1. **Database Design**: Tables, relationships, constraints
2. **SQL**: SELECT, INSERT, UPDATE, DELETE, JOIN
3. **Python Integration**: sqlite3 module, parameterized queries
4. **Validation**: Checking data before saving
5. **Error Handling**: Try-except, custom exceptions
6. **CRUD**: The four basic operations
7. **Best Practices**: Security, clarity, robustness

**Next Steps:**
1. Review the Library System implementation (`models/library.py`)
2. Complete the Todo System exercises (`models/todo.py`)
3. Challenge yourself with the Inventory System (`models/inventory.py`)
4. Refer back to this guide whenever you need clarification

**Remember**: Understanding these concepts is more important than memorizing syntax. Take your time, experiment, and don't be afraid to make mistakes - that's how you learn!

---

**Happy Learning! 🚀**
