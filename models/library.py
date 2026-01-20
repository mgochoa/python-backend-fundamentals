"""
Library System Models - Complete Reference Implementation

This module provides a complete, working implementation of CRUD operations
for the Library System. Students should study this code to understand:
- How to structure model classes for database entities
- How to implement Create, Read, Update, and Delete operations
- How to validate input data before database operations
- How to handle errors gracefully with clear messages
- How to use parameterized queries to prevent SQL injection
- How to work with relationships between tables

The Library System includes three main entities:
1. Book: Represents books in the library collection
2. Member: Represents library members (patrons)
3. Loan: Represents the borrowing relationship between books and members

This is a REFERENCE IMPLEMENTATION - study it carefully before moving on
to the Todo System exercises where you'll implement similar functionality.

Key Learning Objectives:
- Database CRUD operations in Python
- Input validation and error handling
- SQL query construction with parameters
- Working with foreign key relationships
- Transaction management and data integrity
"""

import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta

# Import database connection utilities
from database.connection import execute_query, execute_insert, execute_update, QueryExecutionError


# ============================================================================
# Custom Exception Classes
# ============================================================================
# These provide clear, specific error messages for different failure scenarios

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
    
    Examples:
    - Book with duplicate ISBN
    - Member with duplicate email
    """
    pass


class NotFoundError(Exception):
    """
    Raised when a requested record doesn't exist.
    
    Examples:
    - Trying to get a book with non-existent ID
    - Trying to update a member that doesn't exist
    """
    pass


# ============================================================================
# Validation Helper Functions
# ============================================================================
# These functions validate input data before database operations
# Validation should ALWAYS happen before executing queries

def validate_not_empty(value: str, field_name: str) -> None:
    """
    Validate that a string field is not empty or whitespace-only.
    
    Args:
        value: The string to validate
        field_name: Name of the field (for error messages)
        
    Raises:
        ValidationError: If value is None, empty, or only whitespace
        
    Example:
        >>> validate_not_empty("Python Book", "title")  # OK
        >>> validate_not_empty("", "title")  # Raises ValidationError
        >>> validate_not_empty("   ", "title")  # Raises ValidationError
    """
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")


def validate_isbn(isbn: str) -> None:
    """
    Validate ISBN format (basic validation).
    
    This is a simplified validation that checks:
    - ISBN is not empty
    - ISBN contains only digits and hyphens
    - ISBN is either 10 or 13 digits (excluding hyphens)
    
    Args:
        isbn: The ISBN string to validate
        
    Raises:
        ValidationError: If ISBN format is invalid
        
    Example:
        >>> validate_isbn("978-1593279288")  # OK (ISBN-13)
        >>> validate_isbn("1593279280")  # OK (ISBN-10)
        >>> validate_isbn("123")  # Raises ValidationError (too short)
        
    Learning Note:
    - Real ISBN validation includes checksum verification
    - This is left as an exercise for advanced students
    - For now, we just check basic format requirements
    """
    if not isbn:
        raise ValidationError("ISBN cannot be empty")
    
    # Remove hyphens and spaces for length checking
    isbn_digits = isbn.replace("-", "").replace(" ", "")
    
    # Check if it contains only digits
    if not isbn_digits.isdigit():
        raise ValidationError("ISBN must contain only digits and hyphens")
    
    # Check length (ISBN-10 or ISBN-13)
    if len(isbn_digits) not in [10, 13]:
        raise ValidationError("ISBN must be 10 or 13 digits")


def validate_year(year: Optional[int]) -> None:
    """
    Validate publication year is reasonable.
    
    Args:
        year: The year to validate (can be None)
        
    Raises:
        ValidationError: If year is invalid
        
    Example:
        >>> validate_year(2023)  # OK
        >>> validate_year(None)  # OK (optional field)
        >>> validate_year(1200)  # Raises ValidationError (too old)
        >>> validate_year(2100)  # Raises ValidationError (future)
    """
    if year is None:
        return  # Year is optional
    
    current_year = datetime.now().year
    
    # Books weren't really published before printing press (~1450)
    # But let's be generous and allow from 1000 onwards
    if year < 1000:
        raise ValidationError("Publication year must be 1000 or later")
    
    # Can't publish books in the future (with some buffer for upcoming releases)
    if year > current_year + 1:
        raise ValidationError(f"Publication year cannot be after {current_year + 1}")


# ============================================================================
# Book Model Class
# ============================================================================

class Book:
    """
    Model class for Book entity - Complete Reference Implementation.
    
    This class provides all CRUD operations for books in the library system.
    Each method demonstrates important concepts for database interaction.
    
    Database Table: books
    Fields:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - title: TEXT NOT NULL
    - author: TEXT NOT NULL
    - isbn: TEXT UNIQUE NOT NULL
    - published_year: INTEGER (optional)
    - available: INTEGER DEFAULT 1 (boolean: 1=available, 0=checked out)
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    Learning Objectives:
    - How to structure a model class
    - How to implement CRUD operations
    - How to validate input data
    - How to handle errors gracefully
    - How to use parameterized queries
    """
    
    @staticmethod
    def create(title: str, author: str, isbn: str, published_year: Optional[int] = None) -> int:
        """
        Create a new book record in the database.
        
        This method demonstrates:
        1. Input validation before database operations
        2. Using parameterized queries to prevent SQL injection
        3. Handling unique constraint violations (duplicate ISBN)
        4. Returning the ID of the newly created record
        5. Comprehensive error handling with clear messages
        
        Args:
            title: Book title (required, cannot be empty)
            author: Author name (required, cannot be empty)
            isbn: ISBN number (required, must be unique, 10 or 13 digits)
            published_year: Year of publication (optional, must be reasonable if provided)
            
        Returns:
            int: The ID of the newly created book record
            
        Raises:
            ValidationError: If any input validation fails
            DuplicateError: If a book with this ISBN already exists
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Create a book with all fields
            >>> book_id = Book.create(
            ...     title="Python Crash Course",
            ...     author="Eric Matthes",
            ...     isbn="978-1593279288",
            ...     published_year=2019
            ... )
            >>> print(f"Created book with ID: {book_id}")
            
            >>> # Create a book without optional year
            >>> book_id = Book.create(
            ...     title="Learning Python",
            ...     author="Mark Lutz",
            ...     isbn="978-1449355739"
            ... )
            
        Learning Notes:
        - ALWAYS validate input before database operations
        - Use specific exception types for different error scenarios
        - Provide clear, user-friendly error messages
        - Use parameterized queries (?) to prevent SQL injection
        - Handle constraint violations (UNIQUE, NOT NULL) gracefully
        """
        # Step 1: Validate all inputs
        # Validation should happen BEFORE we try to insert into database
        # This catches errors early and provides clear feedback
        
        try:
            validate_not_empty(title, "Title")
            validate_not_empty(author, "Author")
            validate_isbn(isbn)
            validate_year(published_year)
        except ValidationError as e:
            # Re-raise validation errors with context
            raise ValidationError(f"Invalid book data: {str(e)}")
        
        # Step 2: Prepare the SQL INSERT query
        # Use ? placeholders for values - NEVER use string formatting!
        # BAD:  f"INSERT INTO books (title) VALUES ('{title}')"  # SQL injection risk!
        # GOOD: "INSERT INTO books (title) VALUES (?)" with params=(title,)
        
        query = """
            INSERT INTO books (title, author, isbn, published_year)
            VALUES (?, ?, ?, ?)
        """
        
        # Step 3: Execute the query with parameters
        # The execute_insert function will:
        # - Safely substitute the ? placeholders with our values
        # - Execute the query
        # - Commit the transaction
        # - Return the new record's ID
        
        try:
            book_id = execute_insert(query, (title, author, isbn, published_year))
            return book_id
            
        except QueryExecutionError as e:
            # Check if this is a duplicate ISBN error
            # SQLite raises IntegrityError for UNIQUE constraint violations
            error_msg = str(e).lower()
            if "unique" in error_msg or "duplicate" in error_msg:
                raise DuplicateError(
                    f"A book with ISBN '{isbn}' already exists. "
                    f"Each book must have a unique ISBN."
                )
            else:
                # Some other database error occurred
                raise QueryExecutionError(f"Failed to create book: {str(e)}")
    
    @staticmethod
    def get_by_id(book_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single book by its ID.
        
        This method demonstrates:
        1. Simple SELECT query with WHERE clause
        2. Using parameterized queries for filtering
        3. Returning None when record doesn't exist (vs raising exception)
        4. Converting database row to dictionary for easy access
        
        Args:
            book_id: The ID of the book to retrieve
            
        Returns:
            Dictionary containing book data if found, None if not found
            Dictionary keys: id, title, author, isbn, published_year, available, created_at
            
        Raises:
            QueryExecutionError: If database operation fails
            
        Example:
            >>> book = Book.get_by_id(1)
            >>> if book:
            ...     print(f"Found: {book['title']} by {book['author']}")
            ...     print(f"ISBN: {book['isbn']}")
            ...     print(f"Available: {book['available']}")
            ... else:
            ...     print("Book not found")
            
        Learning Notes:
        - SELECT queries return a list of results (even if only one row)
        - We return None instead of raising an exception for "not found"
        - This is a common pattern: exceptions for errors, None for "no data"
        - The result is a dictionary, so we can access fields by name
        - Always use parameterized queries, even for simple WHERE clauses
        """
        # Prepare SELECT query with WHERE clause
        # The ? placeholder will be safely replaced with book_id
        query = "SELECT * FROM books WHERE id = ?"
        
        try:
            # Execute the query
            # execute_query returns a list of dictionaries
            results = execute_query(query, (book_id,))
            
            # Return the first result if found, None if list is empty
            # This is a common Python pattern: results[0] if results else None
            return results[0] if results else None
            
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve book: {str(e)}")
    
    @staticmethod
    def get_all(available_only: bool = False, sort_by: str = "title") -> List[Dict[str, Any]]:
        """
        Retrieve all books, with optional filtering and sorting.
        
        This method demonstrates:
        1. SELECT query with optional WHERE clause
        2. Dynamic query building based on parameters
        3. ORDER BY clause for sorting results
        4. Returning empty list when no results (vs None)
        5. Flexible filtering options
        
        Args:
            available_only: If True, only return available books (not checked out)
            sort_by: Field to sort by - "title", "author", or "created_at"
                    Default is "title" for alphabetical listing
            
        Returns:
            List of dictionaries, each containing book data
            Returns empty list [] if no books found
            
        Raises:
            ValidationError: If sort_by field is invalid
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Get all books, sorted by title
            >>> all_books = Book.get_all()
            >>> for book in all_books:
            ...     print(f"- {book['title']} by {book['author']}")
            
            >>> # Get only available books
            >>> available = Book.get_all(available_only=True)
            >>> print(f"Found {len(available)} available books")
            
            >>> # Get all books sorted by author
            >>> by_author = Book.get_all(sort_by="author")
            
            >>> # Get recently added books
            >>> recent = Book.get_all(sort_by="created_at")
            
        Learning Notes:
        - Build queries dynamically based on parameters
        - Always validate user input (like sort_by field)
        - Use ORDER BY to sort results in the database (more efficient than Python sorting)
        - Return empty list [] for "no results" (consistent with Python conventions)
        - Consider what filtering/sorting options users might need
        """
        # Step 1: Validate sort_by parameter
        # Only allow sorting by fields that exist in the table
        valid_sort_fields = ["title", "author", "created_at", "published_year"]
        if sort_by not in valid_sort_fields:
            raise ValidationError(
                f"Invalid sort field '{sort_by}'. "
                f"Must be one of: {', '.join(valid_sort_fields)}"
            )
        
        # Step 2: Build the query dynamically
        # Start with basic SELECT
        query = "SELECT * FROM books"
        params = []
        
        # Add WHERE clause if filtering by availability
        if available_only:
            query += " WHERE available = ?"
            params.append(1)  # 1 = true (available)
        
        # Add ORDER BY clause
        # Note: We validated sort_by above, so it's safe to use in query
        query += f" ORDER BY {sort_by}"
        
        # Step 3: Execute the query
        try:
            results = execute_query(query, tuple(params))
            return results
            
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve books: {str(e)}")
    
    @staticmethod
    def update(book_id: int, **kwargs) -> bool:
        """
        Update one or more fields of a book record.
        
        This method demonstrates:
        1. Dynamic UPDATE queries based on provided fields
        2. Validating which fields can be updated
        3. Partial updates (only update specified fields)
        4. Checking if update actually affected any rows
        5. Using **kwargs for flexible function parameters
        
        Args:
            book_id: ID of the book to update
            **kwargs: Field names and new values to update
                     Allowed fields: title, author, isbn, published_year, available
                     
        Returns:
            bool: True if book was updated, False if book not found
            
        Raises:
            ValidationError: If invalid field name or value provided
            DuplicateError: If updating ISBN to one that already exists
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Update a single field
            >>> Book.update(1, title="New Title")
            
            >>> # Update multiple fields
            >>> Book.update(1, title="New Title", author="New Author", published_year=2024)
            
            >>> # Mark book as unavailable (checked out)
            >>> Book.update(1, available=False)
            
            >>> # Check if update succeeded
            >>> if Book.update(999, title="Test"):
            ...     print("Updated successfully")
            ... else:
            ...     print("Book not found")
            
        Learning Notes:
        - **kwargs allows flexible parameters: update(id, field1=val1, field2=val2, ...)
        - Only update fields that are provided (partial updates)
        - Validate each field before building the query
        - Use SET field1 = ?, field2 = ? syntax for multiple updates
        - Check rowcount to see if update actually affected any rows
        - Return False for "not found" vs raising exception (user-friendly)
        """
        # Step 1: Check if any fields were provided
        if not kwargs:
            raise ValidationError("No fields provided to update")
        
        # Step 2: Define which fields can be updated
        # We don't allow updating 'id' or 'created_at' (system-managed fields)
        updatable_fields = ["title", "author", "isbn", "published_year", "available"]
        
        # Step 3: Validate field names and values
        update_fields = []
        update_values = []
        
        for field, value in kwargs.items():
            # Check if field is allowed to be updated
            if field not in updatable_fields:
                raise ValidationError(
                    f"Cannot update field '{field}'. "
                    f"Allowed fields: {', '.join(updatable_fields)}"
                )
            
            # Validate the value based on field type
            if field == "title" or field == "author":
                validate_not_empty(value, field.capitalize())
            elif field == "isbn":
                validate_isbn(value)
            elif field == "published_year":
                validate_year(value)
            elif field == "available":
                # Convert to integer (SQLite uses 0/1 for boolean)
                if not isinstance(value, (bool, int)):
                    raise ValidationError("Available must be a boolean or integer (0/1)")
                value = 1 if value else 0
            
            # Add to our lists for query building
            update_fields.append(f"{field} = ?")
            update_values.append(value)
        
        # Step 4: Build the UPDATE query
        # Example result: "UPDATE books SET title = ?, author = ? WHERE id = ?"
        query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = ?"
        
        # Add book_id to the end of parameters
        update_values.append(book_id)
        
        # Step 5: Execute the update
        try:
            affected_rows = execute_update(query, tuple(update_values))
            
            # If affected_rows is 0, the book_id didn't exist
            # Return False to indicate "not found" (not an error, just no match)
            return affected_rows > 0
            
        except QueryExecutionError as e:
            # Check if this is a duplicate ISBN error
            error_msg = str(e).lower()
            if "unique" in error_msg or "duplicate" in error_msg:
                raise DuplicateError(
                    f"Cannot update: Another book already has this ISBN"
                )
            else:
                raise QueryExecutionError(f"Failed to update book: {str(e)}")
    
    @staticmethod
    def delete(book_id: int) -> bool:
        """
        Delete a book record from the database.
        
        This method demonstrates:
        1. Simple DELETE query with WHERE clause
        2. Checking if deletion actually removed a row
        3. Handling foreign key constraints (if book is referenced in loans)
        4. Returning boolean to indicate success
        
        Args:
            book_id: ID of the book to delete
            
        Returns:
            bool: True if book was deleted, False if book not found
            
        Raises:
            QueryExecutionError: If database operation fails
                                (e.g., book is referenced in loans table)
            
        Example:
            >>> # Delete a book
            >>> if Book.delete(1):
            ...     print("Book deleted successfully")
            ... else:
            ...     print("Book not found")
            
            >>> # Try to delete a book that's been loaned
            >>> try:
            ...     Book.delete(5)
            ... except QueryExecutionError as e:
            ...     print(f"Cannot delete: {e}")
            ...     print("Book may be referenced in loan records")
            
        Learning Notes:
        - DELETE is permanent - there's no undo!
        - Always use WHERE clause (DELETE without WHERE removes ALL rows!)
        - Check affected rows to see if anything was actually deleted
        - Foreign key constraints may prevent deletion if record is referenced
        - Consider "soft delete" (marking as deleted) vs "hard delete" (actual removal)
        - In production, you might want to archive data before deleting
        """
        # Prepare DELETE query with WHERE clause
        # CRITICAL: Always include WHERE clause!
        # Without WHERE, this would delete ALL books!
        query = "DELETE FROM books WHERE id = ?"
        
        try:
            # Execute the deletion
            affected_rows = execute_update(query, (book_id,))
            
            # Return True if a row was deleted, False if book_id didn't exist
            return affected_rows > 0
            
        except QueryExecutionError as e:
            # Check if this is a foreign key constraint error
            # This happens if the book is referenced in the loans table
            error_msg = str(e).lower()
            if "foreign key" in error_msg:
                raise QueryExecutionError(
                    f"Cannot delete book: It is referenced in loan records. "
                    f"You must delete or update related loans first."
                )
            else:
                raise QueryExecutionError(f"Failed to delete book: {str(e)}")
    
    @staticmethod
    def search(search_term: str, search_field: str = "title") -> List[Dict[str, Any]]:
        """
        Search for books by title or author (partial match).
        
        This method demonstrates:
        1. Using LIKE operator for partial text matching
        2. Case-insensitive search
        3. Wildcard patterns (% for any characters)
        4. Searching across different fields
        
        Args:
            search_term: Text to search for (partial match)
            search_field: Field to search in - "title" or "author"
            
        Returns:
            List of matching books (empty list if no matches)
            
        Raises:
            ValidationError: If search_field is invalid
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Find books with "Python" in title
            >>> results = Book.search("Python", "title")
            >>> for book in results:
            ...     print(book['title'])
            
            >>> # Find books by authors with "Smith" in name
            >>> results = Book.search("Smith", "author")
            
        Learning Notes:
        - LIKE operator: 'Python%' matches "Python...", '%Python%' matches "...Python..."
        - Use % as wildcard (matches any characters)
        - SQLite LIKE is case-insensitive by default
        - For case-sensitive search, use GLOB instead of LIKE
        """
        # Validate search field
        if search_field not in ["title", "author"]:
            raise ValidationError("search_field must be 'title' or 'author'")
        
        # Build query with LIKE for partial matching
        # %search_term% matches any text containing search_term
        query = f"SELECT * FROM books WHERE {search_field} LIKE ? ORDER BY {search_field}"
        
        # Add wildcards to search term
        search_pattern = f"%{search_term}%"
        
        try:
            results = execute_query(query, (search_pattern,))
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to search books: {str(e)}")


