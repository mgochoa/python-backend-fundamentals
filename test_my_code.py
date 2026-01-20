#!/usr/bin/env python3
"""
Interactive Test Script for Students

This script helps you test your TODO implementations as you work through the exercises.
Run it anytime to check your progress!

Usage:
    python test_my_code.py              # Test everything
    python test_my_code.py --validators # Test only validators
    python test_my_code.py --todo       # Test only Todo model
    python test_my_code.py --verbose    # Show detailed output
"""

import sys
import sqlite3
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text.center(70)}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")


def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")


def print_warning(text):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")


def print_info(text):
    """Print info message."""
    print(f"{BLUE}ℹ {text}{RESET}")


def test_validators(verbose=False):
    """Test validation functions."""
    print_header("Testing Validators")
    
    try:
        from validation.exercises.todo_validators import (
            validate_task_title,
            validate_task_status,
            validate_task_priority
        )
        print_success("Successfully imported validator functions")
    except ImportError as e:
        print_error(f"Could not import validators: {e}")
        print_info("Make sure validation/exercises/todo_validators.py exists")
        return False
    
    all_passed = True
    
    # Test validate_task_title
    print("\n📝 Testing validate_task_title()...")
    try:
        # Should pass
        validate_task_title("Buy groceries")
        print_success("Valid title accepted")
        
        # Should fail
        try:
            validate_task_title("")
            print_error("Empty title should raise ValidationError")
            all_passed = False
        except Exception as e:
            if "ValidationError" in str(type(e).__name__):
                print_success("Empty title correctly rejected")
            else:
                print_error(f"Wrong exception type: {type(e).__name__}")
                all_passed = False
                
        try:
            validate_task_title("   ")
            print_error("Whitespace-only title should raise ValidationError")
            all_passed = False
        except Exception as e:
            if "ValidationError" in str(type(e).__name__):
                print_success("Whitespace-only title correctly rejected")
            else:
                print_error(f"Wrong exception type: {type(e).__name__}")
                all_passed = False
                
    except NotImplementedError:
        print_warning("validate_task_title() not implemented yet (TODO)")
        all_passed = False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        all_passed = False
    
    # Test validate_task_status
    print("\n📊 Testing validate_task_status()...")
    try:
        # Should pass
        for status in ['pending', 'in_progress', 'completed']:
            validate_task_status(status)
        print_success("All valid statuses accepted")
        
        # Should fail
        try:
            validate_task_status("invalid")
            print_error("Invalid status should raise ValidationError")
            all_passed = False
        except Exception as e:
            if "ValidationError" in str(type(e).__name__):
                print_success("Invalid status correctly rejected")
            else:
                print_error(f"Wrong exception type: {type(e).__name__}")
                all_passed = False
                
    except NotImplementedError:
        print_warning("validate_task_status() not implemented yet (TODO)")
        all_passed = False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        all_passed = False
    
    # Test validate_task_priority
    print("\n🎯 Testing validate_task_priority()...")
    try:
        # Should pass
        for priority in ['low', 'medium', 'high']:
            validate_task_priority(priority)
        print_success("All valid priorities accepted")
        
        # Should fail
        try:
            validate_task_priority("urgent")
            print_error("Invalid priority should raise ValidationError")
            all_passed = False
        except Exception as e:
            if "ValidationError" in str(type(e).__name__):
                print_success("Invalid priority correctly rejected")
            else:
                print_error(f"Wrong exception type: {type(e).__name__}")
                all_passed = False
                
    except NotImplementedError:
        print_warning("validate_task_priority() not implemented yet (TODO)")
        all_passed = False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        all_passed = False
    
    return all_passed


