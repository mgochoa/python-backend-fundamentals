# 🔧 Troubleshooting Guide

Common issues and how to fix them.

## 🚨 Setup Issues

### "python: command not found"

**Problem**: Python is not installed or not in PATH.

**Solution**:
```bash
# Check if Python 3 is installed
python3 --version

# If python3 works, use it instead
python3 setup.py
python3 main.py

# Or create an alias (add to ~/.zshrc or ~/.bashrc)
alias python=python3
```

**Install Python**: https://www.python.org/downloads/

---

### "No such file or directory: data/learning_project.db"

**Problem**: Database hasn't been initialized.

**Solution**:
```bash
# Initialize the database
python setup.py

# Verify it was created
ls -la data/
```

**Expected**: You should see `learning_project.db` in the `data/` folder.

---

### "Error executing schema: syntax error"

**Problem**: SQL syntax error in schema file.

**Solution**:
1. Check which schema file has the error (shown in error message)
2. Open the file and look for:
   - Missing commas between fields
   - Extra commas after last field
   - Unclosed parentheses
   - Typos in SQL keywords

**Common mistakes**:
```sql
# ❌ Wrong - comma after last field
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,  -- ← Remove this comma
);

# ✅ Correct
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);
```

---

## 💻 Import Errors

### "ModuleNotFoundError: No module named 'models'"

**Problem**: Not running from project root directory.

**Solution**:
```bash
# Check current directory
pwd

# Should show: .../python-backend-fundamentals

# If not, navigate to project root
cd path/to/python-backend-fundamentals

# Then run your command
python test_my_code.py
```

---

### "ImportError: cannot import name 'Task'"

**Problem**: Task class not defined or has syntax error.

**Solution**:
1. Open `models/todo.py`
2. Check that the class is defined:
   ```python
   class Task:
       # ...
   ```
3. Check for syntax errors (missing colons, wrong indentation)
4. Try importing in Python REPL:
   ```python
   python
   >>> from models.todo import Task
   >>> # If this works, import is fine
   ```

---

## 🧪 Testing Issues

### "NotImplementedError" when running tests

**Problem**: Function not implemented yet (still has `raise NotImplementedError`).

**Solution**: This is normal! It means you haven't completed that TODO yet.

```python
# ❌ Not implemented
def validate_task_title(title):
    raise NotImplementedError("TODO: Implement this function")

# ✅ Implemented
def validate_task_title(title):
    if not title or not title.strip():
        raise ValidationError("Title cannot be empty")
```

**Action**: Complete the TODO following the instructions in the comments.

---

### "All tests failing" or "Many errors"

**Problem**: Might be a fundamental issue.

**Solution**:
```bash
# 1. Reinitialize database
python setup.py

# 2. Test imports
python
>>> from models.todo import Task
>>> from validation.exercises.todo_validators import validate_task_title
>>> # If these work, imports are fine

# 3. Run tests with verbose output
python test_my_code.py -v

# 4. Read the FIRST error message carefully
# Fix that one first, then test again
```

---

### "ValidationError not defined"

**Problem**: Forgot to import ValidationError.

**Solution**:
```python
# Add this import at the top of your file
from utils.error_handlers import ValidationError

# Then you can use it
def validate_task_title(title):
    if not title:
        raise ValidationError("Title cannot be empty")
```

---

## 🗄️ Database Issues

### "database is locked"

**Problem**: Another process is using the database.

**Solution**:
```bash
# 1. Close any open database connections
# - Close DB Browser for SQLite if open
# - Exit any Python REPL sessions
# - Close playground if running

# 2. If still locked, restart terminal

# 3. As last resort, delete and recreate
rm data/learning_project.db
python setup.py
```

---

### "no such table: tasks"

**Problem**: Table doesn't exist in database.

**Solution**:
```bash
# Reinitialize database
python setup.py

# Or force recreation
python setup.py --force

# Verify tables exist
sqlite3 data/learning_project.db
sqlite> .tables
sqlite> .quit
```

---

### "FOREIGN KEY constraint failed"

**Problem**: Trying to reference a non-existent record.

