#!/usr/bin/env python3
"""
Interactive Playground for Python Backend Learning Project

This script provides an interactive environment to explore and test your code.
It's like a Python REPL but with your project already loaded!

Usage:
    python playground.py

Available commands:
    help()          - Show this help message
    explore()       - Show what's available to test
    demo_library()  - Run library system demo
    demo_validators() - Run validation demo
    test_task()     - Test your Task implementation
    clear()         - Clear the screen
    exit() or quit() - Exit the playground
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Color codes
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text.center(70)}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")


def print_section(text):
    """Print a section header."""
    print(f"\n{CYAN}▶ {text}{RESET}")


def help_message():
    """Show help message."""
    print_header("Playground Help")
    print(f"{GREEN}Available Commands:{RESET}")
    print(f"  {CYAN}help(){RESET}          - Show this help message")
    print(f"  {CYAN}explore(){RESET}       - Show what's available to test")
    print(f"  {CYAN}demo_library(){RESET}  - Run library system demo")
    print(f"  {CYAN}demo_validators(){RESET} - Run validation demo")
    print(f"  {CYAN}test_task(){RESET}     - Test your Task implementation")
    print(f"  {CYAN}clear(){RESET}         - Clear the screen")
    print(f"  {CYAN}exit(){RESET} or {CYAN}quit(){RESET} - Exit the playground")
    print()
    print(f"{GREEN}Quick Start:{RESET}")
    print(f"  1. Run {CYAN}explore(){RESET} to see what's available")
    print(f"  2. Try {CYAN}demo_library(){RESET} to see the reference implementation")
    print(f"  3. Use {CYAN}test_task(){RESET} to test your TODO implementations")
    print()


def explore():
    """Show what's available in the project."""
    print_header("What's Available to Explore")
    
    print_section("Reference Implementation (Study These!)")
    print("  📚 from models.library import Book, Member, Loan")
    print("     - Complete CRUD implementation")
    print("     - Shows all the patterns you'll use")
    print()
    
    print_section("Your Work (Complete the TODOs)")
    print("  ✏️  from models.todo import Task")
    print("     - Implement: create(), get_all(), update_status(), delete()")
    print()
    print("  ✅ from validation.exercises.todo_validators import (")
    print("         validate_task_title,")
    print("         validate_task_status,")
    print("         validate_task_priority")
    print("     )")
    print()
    
    print_section("Utilities")
    print("  🛠️  from validation.validators import (")
    print("         validate_not_empty,")
    print("         validate_choice,")
    print("         validate_positive_number")
    print("     )")
    print("  🚨 from utils.error_handlers import ValidationError, DatabaseError")
    print()
    
    print_section("Try It Out!")
    print(f"  Run {CYAN}demo_library(){RESET} to see the library system in action")
    print(f"  Run {CYAN}test_task(){RESET} to test your Task implementation")
    print()


def demo_library():
    """Demonstrate the library system."""
    print_header("Library System Demo (Reference Implementation)")
    
    try:
        from models.library import Book
        
        print_section("Creating a Book")
        print("Code: Book.create('Python Crash Course', 'Eric Matthes', '978-1593279288', 2019)")
        book_id = Book.create('Python Crash Course', 'Eric Matthes', '978-1593279288', 2019)
        print(f"{GREEN}✓ Book created with ID: {book_id}{RESET}")
        
        print_section("Getting All Books")
        print("Code: Book.get_all()")
        books = Book.get_all()
        for book in books[:3]:  # Show first 3
            print(f"  - {book}")
        if len(books) > 3:
            print(f"  ... and {len(books) - 3} more")
        
        print_section("Searching Books")
        print("Code: Book.search('Python')")
        results = Book.search('Python')
        print(f"{GREEN}✓ Found {len(results)} book(s){RESET}")
        
        print_section("Updating a Book")
        print(f"Code: Book.update({book_id}, available=False)")
        Book.update(book_id, available=False)
        print(f"{GREEN}✓ Book updated{RESET}")
        
        print()
        print(f"{YELLOW}💡 Tip: Study models/library.py to see how this works!{RESET}")
        
    except Exception as e:
        print(f"{YELLOW}Error: {e}{RESET}")
        print("Make sure the database is initialized: python setup.py")


