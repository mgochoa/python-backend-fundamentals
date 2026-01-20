#!/usr/bin/env python3
"""
Python Backend Learning Project - Main Demo Script

This script demonstrates how to use the backend models you've built.
It shows working examples from the Library System and provides a template
for you to add your own Todo System operations.

LEARNING OBJECTIVES:
- See how to import and use model classes
- Understand the flow of CRUD operations
- Learn how to handle errors gracefully
- Practice adding your own operations

HOW TO USE:
1. Make sure you've run setup.py to initialize the database
2. Run this script: python main.py
3. Observe the output and study the code
4. Complete the TODO sections to add Todo operations
"""

import sys
from datetime import datetime

# Import Library System models (complete reference implementation)
from models.library import Book, Member, Loan, ValidationError, DuplicateError, NotFoundError

# Import Todo System models (you'll implement these!)
from models.todo import Task

# Import error handlers for consistent error messages
from utils.error_handlers import handle_database_error


# ============================================================================
# HELPER FUNCTIONS FOR PRETTY OUTPUT
# ============================================================================

def print_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_success(message: str) -> None:
    """Print a success message with checkmark."""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message with X mark."""
    print(f"✗ {message}")


def print_info(message: str) -> None:
    """Print an informational message."""
    print(f"ℹ {message}")


def print_book(book: dict) -> None:
    """Print book details in a formatted way."""
    available = "Available" if book.get('available', 1) else "Checked Out"
    print(f"  [{book['id']}] {book['title']}")
    print(f"      Author: {book['author']}")
    print(f"      ISBN: {book['isbn']}")
    if book.get('published_year'):
        print(f"      Published: {book['published_year']}")
    print(f"      Status: {available}")


def print_member(member: dict) -> None:
    """Print member details in a formatted way."""
    print(f"  [{member['id']}] {member['name']}")
    print(f"      Email: {member['email']}")
    print(f"      Joined: {member['join_date']}")


def print_task(task: dict) -> None:
    """Print task details in a formatted way."""
    print(f"  [{task['id']}] {task['title']}")
    if task.get('description'):
        print(f"      Description: {task['description']}")
    if task.get('status'):
        print(f"      Status: {task['status']}")
    if task.get('priority'):
        print(f"      Priority: {task['priority']}")


# ============================================================================
# LIBRARY SYSTEM DEMONSTRATIONS
# ============================================================================

def demo_library_system():
    """
    Demonstrate Library System operations.
    
    This is a complete working example showing:
    - Creating records (books, members)
    - Reading records (get by ID, get all, search)
    - Updating records
    - Handling errors
    - Working with relationships (loans)
    """
    
    print_header("LIBRARY SYSTEM DEMONSTRATION")
    print_info("This demonstrates the complete Library System implementation.")
    print_info("Study this code to understand CRUD operations!\n")
    
    # -------------------------------------------------------------------------
    # 1. CREATE OPERATIONS - Adding new records
    # -------------------------------------------------------------------------
    print_header("1. Creating Books")
    
    try:
        # Create a book with all fields
        book1_id = Book.create(
            title="Python Crash Course",
            author="Eric Matthes",
            isbn="978-1593279288",
            published_year=2019
        )
        print_success(f"Created book: 'Python Crash Course' (ID: {book1_id})")
        
        # Create another book
        book2_id = Book.create(
            title="Clean Code",
            author="Robert C. Martin",
            isbn="978-0132350884",
            published_year=2008
        )
        print_success(f"Created book: 'Clean Code' (ID: {book2_id})")
        
        # Create a third book
        book3_id = Book.create(
            title="The Pragmatic Programmer",
            author="Andrew Hunt",
            isbn="978-0135957059",
            published_year=2019
        )
        print_success(f"Created book: 'The Pragmatic Programmer' (ID: {book3_id})")
        
    except ValidationError as e:
        print_error(f"Validation failed: {e}")
    except DuplicateError as e:
        print_error(f"Duplicate record: {e}")
        print_info("Books may already exist from a previous run - continuing...")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
    
    # -------------------------------------------------------------------------
    # 2. READ OPERATIONS - Retrieving records
    # -------------------------------------------------------------------------
    print_header("2. Reading Books")
    
    try:
        # Get a specific book by ID
        print_info("Getting book by ID...")
        book = Book.get_by_id(1)
        if book:
            print_success("Found book:")
            print_book(book)
        else:
            print_error("Book not found")
        
        # Get all books
        print_info("\nGetting all books...")
        all_books = Book.get_all()
        print_success(f"Found {len(all_books)} books:")
        for book in all_books:
            print_book(book)
        
        # Search for books
        print_info("\nSearching for books with 'Python' in title...")
        python_books = Book.search("Python", search_field="title")
        print_success(f"Found {len(python_books)} matching books:")
        for book in python_books:
            print_book(book)
            
    except Exception as e:
        print_error(f"Error reading books: {e}")
    
    # -------------------------------------------------------------------------
    # 3. CREATE MEMBERS
    # -------------------------------------------------------------------------
    print_header("3. Creating Library Members")
    
    try:
        member1_id = Member.create(
            name="Alice Johnson",
            email="alice@example.com"
        )
        print_success(f"Created member: 'Alice Johnson' (ID: {member1_id})")
        
        member2_id = Member.create(
            name="Bob Smith",
            email="bob@example.com"
        )
        print_success(f"Created member: 'Bob Smith' (ID: {member2_id})")
        
    except DuplicateError as e:
        print_error(f"Duplicate member: {e}")
        print_info("Members may already exist from a previous run - continuing...")
    except Exception as e:
        print_error(f"Error creating member: {e}")
    
    # -------------------------------------------------------------------------
    # 4. UPDATE OPERATIONS - Modifying records
    # -------------------------------------------------------------------------
    print_header("4. Updating a Book")
    
    try:
        # Update a book's published year
        success = Book.update(1, published_year=2023)
        if success:
            print_success("Updated book's published year")
            updated_book = Book.get_by_id(1)
            print_book(updated_book)
        else:
            print_error("Book not found for update")
            
    except ValidationError as e:
        print_error(f"Validation failed: {e}")
    except Exception as e:
        print_error(f"Error updating book: {e}")
    
    # -------------------------------------------------------------------------
    # 5. WORKING WITH RELATIONSHIPS - Loans
    # -------------------------------------------------------------------------
    print_header("5. Creating a Loan (Member Borrows Book)")
    
    try:
        # Member 1 borrows Book 1
        loan_id = Loan.create(
            book_id=1,
            member_id=1,
            loan_days=14  # 2-week loan
        )
        print_success(f"Created loan: Member 1 borrowed Book 1 (Loan ID: {loan_id})")
        
        # Show the book is now unavailable
        book = Book.get_by_id(1)
        print_info(f"Book status is now: {'Available' if book['available'] else 'Checked Out'}")
        
    except NotFoundError as e:
        print_error(f"Record not found: {e}")
    except ValidationError as e:
        print_error(f"Validation failed: {e}")
    except Exception as e:
        print_error(f"Error creating loan: {e}")
    
    # -------------------------------------------------------------------------
    # 6. ERROR HANDLING DEMONSTRATION
    # -------------------------------------------------------------------------
    print_header("6. Error Handling Examples")
    
    # Example 1: Validation error (empty title)
    print_info("Attempting to create book with empty title...")
    try:
        Book.create(title="", author="Test Author", isbn="123456789")
        print_error("Should have raised ValidationError!")
    except ValidationError as e:
        print_success(f"Caught validation error: {e}")
    
    # Example 2: Not found error
    print_info("\nAttempting to get non-existent book (ID: 99999)...")
    try:
        book = Book.get_by_id(99999)
        if book is None:
            print_success("Correctly returned None for non-existent book")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
    
    # Example 3: Duplicate error
    print_info("\nAttempting to create book with duplicate ISBN...")
    try:
        Book.create(
            title="Duplicate Book",
            author="Test Author",
            isbn="978-1593279288"  # Same ISBN as first book
        )
        print_error("Should have raised DuplicateError!")
    except DuplicateError as e:
        print_success(f"Caught duplicate error: {e}")


# ============================================================================
# TODO SYSTEM DEMONSTRATIONS (FOR STUDENTS TO IMPLEMENT)
# ============================================================================

def demo_todo_system():
    """
    TODO: Demonstrate Todo System operations.
    
    This section is for YOU to implement! Follow the pattern from the
    Library System demonstration above.
    
    TASKS TO COMPLETE:
    1. Create some tasks with different priorities
    2. List all tasks
    3. Update a task's status
    4. Search or filter tasks
    5. Delete a task
    6. Handle errors appropriately
    
    HINTS:
    - Import Task from models.todo at the top of this file (already done!)
    - Use the same error handling patterns as Library System
    - Use the print_task() helper function to display tasks
    - Study the demo_library_system() function for the pattern
    
    EXAMPLE STRUCTURE:
    
    print_header("TODO SYSTEM DEMONSTRATION")
    print_info("This demonstrates the Todo System you implemented!")
    
    # Create tasks
    print_header("1. Creating Tasks")
    try:
        task1_id = Task.create(
            title="Learn Python",
            description="Complete Python tutorial"
        )
        print_success(f"Created task: 'Learn Python' (ID: {task1_id})")
        
        # TODO: Create more tasks
        
    except ValidationError as e:
        print_error(f"Validation failed: {e}")
    except Exception as e:
        print_error(f"Error creating task: {e}")
    
    # TODO: Add more operations (read, update, delete)
    """
    
    print_header("TODO SYSTEM DEMONSTRATION")
    print_info("This section is for YOU to implement!")
    print_info("Follow the pattern from the Library System above.")
    print_info("Uncomment and complete the code below:\n")
    
    # TODO: Uncomment and implement the following sections
    
    # # -------------------------------------------------------------------------
    # # 1. CREATE TASKS
    # # -------------------------------------------------------------------------
    # print_header("1. Creating Tasks")
    # try:
    #     task1_id = Task.create(
    #         title="Learn Python basics",
    #         description="Complete Python fundamentals tutorial"
    #     )
    #     print_success(f"Created task: 'Learn Python basics' (ID: {task1_id})")
    #     
    #     # TODO: Create more tasks with different priorities
    #     
    # except ValidationError as e:
    #     print_error(f"Validation failed: {e}")
    # except Exception as e:
    #     print_error(f"Error creating task: {e}")
    
    # # -------------------------------------------------------------------------
    # # 2. READ TASKS
    # # -------------------------------------------------------------------------
    # print_header("2. Reading Tasks")
    # try:
    #     # Get all tasks
    #     all_tasks = Task.get_all()
    #     print_success(f"Found {len(all_tasks)} tasks:")
    #     for task in all_tasks:
    #         print_task(task)
    #     
    #     # TODO: Try filtering by status
    #     
    # except Exception as e:
    #     print_error(f"Error reading tasks: {e}")
    
    # # -------------------------------------------------------------------------
    # # 3. UPDATE TASK STATUS
    # # -------------------------------------------------------------------------
    # print_header("3. Updating Task Status")
    # try:
    #     # TODO: Update a task's status to 'completed'
    #     pass
    # except Exception as e:
    #     print_error(f"Error updating task: {e}")
    
    # # -------------------------------------------------------------------------
    # # 4. DELETE A TASK
    # # -------------------------------------------------------------------------
    # print_header("4. Deleting a Task")
    # try:
    #     # TODO: Delete a task
    #     pass
    # except Exception as e:
    #     print_error(f"Error deleting task: {e}")
    
    print_info("\n👉 Complete the TODO sections above to see your Todo System in action!")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """
    Main entry point for the demo script.
    
    This function runs all demonstrations in sequence.
    """
    
    print("\n" + "=" * 70)
    print("  PYTHON BACKEND LEARNING PROJECT - DEMO SCRIPT")
    print("=" * 70)
    print("\nThis script demonstrates the backend systems you're learning to build.")
    print("Study the code and output to understand CRUD operations!\n")
    
    try:
        # Run Library System demonstration (complete reference)
        demo_library_system()
        
        # Run Todo System demonstration (for students to complete)
        demo_todo_system()
        
        # Final message
        print_header("DEMONSTRATION COMPLETE")
        print_success("All demonstrations completed!")
        print_info("\nNext steps:")
        print("  1. Study the code in this file (main.py)")
        print("  2. Review models/library.py to understand the implementation")
        print("  3. Complete the TODOs in models/todo.py")
        print("  4. Implement the demo_todo_system() function above")
        print("  5. Run this script again to see your Todo System in action!")
        print("\n" + "=" * 70 + "\n")
        
    except KeyboardInterrupt:
        print_error("\n\nScript interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        print_info("Make sure you've run setup.py to initialize the database")
        sys.exit(1)


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