**Solution**:
```python
# ❌ Wrong - category_id 999 doesn't exist
Task.create("My task", "Description", "high", category_id=999)

# ✅ Correct - create category first
category_id = Category.create("Work")
Task.create("My task", "Description", "high", category_id=category_id)

# ✅ Or use NULL (no category)
Task.create("My task", "Description", "high")
```

---

## 🐍 Python Code Issues

### "IndentationError: unexpected indent"

**Problem**: Incorrect indentation (Python is sensitive to this!).

**Solution**:
```python
# ❌ Wrong - inconsistent indentation
def my_function():
    line1 = "hello"
      line2 = "world"  # ← Too many spaces

# ✅ Correct - consistent indentation (4 spaces)
def my_function():
    line1 = "hello"
    line2 = "world"
```

**Tip**: Use a code editor with Python support (VS Code, PyCharm).

---

### "SyntaxError: invalid syntax"

**Problem**: Python syntax error.

**Common causes**:
```python
# ❌ Missing colon
def my_function()
    pass

# ✅ Correct
def my_function():
    pass

# ❌ Missing closing quote
title = "My task

# ✅ Correct
title = "My task"

# ❌ Missing closing parenthesis
result = some_function(arg1, arg2

# ✅ Correct
result = some_function(arg1, arg2)
```

---

### "NameError: name 'x' is not defined"

**Problem**: Using a variable that doesn't exist.

**Solution**:
```python
# ❌ Wrong - typo in variable name
task_id = 1
print(taskid)  # ← Missing underscore

# ✅ Correct
task_id = 1
print(task_id)

# ❌ Wrong - forgot to import
validate_not_empty("test", "field")  # ← Not imported

# ✅ Correct
from validation.validators import validate_not_empty
validate_not_empty("test", "field")
```

---

## 🔍 SQL Query Issues

### "near 'SELECT': syntax error"

**Problem**: SQL syntax error.

**Common causes**:
```python
# ❌ Wrong - missing space
query = "SELECT * FROM" + "tasks"

# ✅ Correct
query = "SELECT * FROM tasks"

# ❌ Wrong - Python variable in SQL string
query = f"SELECT * FROM tasks WHERE id = {task_id}"  # SQL injection risk!

# ✅ Correct - use parameterized query
query = "SELECT * FROM tasks WHERE id = ?"
cursor.execute(query, (task_id,))
```

---

### "no such column: xyz"

**Problem**: Column doesn't exist in table.

**Solution**:
```bash
# 1. Check table structure
sqlite3 data/learning_project.db
sqlite> .schema tasks
sqlite> .quit

# 2. Verify column name spelling
# Common mistakes: "titel" vs "title", "desciption" vs "description"

# 3. If column is missing, update schema and reinitialize
python setup.py --force
```

---

### "Query returns None instead of results"

**Problem**: Forgot to fetch results or used wrong fetch method.

**Solution**:
```python
# ❌ Wrong - forgot to fetch
cursor.execute("SELECT * FROM tasks")
results = cursor  # ← This is the cursor, not results

# ✅ Correct - fetch results
cursor.execute("SELECT * FROM tasks")
results = cursor.fetchall()

# ❌ Wrong - fetchone returns one row
cursor.execute("SELECT * FROM tasks")
results = cursor.fetchone()  # ← Only gets first row

# ✅ Correct - fetchall returns all rows
cursor.execute("SELECT * FROM tasks")
results = cursor.fetchall()
```

---

## 🎮 Playground Issues

### "Playground hangs or won't exit"

**Problem**: Interactive console waiting for input.

**Solution**:
```python
# To exit playground:
>>> exit()
# or
>>> quit()
# or press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows)
```

---

### "Function not available in playground"

**Problem**: Function not imported into playground namespace.

**Solution**:
```python
# Import it yourself
>>> from models.todo import Task
>>> Task.create("My task", "Description", "high")

# Or use the helper functions
>>> test_task()  # Tests your Task implementation
```

---

## 📝 Validation Issues

### "ValidationError not being raised"

