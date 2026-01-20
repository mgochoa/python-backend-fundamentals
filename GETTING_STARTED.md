# Getting Started with Python Backend Fundamentals

Welcome! This guide will help you get started with the Python Backend Learning Project.

## Quick Start

### 1. Prerequisites
- Python 3.7 or higher
- Git (for cloning the repository)
- A text editor or IDE (VS Code recommended)

### 2. Setup

```bash
# Clone the repository
git clone https://github.com/mgochoa/python-backend-fundamentals.git
cd python-backend-fundamentals

# Initialize the database
python setup.py

# Run the demo
python main.py

# Load sample data (optional)
python database/sample_data.py
```

### 3. Verify Installation

If everything is set up correctly, you should see:
- A `data/` directory with `learning_project.db`
- Output from `main.py` showing library operations
- No error messages

## Learning Path

### Phase 1: Study (Stories 1-3)
**Goal**: Understand how backend systems work

1. **Story 1**: Complete the setup above
2. **Story 2**: Study `models/library.py` - the complete reference implementation
3. **Story 3**: Study relationships between Books, Members, and Loans

**Time**: ~4.5 hours

### Phase 2: Guided Implementation (Stories 4-9)
**Goal**: Build the Todo system with guidance

4. **Story 4**: Implement validators in `validation/exercises/todo_validators.py`
5. **Story 5**: Implement `Task.create()` in `models/todo.py`
6. **Story 6**: Implement `Task.get_all()` in `models/todo.py`
7. **Story 7**: Implement `Task.update_status()` in `models/todo.py`
8. **Story 8**: Implement `Task.delete()` in `models/todo.py`
9. **Story 9**: (Optional) Implement category system

**Time**: ~6-9 hours

### Phase 3: Challenge (Stories 10-15)
**Goal**: Build the Inventory system independently

10. **Story 10**: Design the inventory database schema
11. **Story 11**: Implement Product CRUD operations
12. **Story 12**: Implement stock management
13. **Story 13**: Implement Category and Supplier models
14. **Story 14**: Implement many-to-many relationships
15. **Story 15**: Implement low stock alerts

**Time**: ~14.5 hours

### Bonus (Stories 16-18)
Optional extensions to enhance your learning:
- Add due dates to tasks
- Create a CLI interface
- Build a REST API

## Key Files to Know

### Documentation
- `README.md` - Project overview and setup
- `CONCEPTS.md` - Core backend concepts explained
- `EXERCISES.md` - Detailed exercise instructions
- `PROJECT_STRUCTURE.md` - Directory structure guide

### Reference Implementation
- `models/library.py` - Complete CRUD implementation (study this!)
- `database/schemas/library_schema.sql` - Database schema example

### Your Work
- `models/todo.py` - Complete the TODOs here
- `models/inventory.py` - Build this from scratch
- `validation/exercises/todo_validators.py` - Implement validators

### Utilities
- `validation/validators.py` - Reusable validation functions
- `utils/error_handlers.py` - Custom exceptions
- `utils/logger.py` - Logging setup

## Testing Your Code

### Quick Testing (Recommended for Beginners)

```bash
# Test your TODO implementations as you work
python test_my_code.py

# Test only validators
python test_my_code.py --validators

# Test only Todo model
python test_my_code.py --todo

# Show detailed output
python test_my_code.py --verbose
```

This script will:
- ✅ Check if your functions are implemented
- ✅ Test with valid and invalid inputs
- ✅ Show clear success/error messages
- ✅ Give you immediate feedback

### Interactive Playground

```bash
# Launch interactive environment
python playground.py
```

In the playground you can:
- 🔍 `explore()` - See what's available to test
- 📚 `demo_library()` - See the reference implementation in action
- ✅ `demo_validators()` - See how validation works
- ✏️ `test_task()` - Test your Task implementation
- 💻 Use any Python code to experiment!

Example playground session:
```python
>>> explore()  # See what's available
>>> demo_library()  # Watch the library system work
>>> test_task()  # Test your Task implementation
>>> Task.create("My task", "Description", "high")  # Try it yourself!
>>> exit()  # Leave when done
```

### Advanced Testing (Optional)

```bash
# Install pytest (if not already installed)
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_validators.py

# Run with verbose output
pytest tests/ -v
```

## Getting Help

### Testing Your Work

**Always test as you go!** After implementing each TODO:

1. **Quick test**: `python test_my_code.py`
2. **Interactive test**: `python playground.py` then `test_task()`
3. **Manual test**: Try your functions in the playground

### When You're Stuck

1. **Read the error message** - It tells you what's wrong
2. **Check the TODO comments** - They have step-by-step hints
3. **Study the reference** - `models/library.py` shows the patterns
4. **Review concepts** - `CONCEPTS.md` explains fundamentals
5. **Check exercises** - `EXERCISES.md` has detailed guides
6. **Use the playground** - `python playground.py` to experiment

### Common Issues

**Database not found**
```bash
python setup.py
```

**Import errors**
Make sure you're in the project root directory.

**Tests failing**
This is normal! Tests help you verify your implementation is correct.

## Tips for Success

1. **Work sequentially** - Each story builds on previous ones
2. **Test frequently** - Run your code after each change
3. **Read comments** - They explain the "why" not just the "what"
4. **Take breaks** - Learning takes time
5. **Experiment** - Try things in the Python REPL
6. **Track progress** - Use the GitHub Project board

## Project Board

Track your progress on GitHub:
1. Go to https://github.com/mgochoa/python-backend-fundamentals
2. Click the "Projects" tab
3. View "Python Backend Learning Journey"
4. Move issues as you complete them: Todo → In Progress → Done

## Resources

- [Python SQLite Documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)

## Ready to Start?

1. Complete the setup above
2. Open the GitHub Project board
3. Start with Story 1: Project Setup
4. Move to Story 2: Study the Library System

Happy learning! 🚀
