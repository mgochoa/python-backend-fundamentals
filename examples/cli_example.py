#!/usr/bin/env python3
"""
Command-Line Interface (CLI) Example

This is an OPTIONAL advanced example showing how to build a command-line
interface for your backend using Python's argparse module.

LEARNING OBJECTIVES:
- Understand command-line argument parsing
- Build user-friendly CLI applications
- Handle user input and validation
- Provide helpful error messages and usage information

WHAT IS A CLI?
A CLI (Command-Line Interface) allows users to interact with your application
by typing commands in a terminal, like:
    python cli_example.py add-book --title "Python Book" --author "John Doe"
    python cli_example.py list-books
    python cli_example.py search-books --query "Python"

This is useful for:
- Automation and scripting
- Server-side applications without a GUI
- Developer tools and utilities
- Quick testing and debugging

HOW TO USE THIS FILE:
1. Make sure you've run setup.py to initialize the database
2. Run with --help to see available commands:
   python examples/cli_example.py --help
3. Try the library commands:
   python examples/cli_example.py add-book --title "Test Book" --author "Test Author" --isbn "1234567890"
   python examples/cli_example.py list-books
4. Study the code to understand how it works
5. Complete the TODO sections to add Todo commands
"""

import argparse
import sys
from typing import Optional

# Import Library System models
from models.library import Book, Member, Loan, ValidationError, DuplicateError, NotFoundError

# Import Todo System models
from models.todo import Task


# ============================================================================
# LIBRARY SYSTEM COMMANDS (Complete Examples)
# ============================================================================