**Problem**: Validation function not checking properly.

**Solution**:
```python
# ❌ Wrong - doesn't check empty string
def validate_task_title(title):
    if title is None:
        raise ValidationError("Title cannot be empty")

# ✅ Correct - checks both None and empty
def validate_task_title(title):
    if not title or not title.strip():
        raise ValidationError("Title cannot be empty")

# Test it:
validate_task_title("")  # Should raise error
validate_task_title("   ")  # Should raise error
validate_task_title("Valid")  # Should not raise error
```

---

## 🔄 Git/GitHub Issues

### "Permission denied" when pushing

**Problem**: Not authenticated with GitHub.

**Solution**:
```bash
# Authenticate with GitHub CLI
gh auth login

# Or check your git remote
git remote -v

# Should show your repository URL
```

---

### "Merge conflict"

**Problem**: Local and remote changes conflict.

**Solution**:
```bash
# 1. Stash your changes
git stash

# 2. Pull latest changes
git pull

# 3. Apply your changes back
git stash pop

# 4. Resolve any conflicts in your editor
# 5. Commit and push
git add .
git commit -m "Resolved conflicts"
git push
```

---

## 🆘 Still Stuck?

### Debug Checklist

- [ ] Read the error message carefully (it tells you what's wrong!)
- [ ] Check the line number in the error
- [ ] Look for typos in variable/function names
- [ ] Verify indentation is correct
- [ ] Make sure you're in the project root directory
- [ ] Try the simplest possible test first
- [ ] Check the reference implementation (library.py)
- [ ] Search the error message online

### Get Help

1. **Check documentation**:
   - [CONCEPTS.md](CONCEPTS.md) - Fundamentals
   - [EXERCISES.md](exercises/EXERCISES.md) - Detailed guides
   - [WORKFLOW.md](WORKFLOW.md) - Step-by-step

2. **Use the playground**:
   ```bash
   python playground.py
   >>> demo_library()  # See how it should work
   ```

3. **Ask for help**:
   - Open a GitHub issue
   - Include the error message
   - Include what you tried
   - Include relevant code

### Debugging Tips

```python
# Add print statements to see what's happening
def my_function(arg):
    print(f"DEBUG: arg = {arg}")  # ← Add this
    result = do_something(arg)
    print(f"DEBUG: result = {result}")  # ← And this
    return result

# Use the Python debugger
import pdb; pdb.set_trace()  # ← Execution stops here
# Then use: n (next), s (step), c (continue), p variable (print)

# Test in REPL
python
>>> from models.todo import Task
>>> Task.create("Test", "Test", "low")
>>> # See what happens step by step
```

---

## 💡 Prevention Tips

1. **Test frequently** - Don't write lots of code before testing
2. **Read error messages** - They tell you exactly what's wrong
3. **Use version control** - Commit working code often
4. **Follow the patterns** - Study library.py for examples
5. **Start simple** - Get basic version working first
6. **Use the tools** - test_my_code.py and playground.py are your friends

---

**Remember**: Every developer faces these issues. Debugging is a skill you're learning too! 🚀


---

## 🔗 Navigation

**You are here**: TROUBLESHOOTING.md (Bookmark this for when you're stuck!)

**Still Need Help?**
- 📖 [Concepts](CONCEPTS.md) - Understand fundamentals
- 📋 [Exercises](exercises/EXERCISES.md) - Detailed guides with hints
- 📚 [Database Schemas](docs/DATABASE_SCHEMAS.md) - Visual diagrams
- 📋 [Workflow](WORKFLOW.md) - Step-by-step guide

**Testing & Exploration**:
- 🧪 Test: `python test_my_code.py -v`
- 🎮 Playground: `python playground.py`
- ⚡ [Quick Reference](QUICK_REFERENCE.md) - Commands

**Track Progress**:
- 📊 [Progress Tracker](PROGRESS_TRACKER.md) - Mark what you've completed

**Back to Start**:
- 👋 [Start Here](START_HERE.md)
- 📖 [README](README.md)
- 🚀 [Getting Started](GETTING_STARTED.md)