# ============================================================================
# Module-level documentation for students
# ============================================================================

"""
SUMMARY - Book Model Implementation:

This module demonstrates a complete CRUD implementation for the Book entity.
Study each method to understand the patterns and best practices.

Key Patterns Demonstrated:

1. CREATE (Book.create):
   - Validate input before database operation
   - Use parameterized queries
   - Handle unique constraint violations
   - Return the new record's ID

2. READ (Book.get_by_id, Book.get_all, Book.search):
   - Simple and complex SELECT queries
   - Optional filtering with WHERE
   - Sorting with ORDER BY
   - Partial text matching with LIKE
   - Return None for single record not found
   - Return empty list for no results

3. UPDATE (Book.update):
   - Dynamic query building
   - Partial updates (only specified fields)
   - Validate each field
   - Return boolean for success/not found

4. DELETE (Book.delete):
   - Simple deletion with WHERE clause
   - Handle foreign key constraints
   - Return boolean for success/not found

Best Practices Applied:

✓ Input validation before database operations
✓ Parameterized queries to prevent SQL injection
✓ Comprehensive error handling with specific exceptions
✓ Clear, detailed docstrings with examples
✓ Inline comments explaining the "why" not just "what"
✓ User-friendly error messages
✓ Consistent return types (None vs empty list vs boolean)
✓ Flexible function parameters (optional filtering, sorting)

Common Patterns:

- Validation → Query Building → Execution → Error Handling
- Use specific exceptions (ValidationError, DuplicateError, NotFoundError)
- Return None for "not found" in get operations
- Return False for "not found" in update/delete operations
- Return empty list for "no results" in list operations
- Always use try-except for database operations
- Provide context in error messages

Next Steps:

After studying this implementation:
1. Understand each method's purpose and pattern
2. Note how validation happens before database operations
3. See how errors are handled and converted to user-friendly messages
4. Observe the use of parameterized queries throughout
5. Move on to models/todo.py to implement similar functionality yourself!

The Todo model will have similar structure but you'll implement it with guidance.
Use this Book model as a reference when you get stuck.
"""


