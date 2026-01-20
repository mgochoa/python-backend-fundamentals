# Student Workflow Guide

This guide shows you exactly how to work through the project, step by step.

## 📋 Daily Workflow

### Starting a New Story

1. **Check GitHub Project Board**
   - Go to your project board
   - Pick the next story in sequence
   - Move it to "In Progress"

2. **Read the Story**
   - Read the user story and acceptance criteria
   - Review the learning objectives
   - Check the implementation notes

3. **Review Documentation**
   - Check `CONCEPTS.md` for relevant concepts
   - Review `EXERCISES.md` for detailed instructions
   - Study the reference implementation if needed

### Working on the Code

4. **Open the File**
   ```bash
   # For validators (Story 4)
   code validation/exercises/todo_validators.py
   
   # For Task model (Stories 5-8)
   code models/todo.py
   
   # For Inventory (Stories 10-15)
   code models/inventory.py
   code database/schemas/inventory_schema.sql
   ```

5. **Find the TODOs**
   - Look for `# TODO:` comments
   - Read the instructions carefully
   - Check the hints and examples

6. **Implement the Function**
   - Write your code following the TODO instructions
   - Use the reference implementation as a guide
   - Add comments to explain your logic

### Testing Your Work

7. **Quick Test**
   ```bash
   # Test what you just implemented
   python test_my_code.py
   
   # Or test specific parts
   python test_my_code.py --validators
   python test_my_code.py --todo
   ```

8. **Interactive Testing**
   ```bash
   # Launch playground
   python playground.py
   ```
   
   Then in the playground:
   ```python
   >>> test_task()  # Test your Task implementation
   >>> Task.create("Test", "Testing my code", "high")  # Try it manually
   >>> Task.get_all()  # See if it works
   ```

9. **Fix Any Issues**
   - Read error messages carefully
   - Check your code against the reference
   - Test again until it works

### Completing a Story

10. **Final Verification**
    ```bash
    # Run all tests
    python test_my_code.py -v
    
    # Try it in the playground
    python playground.py
    ```

11. **Update GitHub**
    - Check off completed acceptance criteria
    - Move issue to "Done" on project board
    - Add any notes or learnings

12. **Celebrate!** 🎉
    - You completed a story!
    - Take a break if needed
    - Move to the next story

## 🎯 Story-by-Story Guide

### Story 1: Project Setup
```bash
python setup.py              # Initialize database
python main.py               # Run demo
python database/sample_data.py  # Load sample data
```
✅ Done when: Everything runs without errors

### Story 2: Study Library System
```bash
# Open and read
code models/library.py
code database/schemas/library_schema.sql

# Try it in playground
python playground.py
>>> demo_library()
>>> Book.get_all()
>>> Book.search("Python")
```
✅ Done when: You understand how CRUD operations work

### Story 3: Study Relationships
```bash
# Open and read
code models/library.py  # Focus on Member and Loan classes

# Try it in playground
python playground.py
>>> from models.library import Member, Loan
>>> Member.get_all()
>>> Loan.get_by_member(1)
```
✅ Done when: You understand foreign keys and JOINs

### Story 4: Implement Validators
```bash
# Edit the file
code validation/exercises/todo_validators.py

# Test as you go
python test_my_code.py --validators

# Try in playground
python playground.py
>>> from validation.exercises.todo_validators import validate_task_title
>>> validate_task_title("My task")  # Should work
>>> validate_task_title("")  # Should raise error
```
✅ Done when: All validator tests pass

### Story 5: Implement Task.create()
```bash
# Edit the file
code models/todo.py  # Find Task.create() TODO

# Test it
python test_my_code.py --todo

# Try it
python playground.py
>>> Task.create("My first task", "Description", "high")
```
✅ Done when: You can create tasks successfully

### Story 6: Implement Task.get_all()
```bash
# Edit the file
code models/todo.py  # Find Task.get_all() TODO

# Test it
python test_my_code.py --todo

# Try it
python playground.py
>>> Task.get_all()
>>> Task.get_all(status="pending")
```
✅ Done when: You can retrieve and filter tasks