def demo_validators():
    """Demonstrate validation functions."""
    print_header("Validation Demo")
    
    try:
        from validation.validators import validate_not_empty, validate_choice
        from utils.error_handlers import ValidationError
        
        print_section("Testing validate_not_empty()")
        
        # Valid input
        print("Code: validate_not_empty('Hello', 'greeting')")
        try:
            validate_not_empty('Hello', 'greeting')
            print(f"{GREEN}✓ Valid input accepted{RESET}")
        except ValidationError as e:
            print(f"Error: {e}")
        
        # Invalid input
        print("\nCode: validate_not_empty('', 'greeting')")
        try:
            validate_not_empty('', 'greeting')
            print("No error raised (unexpected)")
        except ValidationError as e:
            print(f"{GREEN}✓ Correctly rejected: {e}{RESET}")
        
        print_section("Testing validate_choice()")
        
        # Valid choice
        print("Code: validate_choice('red', ['red', 'green', 'blue'], 'color')")
        try:
            validate_choice('red', ['red', 'green', 'blue'], 'color')
            print(f"{GREEN}✓ Valid choice accepted{RESET}")
        except ValidationError as e:
            print(f"Error: {e}")
        
        # Invalid choice
        print("\nCode: validate_choice('yellow', ['red', 'green', 'blue'], 'color')")
        try:
            validate_choice('yellow', ['red', 'green', 'blue'], 'color')
            print("No error raised (unexpected)")
        except ValidationError as e:
            print(f"{GREEN}✓ Correctly rejected: {e}{RESET}")
        
        print()
        print(f"{YELLOW}💡 Tip: Use these validators in your Task implementation!{RESET}")
        
    except Exception as e:
        print(f"{YELLOW}Error: {e}{RESET}")


def test_task():
    """Test the Task implementation."""
    print_header("Testing Your Task Implementation")
    
    try:
        from models.todo import Task
        
        print_section("Testing Task.create()")
        print("Code: Task.create('Learn Python', 'Complete the backend project', 'high')")
        try:
            task_id = Task.create('Learn Python', 'Complete the backend project', 'high')
            if task_id:
                print(f"{GREEN}✓ Task created with ID: {task_id}{RESET}")
            else:
                print(f"{YELLOW}⚠ Task.create() returned: {task_id}{RESET}")
        except NotImplementedError:
            print(f"{YELLOW}⚠ Task.create() not implemented yet (TODO){RESET}")
        except Exception as e:
            print(f"{YELLOW}Error: {e}{RESET}")
        
        print_section("Testing Task.get_all()")
        print("Code: Task.get_all()")
        try:
            tasks = Task.get_all()
            print(f"{GREEN}✓ Retrieved {len(tasks)} task(s){RESET}")
            for task in tasks[:3]:
                print(f"  - {task}")
        except NotImplementedError:
            print(f"{YELLOW}⚠ Task.get_all() not implemented yet (TODO){RESET}")
        except Exception as e:
            print(f"{YELLOW}Error: {e}{RESET}")
        
        if 'task_id' in locals() and task_id:
            print_section("Testing Task.update_status()")
            print(f"Code: Task.update_status({task_id}, 'in_progress')")
            try:
                success = Task.update_status(task_id, 'in_progress')
                if success:
                    print(f"{GREEN}✓ Task status updated{RESET}")
                else:
                    print(f"{YELLOW}⚠ Task.update_status() returned False{RESET}")
            except NotImplementedError:
                print(f"{YELLOW}⚠ Task.update_status() not implemented yet (TODO){RESET}")
            except Exception as e:
                print(f"{YELLOW}Error: {e}{RESET}")
        
        print()
        print(f"{YELLOW}💡 Tip: Run 'python test_my_code.py' for comprehensive testing{RESET}")
        
    except ImportError as e:
        print(f"{YELLOW}Error importing Task: {e}{RESET}")
    except Exception as e:
        print(f"{YELLOW}Unexpected error: {e}{RESET}")


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def main():
    """Main playground function."""
    clear_screen()
    print_header("Python Backend Learning Project - Interactive Playground")
    
    print(f"{GREEN}Welcome to the playground!{RESET}")
    print(f"This is an interactive environment to explore and test your code.")
    print()
    print(f"Type {CYAN}help(){RESET} to see available commands")
    print(f"Type {CYAN}explore(){RESET} to see what you can test")
    print(f"Type {CYAN}exit(){RESET} or {CYAN}quit(){RESET} to leave")
    print()
    
    # Make functions available in the interactive session
    import code
    
    # Create a custom namespace with our helper functions
    namespace = {
        'help': help_message,
        'explore': explore,
        'demo_library': demo_library,
        'demo_validators': demo_validators,
        'test_task': test_task,
        'clear': clear_screen,
    }
    
    # Also import commonly used modules
    try:
        from models.library import Book, Member, Loan
        namespace.update({'Book': Book, 'Member': Member, 'Loan': Loan})
    except:
        pass
    
    try:
        from models.todo import Task
        namespace['Task'] = Task
    except:
        pass
    
    try:
        from validation.validators import validate_not_empty, validate_choice
        namespace.update({'validate_not_empty': validate_not_empty, 'validate_choice': validate_choice})
    except:
        pass
    
    try:
        from utils.error_handlers import ValidationError, DatabaseError
        namespace.update({'ValidationError': ValidationError, 'DatabaseError': DatabaseError})
    except:
        pass
    
    # Start interactive console
    console = code.InteractiveConsole(namespace)
    console.interact(banner="", exitmsg=f"\n{GREEN}Thanks for using the playground! Keep learning! 🚀{RESET}\n")


if __name__ == "__main__":
    main()