# ============================================================================
# Member Model Class
# ============================================================================

class Member:
    """
    Model class for Member entity - Complete Reference Implementation.
    
    This class provides all CRUD operations for library members (patrons).
    Members can register with the library and borrow books.
    
    Database Table: members
    Fields:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - name: TEXT NOT NULL
    - email: TEXT UNIQUE NOT NULL
    - join_date: DATE DEFAULT CURRENT_DATE
    
    Learning Objectives:
    - Similar CRUD patterns to Book class
    - Email validation
    - Handling unique email constraint
    - Date handling with default values
    """
    
    @staticmethod
    def create(name: str, email: str) -> int:
        """
        Create a new member record in the database.
        
        This method demonstrates:
        1. Validating member information (name and email)
        2. Handling unique email constraint
        3. Automatic join_date assignment by database
        
        Args:
            name: Member's full name (required, cannot be empty)
            email: Member's email address (required, must be unique)
            
        Returns:
            int: The ID of the newly created member record
            
        Raises:
            ValidationError: If input validation fails
            DuplicateError: If email already exists
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Create a new member
            >>> member_id = Member.create(
            ...     name="Alice Johnson",
            ...     email="alice@example.com"
            ... )
            >>> print(f"Created member with ID: {member_id}")
            
        Learning Notes:
        - Email validation is important for user accounts
        - Unique constraint prevents duplicate registrations
        - join_date is automatically set by database (DEFAULT CURRENT_DATE)
        """
        # Step 1: Validate inputs
        try:
            validate_not_empty(name, "Name")
            validate_not_empty(email, "Email")
            
            # Basic email format validation
            if "@" not in email or "." not in email.split("@")[-1]:
                raise ValidationError("Invalid email format")
                
        except ValidationError as e:
            raise ValidationError(f"Invalid member data: {str(e)}")
        
        # Step 2: Prepare INSERT query
        # Note: join_date is not included - it will use DEFAULT CURRENT_DATE
        query = """
            INSERT INTO members (name, email)
            VALUES (?, ?)
        """
        
        # Step 3: Execute the insert
        try:
            member_id = execute_insert(query, (name, email))
            return member_id
            
        except QueryExecutionError as e:
            # Check for duplicate email
            error_msg = str(e).lower()
            if "unique" in error_msg or "duplicate" in error_msg:
                raise DuplicateError(
                    f"A member with email '{email}' already exists. "
                    f"Each member must have a unique email address."
                )
            else:
                raise QueryExecutionError(f"Failed to create member: {str(e)}")
    
    @staticmethod
    def get_by_id(member_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single member by their ID.
        
        Args:
            member_id: The ID of the member to retrieve
            
        Returns:
            Dictionary containing member data if found, None if not found
            Dictionary keys: id, name, email, join_date
            
        Raises:
            QueryExecutionError: If database operation fails
            
        Example:
            >>> member = Member.get_by_id(1)
            >>> if member:
            ...     print(f"Member: {member['name']}")
            ...     print(f"Email: {member['email']}")
            ...     print(f"Joined: {member['join_date']}")
            ... else:
            ...     print("Member not found")
        """
        query = "SELECT * FROM members WHERE id = ?"
        
        try:
            results = execute_query(query, (member_id,))
            return results[0] if results else None
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve member: {str(e)}")
    
    @staticmethod
    def get_all(sort_by: str = "name") -> List[Dict[str, Any]]:
        """
        Retrieve all members, with optional sorting.
        
        Args:
            sort_by: Field to sort by - "name", "email", or "join_date"
                    Default is "name" for alphabetical listing
            
        Returns:
            List of dictionaries, each containing member data
            Returns empty list [] if no members found
            
        Raises:
            ValidationError: If sort_by field is invalid
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Get all members sorted by name
            >>> members = Member.get_all()
            >>> for member in members:
            ...     print(f"- {member['name']} ({member['email']})")
            
            >>> # Get members sorted by join date (newest first)
            >>> recent = Member.get_all(sort_by="join_date")
        """
        # Validate sort_by parameter
        valid_sort_fields = ["name", "email", "join_date"]
        if sort_by not in valid_sort_fields:
            raise ValidationError(
                f"Invalid sort field '{sort_by}'. "
                f"Must be one of: {', '.join(valid_sort_fields)}"
            )
        
        # Build and execute query
        query = f"SELECT * FROM members ORDER BY {sort_by}"
        
        try:
            results = execute_query(query)
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve members: {str(e)}")
    
    @staticmethod
    def update(member_id: int, **kwargs) -> bool:
        """
        Update one or more fields of a member record.
        
        Args:
            member_id: ID of the member to update
            **kwargs: Field names and new values to update
                     Allowed fields: name, email
                     
        Returns:
            bool: True if member was updated, False if member not found
            
        Raises:
            ValidationError: If invalid field name or value provided
            DuplicateError: If updating email to one that already exists
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Update member's name
            >>> Member.update(1, name="Alice Smith")
            
            >>> # Update multiple fields
            >>> Member.update(1, name="Alice Smith", email="alice.smith@example.com")
        """
        if not kwargs:
            raise ValidationError("No fields provided to update")
        
        # Define updatable fields (can't update id or join_date)
        updatable_fields = ["name", "email"]
        
        update_fields = []
        update_values = []
        
        for field, value in kwargs.items():
            if field not in updatable_fields:
                raise ValidationError(
                    f"Cannot update field '{field}'. "
                    f"Allowed fields: {', '.join(updatable_fields)}"
                )
            
            # Validate the value
            if field == "name":
                validate_not_empty(value, "Name")
            elif field == "email":
                validate_not_empty(value, "Email")
                if "@" not in value or "." not in value.split("@")[-1]:
                    raise ValidationError("Invalid email format")
            
            update_fields.append(f"{field} = ?")
            update_values.append(value)
        
        # Build UPDATE query
        query = f"UPDATE members SET {', '.join(update_fields)} WHERE id = ?"
        update_values.append(member_id)
        
        # Execute update
        try:
            affected_rows = execute_update(query, tuple(update_values))
            return affected_rows > 0
        except QueryExecutionError as e:
            error_msg = str(e).lower()
            if "unique" in error_msg or "duplicate" in error_msg:
                raise DuplicateError("Cannot update: Another member already has this email")
            else:
                raise QueryExecutionError(f"Failed to update member: {str(e)}")
    
    @staticmethod
    def delete(member_id: int) -> bool:
        """
        Delete a member record from the database.
        
        Args:
            member_id: ID of the member to delete
            
        Returns:
            bool: True if member was deleted, False if member not found
            
        Raises:
            QueryExecutionError: If database operation fails
                                (e.g., member has active loans)
            
        Example:
            >>> if Member.delete(1):
            ...     print("Member deleted successfully")
            ... else:
            ...     print("Member not found")
            
        Learning Notes:
        - Cannot delete a member who has loan records (foreign key constraint)
        - Consider "soft delete" (marking as inactive) for production systems
        """
        query = "DELETE FROM members WHERE id = ?"
        
        try:
            affected_rows = execute_update(query, (member_id,))
            return affected_rows > 0
        except QueryExecutionError as e:
            error_msg = str(e).lower()
            if "foreign key" in error_msg:
                raise QueryExecutionError(
                    f"Cannot delete member: They have loan records. "
                    f"You must delete or update related loans first."
                )
            else:
                raise QueryExecutionError(f"Failed to delete member: {str(e)}")
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a member by their email address.
        
        This demonstrates searching by a unique field other than ID.
        
        Args:
            email: The email address to search for
            
        Returns:
            Dictionary containing member data if found, None if not found
            
        Raises:
            QueryExecutionError: If database operation fails
            
        Example:
            >>> member = Member.get_by_email("alice@example.com")
            >>> if member:
            ...     print(f"Found member: {member['name']}")
        """
        query = "SELECT * FROM members WHERE email = ?"
        
        try:
            results = execute_query(query, (email,))
            return results[0] if results else None
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve member: {str(e)}")


# ============================================================================
# Loan Model Class
# ============================================================================

class Loan:
    """
    Model class for Loan entity - Demonstrates Relationships and JOINs.
    
    This class manages the borrowing relationship between books and members.
    It demonstrates:
    - Foreign key relationships
    - JOIN operations to combine data from multiple tables
    - Date handling and calculations
    - Business logic (checking availability, calculating due dates)
    
    Database Table: loans
    Fields:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - book_id: INTEGER NOT NULL (foreign key to books.id)
    - member_id: INTEGER NOT NULL (foreign key to members.id)
    - loan_date: DATE DEFAULT CURRENT_DATE
    - due_date: DATE NOT NULL
    - return_date: DATE (NULL until book is returned)
    
    Learning Objectives:
    - Working with foreign keys
    - JOIN queries to combine related data
    - Date arithmetic
    - Business logic implementation
    - Transaction-like operations (updating multiple tables)
    """
    
    @staticmethod
    def create(book_id: int, member_id: int, loan_days: int = 14) -> int:
        """
        Create a new loan record (member borrows a book).
        
        This method demonstrates:
        1. Checking business rules (book must be available)
        2. Calculating due date from loan date
        3. Creating the loan record
        4. Updating related records (marking book as unavailable)
        5. Multiple database operations in sequence
        
        Args:
            book_id: ID of the book being borrowed
            member_id: ID of the member borrowing the book
            loan_days: Number of days until due (default 14 days / 2 weeks)
            
        Returns:
            int: The ID of the newly created loan record
            
        Raises:
            ValidationError: If book is not available or IDs are invalid
            NotFoundError: If book or member doesn't exist
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Create a loan with default 14-day period
            >>> loan_id = Loan.create(book_id=1, member_id=1)
            >>> print(f"Loan created with ID: {loan_id}")
            
            >>> # Create a loan with custom 21-day period
            >>> loan_id = Loan.create(book_id=2, member_id=1, loan_days=21)
            
        Learning Notes:
        - This is a complex operation involving multiple steps
        - We check business rules before creating the loan
        - We update the book's availability status
        - In production, this would be wrapped in a database transaction
        - Transactions ensure all steps succeed or all fail (atomicity)
        """
        # Step 1: Validate loan_days
        if loan_days < 1:
            raise ValidationError("Loan period must be at least 1 day")
        
        # Step 2: Check if book exists and is available
        book = Book.get_by_id(book_id)
        if not book:
            raise NotFoundError(f"Book with ID {book_id} does not exist")
        
        if not book['available']:
            raise ValidationError(
                f"Book '{book['title']}' is not available. "
                f"It is currently checked out."
            )
        
        # Step 3: Check if member exists
        member = Member.get_by_id(member_id)
        if not member:
            raise NotFoundError(f"Member with ID {member_id} does not exist")
        
        # Step 4: Calculate due date
        # loan_date will be set automatically by database (DEFAULT CURRENT_DATE)
        # We need to calculate due_date as loan_date + loan_days
        today = date.today()
        due_date = today + timedelta(days=loan_days)
        
        # Step 5: Create the loan record
        query = """
            INSERT INTO loans (book_id, member_id, due_date)
            VALUES (?, ?, ?)
        """
        
        try:
            loan_id = execute_insert(query, (book_id, member_id, due_date.isoformat()))
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to create loan: {str(e)}")
        
        # Step 6: Mark the book as unavailable
        try:
            Book.update(book_id, available=False)
        except Exception as e:
            # If updating book fails, we have a problem
            # In production, this would be in a transaction that could be rolled back
            raise QueryExecutionError(
                f"Loan created but failed to update book availability: {str(e)}"
            )
        
        return loan_id
    
    @staticmethod
    def get_by_id(loan_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single loan by its ID.
        
        Args:
            loan_id: The ID of the loan to retrieve
            
        Returns:
            Dictionary containing loan data if found, None if not found
            
        Raises:
            QueryExecutionError: If database operation fails
            
        Example:
            >>> loan = Loan.get_by_id(1)
            >>> if loan:
            ...     print(f"Book ID: {loan['book_id']}")
            ...     print(f"Member ID: {loan['member_id']}")
            ...     print(f"Due: {loan['due_date']}")
        """
        query = "SELECT * FROM loans WHERE id = ?"
        
        try:
            results = execute_query(query, (loan_id,))
            return results[0] if results else None
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve loan: {str(e)}")
    
    @staticmethod
    def get_active_loans() -> List[Dict[str, Any]]:
        """
        Retrieve all active loans (books not yet returned).
        
        This demonstrates filtering by NULL values.
        
        Returns:
            List of active loan records (return_date IS NULL)
            
        Example:
            >>> active = Loan.get_active_loans()
            >>> print(f"There are {len(active)} books currently checked out")
            
        Learning Notes:
        - NULL means "no value" - the book hasn't been returned yet
        - Use "IS NULL" not "= NULL" in SQL
        - Active loans have return_date IS NULL
        - Completed loans have return_date IS NOT NULL
        """
        query = "SELECT * FROM loans WHERE return_date IS NULL ORDER BY due_date"
        
        try:
            results = execute_query(query)
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve active loans: {str(e)}")
    
    @staticmethod
    def get_by_member(member_id: int, active_only: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve all loans for a specific member with book details.
        
        **This method demonstrates JOIN operations!**
        
        A JOIN combines data from multiple tables based on a relationship.
        Here we join loans with books to show which books the member borrowed.
        
        This is one of the most important concepts in relational databases!
        
        Args:
            member_id: ID of the member
            active_only: If True, only return loans not yet returned
            
        Returns:
            List of dictionaries containing loan data AND book details
            Each dictionary includes:
            - All loan fields (id, book_id, member_id, loan_date, due_date, return_date)
            - Book details (book_title, book_author, book_isbn)
            
        Raises:
            QueryExecutionError: If database operation fails
            
        Example:
            >>> # Get all loans for member 1
            >>> loans = Loan.get_by_member(1)
            >>> for loan in loans:
            ...     print(f"Borrowed: {loan['book_title']} by {loan['book_author']}")
            ...     print(f"  Loan date: {loan['loan_date']}")
            ...     print(f"  Due date: {loan['due_date']}")
            ...     if loan['return_date']:
            ...         print(f"  Returned: {loan['return_date']}")
            ...     else:
            ...         print(f"  Status: Still checked out")
            
            >>> # Get only active loans for member 1
            >>> active = Loan.get_by_member(1, active_only=True)
            >>> print(f"Member has {len(active)} books currently checked out")
            
        Learning Notes - Understanding JOINs:
        
        What is a JOIN?
        - A JOIN combines rows from two or more tables based on a related column
        - Here we join 'loans' and 'books' tables using book_id
        
        Why use JOINs?
        - Without JOIN: We'd need to query loans, then query books separately for each loan
        - With JOIN: We get all data in one efficient query
        - JOINs are fundamental to relational databases
        
        Types of JOINs:
        - INNER JOIN: Only returns rows where there's a match in both tables
        - LEFT JOIN: Returns all rows from left table, even if no match in right table
        - We use INNER JOIN here because every loan must have a valid book
        
        How this JOIN works:
        1. Start with loans table (WHERE member_id = ?)
        2. For each loan, find the matching book (ON loans.book_id = books.id)
        3. Combine the columns from both tables into one result row
        4. Return all combined rows
        
        The result includes columns from both tables:
        - loans.id, loans.book_id, loans.member_id, loans.loan_date, etc.
        - books.title (as book_title), books.author (as book_author), etc.
        """
        # Build the JOIN query
        # We select specific columns and give them clear names using AS
        query = """
            SELECT 
                loans.id,
                loans.book_id,
                loans.member_id,
                loans.loan_date,
                loans.due_date,
                loans.return_date,
                books.title AS book_title,
                books.author AS book_author,
                books.isbn AS book_isbn
            FROM loans
            INNER JOIN books ON loans.book_id = books.id
            WHERE loans.member_id = ?
        """
        
        # Add filter for active loans if requested
        if active_only:
            query += " AND loans.return_date IS NULL"
        
        # Sort by loan date (most recent first)
        query += " ORDER BY loans.loan_date DESC"
        
        try:
            results = execute_query(query, (member_id,))
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve member loans: {str(e)}")
    
    @staticmethod
    def return_book(loan_id: int) -> bool:
        """
        Mark a book as returned.
        
        This method:
        1. Updates the loan record with return_date
        2. Marks the book as available again
        
        Args:
            loan_id: ID of the loan to mark as returned
            
        Returns:
            bool: True if book was returned, False if loan not found
            
        Raises:
            ValidationError: If book was already returned
            QueryExecutionError: If database operation fails
            
        Example:
            >>> if Loan.return_book(1):
            ...     print("Book returned successfully")
            ... else:
            ...     print("Loan not found")
        """
        # Step 1: Get the loan to check if it exists and get book_id
        loan = Loan.get_by_id(loan_id)
        if not loan:
            return False
        
        # Step 2: Check if already returned
        if loan['return_date'] is not None:
            raise ValidationError(
                f"This book was already returned on {loan['return_date']}"
            )
        
        # Step 3: Update loan with return date
        today = date.today()
        query = "UPDATE loans SET return_date = ? WHERE id = ?"
        
        try:
            execute_update(query, (today.isoformat(), loan_id))
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to update loan: {str(e)}")
        
        # Step 4: Mark book as available
        try:
            Book.update(loan['book_id'], available=True)
        except Exception as e:
            raise QueryExecutionError(
                f"Loan updated but failed to update book availability: {str(e)}"
            )
        
        return True
    
    @staticmethod
    def get_overdue_loans() -> List[Dict[str, Any]]:
        """
        Retrieve all overdue loans (past due date and not returned).
        
        This demonstrates date comparison in SQL.
        
        Returns:
            List of overdue loan records with book and member details
            
        Example:
            >>> overdue = Loan.get_overdue_loans()
            >>> for loan in overdue:
            ...     print(f"Overdue: {loan['book_title']}")
            ...     print(f"  Borrowed by: {loan['member_name']}")
            ...     print(f"  Due: {loan['due_date']}")
            
        Learning Notes:
        - This uses a complex JOIN with multiple tables
        - We join loans -> books -> members to get all details
        - Date comparison: due_date < CURRENT_DATE
        - Multiple conditions in WHERE clause
        """
        query = """
            SELECT 
                loans.id,
                loans.loan_date,
                loans.due_date,
                books.title AS book_title,
                books.author AS book_author,
                members.name AS member_name,
                members.email AS member_email
            FROM loans
            INNER JOIN books ON loans.book_id = books.id
            INNER JOIN members ON loans.member_id = members.id
            WHERE loans.return_date IS NULL
              AND loans.due_date < DATE('now')
            ORDER BY loans.due_date
        """
        
        try:
            results = execute_query(query)
            return results
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to retrieve overdue loans: {str(e)}")
    
    @staticmethod
    def delete(loan_id: int) -> bool:
        """
        Delete a loan record from the database.
        
        Args:
            loan_id: ID of the loan to delete
            
        Returns:
            bool: True if loan was deleted, False if loan not found
            
        Raises:
            QueryExecutionError: If database operation fails
            
        Example:
            >>> if Loan.delete(1):
            ...     print("Loan record deleted")
            
        Learning Notes:
        - Deleting loan records is usually not recommended in production
        - Better to keep historical records for reporting
        - This is provided for completeness of CRUD operations
        """
        query = "DELETE FROM loans WHERE id = ?"
        
        try:
            affected_rows = execute_update(query, (loan_id,))
            return affected_rows > 0
        except QueryExecutionError as e:
            raise QueryExecutionError(f"Failed to delete loan: {str(e)}")


# ============================================================================
# Module Summary - Complete Library System Implementation
# ============================================================================

"""
CONGRATULATIONS! You've studied a complete CRUD implementation with relationships.

This module demonstrates three model classes working together:

1. Book Model:
   - Basic CRUD operations
   - Input validation
   - Search functionality
   - Error handling patterns

2. Member Model:
   - Similar CRUD patterns to Book
   - Email validation and uniqueness
   - Demonstrates consistency across models

3. Loan Model:
   - Foreign key relationships
   - JOIN operations (CRITICAL CONCEPT!)
   - Business logic (availability checking)
   - Date handling and calculations
   - Multi-table operations

Key Concepts Mastered:

✓ CRUD Operations: Create, Read, Update, Delete
✓ Input Validation: Checking data before database operations
✓ Parameterized Queries: Preventing SQL injection
✓ Error Handling: Specific exceptions with clear messages
✓ Foreign Keys: Relationships between tables
✓ JOIN Operations: Combining data from multiple tables
✓ Date Handling: Working with dates and calculations
✓ Business Logic: Implementing real-world rules

Understanding JOINs (Most Important Concept):

The Loan.get_by_member() method is the most important example in this file!
It demonstrates how to:
- Combine data from multiple tables (loans + books)
- Use INNER JOIN to match related records
- Select specific columns with aliases (AS)
- Filter and sort joined results

Study this pattern carefully - JOINs are fundamental to working with
relational databases. Almost every real application uses JOINs extensively.

Next Steps:

1. Run the code and experiment with creating books, members, and loans
2. Try the JOIN queries in Loan.get_by_member() and Loan.get_overdue_loans()
3. Understand how foreign keys maintain data integrity
4. Move on to models/todo.py to implement similar functionality yourself
5. Challenge yourself with models/inventory.py for independent practice

Remember:
- This is a REFERENCE implementation - study it when you get stuck
- The patterns here apply to almost any database application
- Understanding these concepts will make you a better backend developer
- Practice is key - implement the Todo and Inventory systems to solidify your learning

Happy coding! 🚀
"""