def test_todo_model(verbose=False):
    """Test Todo model CRUD operations."""
    print_header("Testing Todo Model")
    
    try:
        from models.todo import Task
        print_success("Successfully imported Task model")
    except ImportError as e:
        print_error(f"Could not import Task model: {e}")
        return False
    
    # Create a test database
    test_db = Path("data/test_todo.db")
    test_db.parent.mkdir(exist_ok=True)
    
    # Initialize test database
    try:
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Read and execute schema
        schema_file = Path("database/schemas/todo_schema.sql")
        if schema_file.exists():
            with open(schema_file) as f:
                cursor.executescript(f.read())
            conn.commit()
            print_success("Test database initialized")
        else:
            print_error("todo_schema.sql not found")
            return False
            
    except Exception as e:
        print_error(f"Could not initialize test database: {e}")
        return False
    finally:
        conn.close()
    
    all_passed = True
    
    # Test Task.create()
    print("\n➕ Testing Task.create()...")
    try:
        task_id = Task.create(
            title="Test task",
            description="This is a test",
            priority="medium"
        )
        if task_id:
            print_success(f"Task created with ID: {task_id}")
        else:
            print_error("Task.create() returned None or 0")
            all_passed = False
    except NotImplementedError:
        print_warning("Task.create() not implemented yet (TODO)")
        all_passed = False
    except Exception as e:
        print_error(f"Error creating task: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        all_passed = False
    
    # Test Task.get_all()
    print("\n📋 Testing Task.get_all()...")
    try:
        tasks = Task.get_all()
        if isinstance(tasks, list):
            print_success(f"Retrieved {len(tasks)} task(s)")
            if verbose and tasks:
                for task in tasks:
                    print(f"  - {task}")
        else:
            print_error("Task.get_all() should return a list")
            all_passed = False
    except NotImplementedError:
        print_warning("Task.get_all() not implemented yet (TODO)")
        all_passed = False
    except Exception as e:
        print_error(f"Error getting tasks: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        all_passed = False
    
    # Test Task.update_status()
    print("\n🔄 Testing Task.update_status()...")
    try:
        if 'task_id' in locals():
            success = Task.update_status(task_id, "in_progress")
            if success:
                print_success("Task status updated")
            else:
                print_error("Task.update_status() returned False")
                all_passed = False
        else:
            print_warning("Skipping (no task created)")
    except NotImplementedError:
        print_warning("Task.update_status() not implemented yet (TODO)")
        all_passed = False
    except Exception as e:
        print_error(f"Error updating task: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        all_passed = False
    
    # Test Task.delete()
    print("\n🗑️  Testing Task.delete()...")
    try:
        if 'task_id' in locals():
            success = Task.delete(task_id)
            if success:
                print_success("Task deleted")
            else:
                print_error("Task.delete() returned False")
                all_passed = False
        else:
            print_warning("Skipping (no task created)")
    except NotImplementedError:
        print_warning("Task.delete() not implemented yet (TODO)")
        all_passed = False
    except Exception as e:
        print_error(f"Error deleting task: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        all_passed = False
    
    # Clean up test database
    try:
        test_db.unlink()
        print_info("Test database cleaned up")
    except:
        pass
    
    return all_passed


def main():
    """Main test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test your TODO implementations")
    parser.add_argument('--validators', action='store_true', help='Test only validators')
    parser.add_argument('--todo', action='store_true', help='Test only Todo model')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    print_header("Python Backend Learning Project - Test Your Code")
    
    results = {}
    
    # Run tests based on arguments
    if args.validators or (not args.validators and not args.todo):
        results['validators'] = test_validators(args.verbose)
    
    if args.todo or (not args.validators and not args.todo):
        results['todo'] = test_todo_model(args.verbose)
    
    # Print summary
    print_header("Test Summary")
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        if passed:
            print_success(f"{test_name.capitalize()}: All tests passed!")
        else:
            print_warning(f"{test_name.capitalize()}: Some tests failed or not implemented")
    
    print()
    if all_passed:
        print_success("🎉 Great job! All implemented features are working!")
    else:
        print_info("💡 Keep working on the TODOs. Run this script again to check progress.")
    
    print()
    print_info("Tip: Use 'python playground.py' to interactively test your code")
    print()


if __name__ == "__main__":
    main()