def cmd_add_book(args) -> None:
    """
    Add a new book to the library.
    
    This demonstrates:
    - Accessing command-line arguments
    - Calling model methods
    - Handling errors with try-except
    - Providing user feedback
    """
    try:
        book_id = Book.create(
            title=args.title,
            author=args.author,
            isbn=args.isbn,
            published_year=args.year
        )
        print(f"✓ Book added successfully (ID: {book_id})")
        print(f"  Title: {args.title}")
        print(f"  Author: {args.author}")
        print(f"  ISBN: {args.isbn}")
        
    except ValidationError as e:
        print(f"✗ Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except DuplicateError as e:
        print(f"✗ Duplicate error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list_books(args) -> None:
    """
    List all books in the library.
    
    This demonstrates:
    - Retrieving multiple records
    - Formatting output for readability
    - Handling empty results
    """
    try:
        books = Book.get_all(available_only=args.available_only)
        
        if not books:
            print("No books found.")
            return
        
        print(f"\n{'ID':<5} {'Title':<40} {'Author':<25} {'Status':<12}")
        print("-" * 85)
        
        for book in books:
            status = "Available" if book['available'] else "Checked Out"
            # Truncate long titles/authors for display
            title = book['title'][:37] + "..." if len(book['title']) > 40 else book['title']
            author = book['author'][:22] + "..." if len(book['author']) > 25 else book['author']
            
            print(f"{book['id']:<5} {title:<40} {author:<25} {status:<12}")
        
        print(f"\nTotal: {len(books)} book(s)")
        
    except Exception as e:
        print(f"✗ Error listing books: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_search_books(args) -> None:
    """
    Search for books by title or author.
    
    This demonstrates:
    - Using search functionality
    - Handling search parameters
    - Displaying search results
    """
    try:
        books = Book.search(args.query, search_field=args.field)
        
        if not books:
            print(f"No books found matching '{args.query}' in {args.field}")
            return
        
        print(f"\nSearch results for '{args.query}' in {args.field}:")
        print(f"{'ID':<5} {'Title':<40} {'Author':<25}")
        print("-" * 70)
        
        for book in books:
            title = book['title'][:37] + "..." if len(book['title']) > 40 else book['title']
            author = book['author'][:22] + "..." if len(book['author']) > 25 else book['author']
            print(f"{book['id']:<5} {title:<40} {author:<25}")
        
        print(f"\nFound: {len(books)} book(s)")
        
    except Exception as e:
        print(f"✗ Error searching books: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_delete_book(args) -> None:
    """
    Delete a book from the library.
    
    This demonstrates:
    - Deleting records
    - Confirming actions with users
    - Handling not found errors
    """
    try:
        # First, get the book to show what will be deleted
        book = Book.get_by_id(args.id)
        if not book:
            print(f"✗ Book with ID {args.id} not found", file=sys.stderr)
            sys.exit(1)
        
        # Confirm deletion (unless --force flag is used)
        if not args.force:
            print(f"About to delete: {book['title']} by {book['author']}")
            response = input("Are you sure? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Deletion cancelled.")
                return
        
        # Delete the book
        success = Book.delete(args.id)
        if success:
            print(f"✓ Book deleted successfully (ID: {args.id})")
        else:
            print(f"✗ Failed to delete book (ID: {args.id})", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"✗ Error deleting book: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_add_member(args) -> None:
    """Add a new library member."""
    try:
        member_id = Member.create(name=args.name, email=args.email)
        print(f"✓ Member added successfully (ID: {member_id})")
        print(f"  Name: {args.name}")
        print(f"  Email: {args.email}")
        
    except ValidationError as e:
        print(f"✗ Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except DuplicateError as e:
        print(f"✗ Duplicate error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list_members(args) -> None:
    """List all library members."""
    try:
        members = Member.get_all()
        
        if not members:
            print("No members found.")
            return
        
        print(f"\n{'ID':<5} {'Name':<30} {'Email':<35} {'Join Date':<12}")
        print("-" * 85)
        
        for member in members:
            name = member['name'][:27] + "..." if len(member['name']) > 30 else member['name']
            email = member['email'][:32] + "..." if len(member['email']) > 35 else member['email']
            print(f"{member['id']:<5} {name:<30} {email:<35} {member['join_date']:<12}")
        
        print(f"\nTotal: {len(members)} member(s)")
        
    except Exception as e:
        print(f"✗ Error listing members: {e}", file=sys.stderr)
        sys.exit(1)


# ============================================================================
# TODO SYSTEM COMMANDS (For Students to Implement)
# ============================================================================

def cmd_add_task(args) -> None:
    """
    TODO: Add a new task to the todo list.
    
    This should:
    1. Call Task.create() with title and description from args
    2. Handle ValidationError and other exceptions
    3. Print success message with task ID
    
    HINTS:
    - Follow the pattern from cmd_add_book()
    - Access arguments with args.title, args.description, etc.
    - Use try-except for error handling
    
    EXAMPLE IMPLEMENTATION:
    try:
        task_id = Task.create(
            title=args.title,
            description=args.description
        )
        print(f"✓ Task added successfully (ID: {task_id})")
    except ValidationError as e:
        print(f"✗ Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    """
    print("TODO: Implement cmd_add_task()")
    print("This command should create a new task.")
    print("Study cmd_add_book() above for the pattern.")


def cmd_list_tasks(args) -> None:
    """
    TODO: List all tasks, optionally filtered by status.
    
    This should:
    1. Call Task.get_all() with optional status filter
    2. Format and display tasks in a table
    3. Handle empty results
    
    HINTS:
    - Follow the pattern from cmd_list_books()
    - Use args.status for filtering (if provided)
    - Format output in a readable table
    """
    print("TODO: Implement cmd_list_tasks()")
    print("This command should list all tasks.")
    print("Study cmd_list_books() above for the pattern.")


def cmd_update_task(args) -> None:
    """
    TODO: Update a task's status.
    
    This should:
    1. Call Task.update_status() with task ID and new status
    2. Handle NotFoundError if task doesn't exist
    3. Handle ValidationError if status is invalid
    4. Print success message
    
    HINTS:
    - Use args.id and args.status
    - Handle errors appropriately
    """
    print("TODO: Implement cmd_update_task()")
    print("This command should update a task's status.")


def cmd_delete_task(args) -> None:
    """
    TODO: Delete a task.
    
    This should:
    1. Optionally confirm deletion (unless --force flag)
    2. Call Task.delete() with task ID
    3. Handle NotFoundError if task doesn't exist
    4. Print success message
    
    HINTS:
    - Follow the pattern from cmd_delete_book()
    - Use args.id and args.force
    """
    print("TODO: Implement cmd_delete_task()")
    print("This command should delete a task.")
    print("Study cmd_delete_book() above for the pattern.")


# ============================================================================
# ARGUMENT PARSER SETUP
# ============================================================================

def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    This function sets up all commands and their arguments.
    Study this to understand how argparse works!
    """
    
    # Main parser
    parser = argparse.ArgumentParser(
        description="Python Backend Learning Project - CLI Interface",
        epilog="Study the code to learn how CLI applications work!"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        title="commands",
        description="Available commands",
        dest="command",
        help="Command to execute"
    )
    
    # -------------------------------------------------------------------------
    # LIBRARY SYSTEM COMMANDS
    # -------------------------------------------------------------------------
    
    # add-book command
    parser_add_book = subparsers.add_parser(
        "add-book",
        help="Add a new book to the library"
    )
    parser_add_book.add_argument("--title", required=True, help="Book title")
    parser_add_book.add_argument("--author", required=True, help="Book author")
    parser_add_book.add_argument("--isbn", required=True, help="Book ISBN")
    parser_add_book.add_argument("--year", type=int, help="Publication year (optional)")
    parser_add_book.set_defaults(func=cmd_add_book)
    
    # list-books command
    parser_list_books = subparsers.add_parser(
        "list-books",
        help="List all books in the library"
    )
    parser_list_books.add_argument(
        "--available-only",
        action="store_true",
        help="Show only available books"
    )
    parser_list_books.set_defaults(func=cmd_list_books)
    
    # search-books command
    parser_search_books = subparsers.add_parser(
        "search-books",
        help="Search for books by title or author"
    )
    parser_search_books.add_argument("--query", required=True, help="Search query")
    parser_search_books.add_argument(
        "--field",
        choices=["title", "author"],
        default="title",
        help="Field to search in (default: title)"
    )
    parser_search_books.set_defaults(func=cmd_search_books)
    
    # delete-book command
    parser_delete_book = subparsers.add_parser(
        "delete-book",
        help="Delete a book from the library"
    )
    parser_delete_book.add_argument("--id", type=int, required=True, help="Book ID")
    parser_delete_book.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt"
    )
    parser_delete_book.set_defaults(func=cmd_delete_book)
    
    # add-member command
    parser_add_member = subparsers.add_parser(
        "add-member",
        help="Add a new library member"
    )
    parser_add_member.add_argument("--name", required=True, help="Member name")
    parser_add_member.add_argument("--email", required=True, help="Member email")
    parser_add_member.set_defaults(func=cmd_add_member)
    
    # list-members command
    parser_list_members = subparsers.add_parser(
        "list-members",
        help="List all library members"
    )
    parser_list_members.set_defaults(func=cmd_list_members)
    
    # -------------------------------------------------------------------------
    # TODO SYSTEM COMMANDS (For Students to Add)
    # -------------------------------------------------------------------------
    
    # TODO: Add argument parser for add-task command
    # HINTS:
    # - Use subparsers.add_parser("add-task", help="...")
    # - Add arguments: --title (required), --description (optional)
    # - Set defaults: parser_add_task.set_defaults(func=cmd_add_task)
    #
    # EXAMPLE:
    # parser_add_task = subparsers.add_parser("add-task", help="Add a new task")
    # parser_add_task.add_argument("--title", required=True, help="Task title")
    # parser_add_task.add_argument("--description", help="Task description (optional)")
    # parser_add_task.set_defaults(func=cmd_add_task)
    
    # TODO: Add argument parser for list-tasks command
    # HINTS:
    # - Add optional --status argument for filtering
    # - Use choices=["pending", "in_progress", "completed"] if applicable
    
    # TODO: Add argument parser for update-task command
    # HINTS:
    # - Add --id (required) and --status (required) arguments
    
    # TODO: Add argument parser for delete-task command
    # HINTS:
    # - Add --id (required) and --force (optional) arguments
    # - Follow the pattern from delete-book
    
    return parser


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """
    Main entry point for the CLI application.
    
    This function:
    1. Creates the argument parser
    2. Parses command-line arguments
    3. Calls the appropriate command function
    """
    
    parser = create_parser()
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Call the command function
    args.func(args)


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
