# Python Backend Learning Project

A hands-on educational project designed to teach Python and SQL fundamentals through practical backend development. Learn database design, CRUD operations, data validation, and error handling by building three progressively challenging systems.

## 🎯 Learning Objectives

By completing this project, you will learn:

- **Database Design**: Tables, relationships, constraints, and normalization
- **SQL Fundamentals**: SELECT, INSERT, UPDATE, DELETE, and JOIN operations
- **Python Database Interaction**: Using sqlite3 module with parameterized queries
- **CRUD Operations**: Create, Read, Update, and Delete patterns
- **Data Validation**: Input validation and error handling best practices
- **Code Organization**: Structuring a backend project with models, utilities, and interfaces

## 📚 Project Structure

The project is organized into three topic areas with increasing difficulty:

### 1. **Library System** (Reference Implementation - Study This!)
A complete, working implementation demonstrating all concepts. Study this code to understand:
- How to structure model classes
- How to implement CRUD operations
- How to validate input and handle errors
- How to work with relationships between tables

**Features**: Books, Members, Loans with full CRUD operations

### 2. **Todo System** (Guided Exercise - Build This!)
A partially implemented system with clear TODOs and scaffolding. You'll complete:
- Task creation with validation
- Status and priority management
- Filtering and searching
- Category organization (optional)

**Features**: Tasks with status tracking, priorities, and optional categories

### 3. **Inventory System** (Challenge - Design This!)
Minimal scaffolding for independent practice. You'll design and implement:
- Product management with stock tracking
- Supplier relationships
- Category organization (many-to-many)
- Low stock alerts

**Features**: Products, Categories, Suppliers with complex relationships

## 🚀 Getting Started

### Prerequisites

