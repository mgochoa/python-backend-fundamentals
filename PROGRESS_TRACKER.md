# 📊 Progress Tracker

Track your learning journey through the Python Backend Learning Project!

## 🎯 Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0%   Just started
[████░░░░░░░░░░░░░░░░] 20%  Completed Phase 1 (Study)
[████████░░░░░░░░░░░░] 40%  Completed Phase 2 (Build)
[████████████████████] 100% Completed all phases!
```

**Your Progress**: _____ / 18 stories completed

---

## 📚 Phase 1: Study & Understand (Stories 1-3)

**Goal**: Learn how backend systems work by studying a complete implementation.

**Time Estimate**: 4.5 hours

### ✅ Story 1: Project Setup
- [ ] Python 3.7+ installed and verified
- [ ] Database initialized (`python setup.py`)
- [ ] Demo runs successfully (`python main.py`)
- [ ] Sample data loaded (optional)
- [ ] Playground works (`python playground.py`)

**Completed**: _____ / _____ (date)

### ✅ Story 2: Study Library System - Books
- [ ] Read `models/library.py` Book class
- [ ] Understand `Book.create()` - INSERT operations
- [ ] Understand `Book.get_by_id()` - SELECT with WHERE
- [ ] Understand `Book.get_all()` - SELECT with filtering
- [ ] Understand `Book.update()` - UPDATE operations
- [ ] Understand `Book.delete()` - DELETE operations
- [ ] Understand `Book.search()` - LIKE queries
- [ ] Can explain validation and error handling

**Completed**: _____ / _____ (date)

**Notes**: _______________________________________

### ✅ Story 3: Study Library System - Relationships
- [ ] Read Member class in `models/library.py`
- [ ] Read Loan class in `models/library.py`
- [ ] Understand foreign key relationships
- [ ] Understand `Loan.create()` - creating related records
- [ ] Understand `Loan.get_by_member()` - JOIN operations
- [ ] Understand `Loan.return_book()` - updating related records
- [ ] Can explain how books, members, and loans connect
- [ ] Viewed database schema diagram

**Completed**: _____ / _____ (date)

**Notes**: _______________________________________

---

## ✅ Phase 2: Guided Implementation (Stories 4-9)

**Goal**: Build the Todo system with guidance and TODOs.

**Time Estimate**: 6-9 hours

### ✅ Story 4: Implement Todo Validators
- [ ] Implemented `validate_task_title()`
- [ ] Implemented `validate_task_status()`
- [ ] Implemented `validate_task_priority()`
- [ ] All validators raise `ValidationError` for invalid input
- [ ] All validators have clear error messages
- [ ] Tested with `python test_my_code.py --validators`

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 5: Implement Task.create()
- [ ] Task must have non-empty title
- [ ] Description is optional
- [ ] Task starts with 'pending' status
- [ ] Task has priority (low/medium/high)
- [ ] System returns task ID
- [ ] Validation errors handled properly
- [ ] Tested with `python test_my_code.py --todo`

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 6: Implement Task.get_all()
- [ ] Shows all tasks with details
- [ ] Can filter by status
- [ ] Sorted by creation date (newest first)
- [ ] Returns empty list if no tasks
- [ ] Validates status parameter if provided
- [ ] Tested successfully

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 7: Implement Task.update_status()
- [ ] Can change status to any valid value
- [ ] System validates status values
- [ ] Returns True if task updated
- [ ] Returns False if task doesn't exist
- [ ] Raises ValidationError for invalid status
- [ ] Tested successfully

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 8: Implement Task.delete()
- [ ] Task permanently removed from database
- [ ] Returns True if task deleted
- [ ] Returns False if task doesn't exist
- [ ] Does not affect other tasks
- [ ] Tested successfully
- [ ] All Todo tests pass!

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 9: Implement Category System (Optional)
- [ ] Can create categories with unique names
- [ ] Can assign task to category
- [ ] Can list tasks by category
- [ ] Can list all categories
- [ ] Foreign key relationship works
- [ ] All CRUD operations implemented
- [ ] Tested successfully

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

---

## 📦 Phase 3: Challenge Implementation (Stories 10-15)

**Goal**: Design and build the Inventory system independently.

**Time Estimate**: 14.5 hours

### ✅ Story 10: Design Inventory Schema
- [ ] Products table with all required fields
- [ ] Categories table with structure
- [ ] Suppliers table with contact info
- [ ] Product-Category junction table
- [ ] Foreign key relationships defined
- [ ] Appropriate constraints added
- [ ] Schema executes without errors

**Completed**: _____ / _____ (date)

**Design decisions**: _______________________________________

### ✅ Story 11: Implement Product CRUD Operations
- [ ] `Product.create()` - adds products with validation
- [ ] `Product.get_by_id()` - retrieves product
- [ ] `Product.get_all()` - lists products with filters
- [ ] `Product.update()` - updates product fields
- [ ] `Product.delete()` - removes products
- [ ] All validation works
- [ ] All functions tested

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 12: Implement Stock Management
- [ ] `Product.update_stock()` - adjusts quantity
- [ ] Can increase or decrease stock
- [ ] Stock cannot go negative
- [ ] Returns error if stock would go negative
- [ ] Tested with various scenarios

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 13: Implement Category and Supplier Models
- [ ] Category class with full CRUD
- [ ] Supplier class with full CRUD
- [ ] `Category.get_products()` - lists products
- [ ] `Supplier.get_products()` - lists products
- [ ] All functions tested

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 14: Implement Many-to-Many Relationships
- [ ] `Product.add_category()` - links product to category
- [ ] `Product.remove_category()` - unlinks
- [ ] `Product.get_categories()` - lists categories
- [ ] Junction table used correctly
- [ ] All functions tested

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

### ✅ Story 15: Implement Low Stock Alerts
- [ ] `Product.get_low_stock()` - returns products below threshold
- [ ] Includes supplier information (JOIN)
- [ ] Sorted by stock level (lowest first)
- [ ] Threshold is configurable
- [ ] Tested successfully

**Completed**: _____ / _____ (date)

**Challenges faced**: _______________________________________

---

## 🌟 Bonus Stories (Optional)

### ✅ Story 16: Add Due Dates to Tasks
- [ ] Added `due_date` field to tasks table
- [ ] Implemented `Task.set_due_date()`
- [ ] Implemented `Task.get_overdue()`
- [ ] Implemented `Task.get_due_soon()`
- [ ] Validates due dates not in past

**Completed**: _____ / _____ (date)

### ✅ Story 17: Create CLI Interface
- [ ] CLI supports all CRUD operations
- [ ] Uses argparse for command parsing
- [ ] Provides helpful error messages
- [ ] Includes help text
- [ ] Tested with various commands

**Completed**: _____ / _____ (date)

### ✅ Story 18: Create REST API
- [ ] Flask API with all CRUD endpoints
- [ ] JSON request/response handling
- [ ] Proper HTTP status codes
- [ ] Error handling and validation
- [ ] API documentation

**Completed**: _____ / _____ (date)

---

## 📈 Skills Acquired

Check off skills as you master them:

### Database Design
- [ ] Creating tables with appropriate data types
- [ ] Using PRIMARY KEY and AUTOINCREMENT
- [ ] Adding NOT NULL constraints
- [ ] Adding UNIQUE constraints
- [ ] Setting DEFAULT values
- [ ] Creating foreign key relationships
- [ ] Designing one-to-many relationships
- [ ] Designing many-to-many relationships
- [ ] Using junction tables

### SQL Operations
- [ ] INSERT - Creating records
- [ ] SELECT - Reading records
- [ ] UPDATE - Modifying records
- [ ] DELETE - Removing records
- [ ] WHERE - Filtering results
- [ ] ORDER BY - Sorting results
- [ ] JOIN - Combining tables
- [ ] LEFT JOIN - Optional relationships
- [ ] LIKE - Pattern matching
- [ ] Parameterized queries

### Python Database Interaction
- [ ] Connecting to SQLite database
- [ ] Executing SQL queries
- [ ] Using parameterized queries (SQL injection prevention)
- [ ] Fetching single records (fetchone)
- [ ] Fetching multiple records (fetchall)
- [ ] Getting last inserted ID
- [ ] Checking affected rows
- [ ] Handling database errors

### Data Validation
- [ ] Validating required fields
- [ ] Validating field types
- [ ] Validating field values (choices)
- [ ] Validating numeric ranges
- [ ] Creating custom validators
- [ ] Raising ValidationError
- [ ] Writing clear error messages

### Error Handling
- [ ] Try-except blocks
- [ ] Custom exception classes
- [ ] Converting technical errors to user-friendly messages
- [ ] Logging errors
- [ ] Handling database errors
- [ ] Handling validation errors

### Code Organization
- [ ] Structuring model classes
- [ ] Separating concerns (models, validation, utilities)
- [ ] Writing reusable functions
- [ ] Using class methods
- [ ] Writing docstrings
- [ ] Adding helpful comments

---

## 🎓 Reflection

### What I Learned
_______________________________________
_______________________________________
_______________________________________

### What Was Challenging
_______________________________________
_______________________________________
_______________________________________

### What I'm Proud Of
_______________________________________
_______________________________________
_______________________________________

### Next Steps
_______________________________________
_______________________________________
_______________________________________

---

## 🏆 Achievements

Celebrate your milestones!

- [ ] 🎯 **First Steps** - Completed setup and ran first demo
- [ ] 📚 **Student** - Studied complete reference implementation
- [ ] ✅ **Validator** - Implemented all validation functions
- [ ] 🔨 **Builder** - Completed first CRUD operation
- [ ] 🎨 **Designer** - Designed database schema from scratch
- [ ] 🔗 **Connector** - Implemented many-to-many relationships
- [ ] 🧪 **Tester** - All tests passing
- [ ] 🚀 **Graduate** - Completed all core stories
- [ ] ⭐ **Overachiever** - Completed bonus stories

---

## 📊 Time Tracking

| Phase | Estimated | Actual | Notes |
|-------|-----------|--------|-------|
| Phase 1 (Study) | 4.5 hrs | _____ hrs | _____ |
| Phase 2 (Build) | 6-9 hrs | _____ hrs | _____ |
| Phase 3 (Design) | 14.5 hrs | _____ hrs | _____ |
| Bonus | Variable | _____ hrs | _____ |
| **Total** | **25-28 hrs** | **_____ hrs** | |

---

**Keep going!** Every checkbox is progress. Every error is learning. You've got this! 💪

**Need help?** Check [WORKFLOW.md](WORKFLOW.md) for step-by-step guidance.


---

## 🔗 Navigation

**You are here**: PROGRESS_TRACKER.md (Bookmark this page!)

**Working on a Story?**
- 📋 [Workflow](WORKFLOW.md) - Step-by-step guide
- ⚡ [Quick Reference](QUICK_REFERENCE.md) - Commands
- 🧪 Test: `python test_my_code.py`
- 🎮 Playground: `python playground.py`

**Need Help?**
- 🔧 [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- 📚 [Database Schemas](docs/DATABASE_SCHEMAS.md) - Visual diagrams
- 📖 [Concepts](CONCEPTS.md) - Fundamentals
- 📋 [Exercises](exercises/EXERCISES.md) - Detailed guides

**Back to Start**:
- 👋 [Start Here](START_HERE.md)
- 📖 [README](README.md)
- 🚀 [Getting Started](GETTING_STARTED.md)