### Story 7: Implement Task.update_status()
```bash
# Edit the file
code models/todo.py  # Find Task.update_status() TODO

# Test it
python test_my_code.py --todo

# Try it
python playground.py
>>> task_id = Task.create("Test", "Test", "low")
>>> Task.update_status(task_id, "in_progress")
>>> Task.get_all()  # Verify status changed
```
✅ Done when: You can update task status

### Story 8: Implement Task.delete()
```bash
# Edit the file
code models/todo.py  # Find Task.delete() TODO

# Test it
python test_my_code.py --todo

# Try it
python playground.py
>>> task_id = Task.create("Delete me", "Test", "low")
>>> Task.delete(task_id)
>>> Task.get_all()  # Verify it's gone
```
✅ Done when: You can delete tasks safely

### Stories 9-15: Continue the Pattern
- Read the story
- Find the TODOs (or design from scratch)
- Implement the code
- Test with `test_my_code.py`
- Experiment in `playground.py`
- Verify and move on

## 🐛 When Things Go Wrong

### "Import Error"
```bash
# Make sure you're in the project root
pwd  # Should show .../python-backend-fundamentals

# Try importing in Python
python
>>> import models.todo
>>> # If this works, your imports are fine
```

### "Database Not Found"
```bash
# Reinitialize the database
python setup.py
```

### "Tests Failing"
```bash
# This is normal! Read the error message
python test_my_code.py -v

# Common issues:
# - Function not implemented (still has 'pass' or 'raise NotImplementedError')
# - Wrong return type (returning None instead of a value)
# - Missing validation (not checking inputs)
# - SQL syntax error (check your query)
```

### "Not Sure What to Do"
```bash
# Study the reference implementation
code models/library.py

# Read the concepts
code CONCEPTS.md

# Check the exercises guide
code exercises/EXERCISES.md

# Try the playground
python playground.py
>>> demo_library()  # See how it should work
```

## 💡 Pro Tips

### Tip 1: Test Early, Test Often
Don't wait until you've implemented everything. Test each function as you complete it:
```bash
# After implementing validate_task_title
python test_my_code.py --validators

# After implementing Task.create()
python test_my_code.py --todo
```

### Tip 2: Use the Playground
The playground is your safe space to experiment:
```python
# Try things without fear
>>> Task.create("Test", "Just testing", "low")
>>> # Oops, that didn't work. Let me check the error...
>>> # Fix the code, then try again
```

### Tip 3: Study the Reference
When stuck, look at how the library system does it:
```python
# Your TODO: Implement Task.create()
# Reference: Look at Book.create() in models/library.py
# They follow the same pattern!
```

### Tip 4: Read Error Messages
Error messages tell you exactly what's wrong:
```
ValidationError: Title cannot be empty
# ^ This tells you the validation is working!

AttributeError: 'NoneType' object has no attribute 'fetchall'
# ^ This means your query returned None - check your SQL
```

### Tip 5: Take Breaks
Learning takes time. If you're stuck:
1. Take a 10-minute break
2. Come back with fresh eyes
3. Read the error message again
4. Check the reference implementation
5. Try a different approach

## 📊 Tracking Progress

### Daily Checklist
- [ ] Picked a story from the project board
- [ ] Read the story and documentation
- [ ] Implemented the code
- [ ] Tested with `test_my_code.py`
- [ ] Experimented in `playground.py`
- [ ] Updated GitHub issue
- [ ] Moved to next story or took a break

### Weekly Review
- How many stories completed?
- What concepts did I learn?
- What was challenging?
- What do I want to focus on next week?

## 🎓 Learning Mindset

Remember:
- **Errors are learning opportunities** - They tell you what to fix
- **Testing is your friend** - It shows you what works and what doesn't
- **The reference is there to help** - Study it when stuck
- **Progress over perfection** - Working code is better than perfect code
- **Ask for help** - Use GitHub issues to ask questions

## 🚀 Ready to Start?

```bash
# Initialize everything
python setup.py
python main.py
python database/sample_data.py

# Start with Story 1
# Then move to Story 2
# Keep going!

# Test as you work
python test_my_code.py

# Experiment freely
python playground.py
```

Happy learning! 🎉
