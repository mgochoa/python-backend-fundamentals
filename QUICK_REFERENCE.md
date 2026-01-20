# Quick Reference Card

Quick commands and tips for working through the Python Backend Learning Project.

## 🚀 Getting Started

```bash
# First time setup
python setup.py                    # Initialize database
python main.py                     # Run demo
python database/sample_data.py     # Load sample data (optional)
```

## 🧪 Testing Your Code

```bash
# Quick test (recommended!)
python test_my_code.py             # Test everything
python test_my_code.py --validators # Test only validators
python test_my_code.py --todo      # Test only Todo model
python test_my_code.py -v          # Verbose output

# Interactive playground
python playground.py               # Launch interactive environment
```

## 🎮 Playground Commands

```python
help()           # Show help
explore()        # See what's available
demo_library()   # See reference implementation
demo_validators() # See validation examples
test_task()      # Test your Task implementation
clear()          # Clear screen
exit()           # Exit playground
```

## 📁 Key Files

### Study These (Reference Implementation)
- `models/library.py` - Complete CRUD implementation
- `database/schemas/library_schema.sql` - Database schema example
- `validation/validators.py` - Validation utilities

### Work on These (Your TODOs)
- `validation/exercises/todo_validators.py` - Implement validators
- `models/todo.py` - Implement Task CRUD operations
- `models/inventory.py` - Build from scratch (challenge)

### Documentation
- `README.md` - Project overview
- `CONCEPTS.md` - Backend concepts explained
- `EXERCISES.md` - Detailed exercise instructions
- `GETTING_STARTED.md` - Setup and learning path

## 🔍 Exploring the Code

### In Python REPL or Playground

```python
# Import and explore the reference implementation
from models.library import Book, Member, Loan

# Create a book
book_id = Book.create("Python Basics", "John Doe", "123-456", 2024)

# Get all books
books = Book.get_all()

# Search books
results = Book.search("Python")

# Update a book
Book.update(book_id, available=False)

# Delete a book
Book.delete(book_id)
```

### Test Your Task Implementation

```python
from models.todo import Task

# Create a task
task_id = Task.create("Learn Python", "Complete exercises", "high")

# Get all tasks
tasks = Task.get_all()

# Update task status
Task.update_status(task_id, "in_progress")

# Delete task
Task.delete(task_id)
```

### Test Validators

```python
from validation.exercises.todo_validators import (
    validate_task_title,
    validate_task_status,
    validate_task_priority
)

# Test validation
validate_task_title("Buy groceries")  # Should pass
validate_task_status("pending")       # Should pass
validate_task_priority("high")        # Should pass

# These should raise ValidationError
validate_task_title("")               # Empty title
validate_task_status("invalid")       # Invalid status
validate_task_priority("urgent")      # Invalid priority
```

## 🐛 Debugging Tips

### Check Database

```bash
# View database with sqlite3
sqlite3 data/learning_project.db

# In sqlite3 prompt:
.tables                    # List all tables
.schema tasks              # Show table structure
SELECT * FROM tasks;       # View all tasks
.quit                      # Exit
```

### Common Issues

**Import Error**
```bash
# Make sure you're in the project root
pwd  # Should show .../python-backend-fundamentals
```

**Database Not Found**
```bash
# Reinitialize database
python setup.py
```

**Tests Failing**
```bash
# This is normal! Tests help you verify your implementation
# Read the error messages - they tell you what to fix
python test_my_code.py -v  # Verbose output for details
```

## 📊 Progress Tracking

### Story Checklist

**Phase 1: Study (4.5 hours)**
- [ ] Story 1: Project Setup
- [ ] Story 2: Study Library System - Books
- [ ] Story 3: Study Library System - Relationships

**Phase 2: Guided (6-9 hours)**
- [ ] Story 4: Implement Todo Validators
- [ ] Story 5: Implement Task.create()
- [ ] Story 6: Implement Task.get_all()
- [ ] Story 7: Implement Task.update_status()
- [ ] Story 8: Implement Task.delete()
- [ ] Story 9: Implement Category System (optional)

**Phase 3: Challenge (14.5 hours)**
- [ ] Story 10: Design Inventory Schema
- [ ] Story 11: Implement Product CRUD
- [ ] Story 12: Implement Stock Management
- [ ] Story 13: Implement Category/Supplier Models
- [ ] Story 14: Implement Many-to-Many Relationships
- [ ] Story 15: Implement Low Stock Alerts

### After Each Story

1. ✅ Test your code: `python test_my_code.py`
2. 🎮 Experiment in playground: `python playground.py`
3. 📝 Update GitHub issue status
4. 🎉 Celebrate your progress!

## 💡 Pro Tips

1. **Test frequently** - Run `test_my_code.py` after each TODO
2. **Use the playground** - Experiment without fear of breaking things
3. **Study the reference** - `models/library.py` has all the patterns
4. **Read error messages** - They tell you exactly what's wrong
5. **Take breaks** - Learning takes time, don't rush
6. **Ask questions** - Use the GitHub issues for help

## 🔗 Quick Links

- GitHub Issues: https://github.com/mgochoa/python-backend-fundamentals/issues
- GitHub Project: https://github.com/mgochoa/python-backend-fundamentals/projects

## 📚 Learning Resources

- **[Database Schemas](docs/DATABASE_SCHEMAS.md)** - Visual ER diagrams
- **[Schema Quick Reference](docs/SCHEMA_QUICK_REFERENCE.md)** - Schema lookup
- [Python SQLite Docs](https://docs.python.org/3/library/sqlite3.html)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [Python Exceptions](https://docs.python.org/3/tutorial/errors.html)

---

**Need more help?** Check `GETTING_STARTED.md` for detailed instructions!


---

## 🔗 Navigation

**You are here**: QUICK_REFERENCE.md (Keep this handy while coding!)

**Main Guides**:
- 📋 [Workflow](WORKFLOW.md) - Step-by-step for each story
- 🚀 [Getting Started](GETTING_STARTED.md) - Setup guide
- 📊 [Progress Tracker](PROGRESS_TRACKER.md) - Track your progress
- 🔧 [Troubleshooting](TROUBLESHOOTING.md) - Common issues

**Reference**:
- 📚 [Database Schemas](docs/DATABASE_SCHEMAS.md) - Visual ER diagrams
- 📝 [Schema Quick Ref](docs/SCHEMA_QUICK_REFERENCE.md) - Quick lookup
- 📖 [Concepts](CONCEPTS.md) - Database fundamentals
- 📋 [Exercises](exercises/EXERCISES.md) - Detailed guides

**Back to Start**:
- 👋 [Start Here](START_HERE.md)
- 📖 [README](README.md)