- **Python 3.7 or higher** - [Download Python](https://www.python.org/downloads/)
- **SQLite3** - Included with Python (no separate installation needed)
- **Text Editor or IDE** - VS Code, PyCharm, or any editor you prefer

### Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd python-backend-learning-project
   ```

2. **Verify Python installation**
   ```bash
   python --version
   # Should show Python 3.7 or higher
   ```

3. **Initialize the database**
   ```bash
   python setup.py
   ```
   
   This will:
   - Create the database file (`data/learning_project.db`)
   - Execute all schema files to create tables
   - Verify the setup was successful

   **Expected output:**
   ```
   ✓ Data directory ready: data
   ✓ Executed schema: library_schema.sql
   ✓ Executed schema: todo_schema.sql
   ✓ Executed schema: inventory_schema.sql
   ✓ Database setup completed successfully!
   ```

4. **Run the demo script**
   ```bash
   python main.py
   ```
   
   This demonstrates the Library System and provides a template for your Todo System implementation.

5. **Test your code as you work**
   ```bash
   python test_my_code.py
   ```
   
   This interactive test script checks your TODO implementations and gives immediate feedback.

6. **Explore interactively**
   ```bash
   python playground.py
   ```
   
   Launch an interactive environment to experiment with your code safely.

7. **Populate with sample data (optional but recommended)**
   ```bash
   python database/sample_data.py
   ```
   
   This creates realistic example data including books, members, and loans. Great for:
   - Testing queries without manual data entry
   - Seeing the system in action
   - Understanding relationships between entities
   - Having data to experiment with

### First Steps

1. **Study the Library System** (`models/library.py`)
   - Read through the complete implementation
   - Understand the CRUD patterns
   - Note how validation and error handling work

2. **Read the Concepts Guide** (`CONCEPTS.md`)
   - Learn database design fundamentals
   - Understand SQL query patterns
   - Review Python database interaction

3. **Complete the Todo System** (`models/todo.py`)
   - Start with the validation functions
   - Implement `Task.create()` following the TODOs
   - Complete `Task.get_all()`, `Task.update_status()`, and `Task.delete()`
   - Test your implementation with `python test_my_code.py`

4. **Challenge Yourself** (`models/inventory.py`)
   - Design the complete schema
   - Implement all CRUD operations
   - Handle complex relationships
   - Add business logic (stock management)

## 🧪 Testing Your Code

### Quick Testing (Recommended)

```bash
# Test all your TODO implementations
python test_my_code.py

# Test only validators
python test_my_code.py --validators

# Test only Todo model
python test_my_code.py --todo

# Show detailed output
python test_my_code.py --verbose
```

The test script will:
- ✅ Check if your functions are implemented
- ✅ Test with valid and invalid inputs
- ✅ Show clear success/error messages
- ✅ Give you immediate feedback on what to fix

### Interactive Playground

```bash
python playground.py
```

The playground provides an interactive environment where you can:
- 🔍 Explore what's available with `explore()`
- 📚 See the reference implementation with `demo_library()`
- ✅ Test validators with `demo_validators()`
- ✏️ Test your Task implementation with `test_task()`
- 💻 Experiment with any Python code safely

Example session:
```python
>>> explore()           # See what's available
>>> demo_library()      # Watch the library system work
>>> test_task()         # Test your Task implementation
>>> Task.create("My task", "Description", "high")  # Try it yourself!
>>> exit()              # Leave when done
```

## 📖 Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete setup and learning path guide
- **[WORKFLOW.md](WORKFLOW.md)** - Step-by-step workflow for working through stories
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference and cheat sheet
- **[CONCEPTS.md](CONCEPTS.md)** - Database and SQL fundamentals
- **[exercises/EXERCISES.md](exercises/EXERCISES.md)** - Detailed exercise guide with hints
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Detailed project organization

## 🗂️ Directory Structure

```
python-backend-learning-project/
├── README.md                          # This file
├── CONCEPTS.md                        # Educational content
├── setup.py                           # Database initialization
├── main.py                            # Demo script
├── requirements.txt                   # Python dependencies
│
├── config/
│   └── database.py                    # Database configuration
│
├── database/
│   ├── connection.py                  # Connection management
│   ├── sample_data.py                 # Sample data population script
│   ├── schemas/
│   │   ├── library_schema.sql         # Complete example
│   │   ├── todo_schema.sql            # Guided exercise
│   │   └── inventory_schema.sql       # Challenge
│   └── migrations/
│       └── init_db.py                 # Database initialization
│
├── models/
│   ├── library.py                     # Complete reference (STUDY THIS)
│   ├── todo.py                        # Guided exercise (COMPLETE THIS)
│   └── inventory.py                   # Challenge (BUILD THIS)
│
├── validation/
│   ├── validators.py                  # Example validation functions
│   ├── demo_validators.py             # Additional examples
│   └── exercises/
│       └── todo_validators.py         # Validation exercises
│
├── utils/
│   ├── error_handlers.py              # Error handling utilities
│   └── logger.py                      # Logging configuration
│
├── examples/
│   ├── cli_example.py                 # Optional CLI interface
│   └── api_example.py                 # Optional Flask API
│
└── exercises/
    ├── EXERCISES.md                   # Detailed exercise guide
    └── solutions/
        ├── todo_complete.py           # Complete Todo implementation
        └── todo_validators_complete.py # Complete validators
```

## 🎓 Learning Path

### Beginner Level
1. Study `models/library.py` - Complete reference implementation
2. Read `CONCEPTS.md` - Understand database fundamentals
3. Complete validation functions in `validation/exercises/todo_validators.py`
4. Implement `Task.create()` in `models/todo.py`

### Intermediate Level
1. Implement `Task.get_all()` with filtering
2. Implement `Task.update_status()` and `Task.delete()`
3. Add the Category model (optional)
4. Create a simple CLI or script to use your Todo System

### Advanced Level
1. Design the complete Inventory schema
2. Implement all Product, Category, and Supplier models
3. Handle many-to-many relationships
4. Implement business logic (stock management, low stock alerts)
5. Add comprehensive error handling

## 🔧 Common Commands

### Database Setup
```bash
# Initialize database (first time)
python setup.py

# Populate with sample data (optional but recommended)
python database/sample_data.py
```

### Working with Sample Data

After running `python database/sample_data.py`, you'll have:
- **16 books** across different genres (programming, science, fiction, etc.)
- **8 library members** with realistic names and emails
- **6 active loans** (books currently checked out)
- **5 completed loans** (returned books with history)
- **1 overdue loan** (for testing overdue scenarios)

This sample data lets you:
- Test queries without manually creating data
- See relationships between books, members, and loans
- Practice with realistic examples
- Understand how the system works with real data

**Note**: Running the sample data script will clear any existing data in the database!

# Reinitialize database (WARNING: deletes all data)
python setup.py --force
```

### Running Examples
```bash
# Run the main demo script
python main.py

# Run CLI example (optional)
python examples/cli_example.py --help

# Run API example (optional, requires Flask)
python examples/api_example.py
```

### Testing Your Code
```bash
# Run unit tests (if you create them)
python -m pytest

# Run specific test file
python -m pytest test_library_models.py
```

### Interactive Python REPL
```bash
# Start Python interactive shell
python

# Then import and use your models:
>>> from models.library import Book
>>> book_id = Book.create("Test Book", "Test Author", "1234567890")
>>> book = Book.get_by_id(book_id)
>>> print(book)
```

## 🐛 Troubleshooting

### "Database is locked" Error
**Problem**: Another program is accessing the database.

**Solutions**:
- Close any SQLite browser or database tools
- Close other Python scripts using the database
- Restart your terminal/IDE
- Delete `data/learning_project.db` and run `python setup.py` again

### "No such table" Error
**Problem**: Database tables haven't been created.

**Solutions**:
- Run `python setup.py` to initialize the database
- Check that schema files exist in `database/schemas/`
- Verify schema files have valid SQL syntax

### "Module not found" Error
**Problem**: Python can't find the modules.

**Solutions**:
- Make sure you're in the project root directory
- Check that `__init__.py` files exist in module directories
- Verify your Python path includes the current directory

### "Permission denied" Error
**Problem**: Can't write to the data directory.

**Solutions**:
- Check file permissions on the `data/` directory
- Try running with appropriate permissions
- On Windows, check if the file is open in another program

### Import Errors
**Problem**: `ImportError` or `ModuleNotFoundError`

**Solutions**:
- Ensure you're running Python from the project root directory
- Check that all `__init__.py` files exist
- Verify the module structure matches the imports

### SQL Syntax Errors
**Problem**: Errors when running `setup.py`

**Solutions**:
- Check your schema files for SQL syntax errors
- Test SQL statements in a SQLite browser first
- Make sure all statements end with semicolons
- Check for typos in table/column names

### Validation Errors
**Problem**: Your code raises `ValidationError` unexpectedly

**Solutions**:
- Read the error message carefully - it tells you what's wrong
- Check that required fields are not empty
- Verify data types match expectations (string, int, etc.)
- Ensure values are in allowed ranges (e.g., positive prices)

### Foreign Key Errors
**Problem**: `FOREIGN KEY constraint failed`

**Solutions**:
- Verify the referenced record exists (e.g., supplier_id exists in suppliers table)
- Check that foreign key constraints are enabled: `PRAGMA foreign_keys = ON`
- Make sure you're inserting records in the correct order (parent before child)

## 💡 Tips for Success

1. **Read Error Messages Carefully**: They tell you exactly what went wrong
2. **Start Simple**: Complete one method at a time, test it, then move on
3. **Study the Examples**: The Library System shows you how everything works
4. **Test Frequently**: Don't write all the code before testing
5. **Use the REPL**: Python's interactive shell is great for experimenting
6. **Ask Questions**: If stuck, review the reference implementation
7. **Take Notes**: Write down patterns you notice and concepts you learn
8. **Be Patient**: Learning takes time - it's okay to struggle a bit!

## 📝 Additional Resources

### Python Resources
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Python sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)

### SQL Resources
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [SQL Basics](https://www.w3schools.com/sql/)

### Database Design
- [Database Normalization](https://www.guru99.com/database-normalization.html)
- [Entity Relationship Diagrams](https://www.lucidchart.com/pages/er-diagrams)

## 🤝 Contributing

This is an educational project. If you find issues or have suggestions:
1. Check the troubleshooting section first
2. Review the concepts guide and documentation
3. Look at the reference implementation for patterns
4. Ask your instructor or mentor for guidance

## 📄 License

This project is designed for educational purposes. Feel free to use it for learning and teaching.

## 🎉 Acknowledgments

This project was designed to provide a structured, hands-on approach to learning backend development fundamentals. The progressive difficulty levels ensure that students build confidence and skills gradually.

---

**Ready to start learning?** Run `python setup.py` and then `python main.py` to see the system in action!

**Questions?** Check `CONCEPTS.md` for explanations of key concepts, or `exercises/EXERCISES.md` for detailed exercise instructions.

**Happy Learning! 🚀**
