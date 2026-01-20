# Project Structure Documentation

This document explains the directory structure and organization of the Python Backend Learning Project.

## Directory Overview

```
python-backend-learning-project/
├── config/                    # Configuration files
│   └── database.py           # Database path and connection settings
│
├── database/                  # Database-related code
│   ├── __init__.py           # Package initialization
│   ├── schemas/              # SQL schema definitions
│   │   └── .gitkeep         # (Placeholder - schemas added in later tasks)
│   └── migrations/           # Database initialization scripts
│       └── .gitkeep         # (Placeholder - migrations added in later tasks)
│
├── models/                    # Data models and CRUD operations
│   └── __init__.py           # Package initialization
│   # Files to be added:
│   # - library.py (Complete reference implementation)
│   # - todo.py (Guided implementation with TODOs)
│   # - inventory.py (Challenge implementation)
│
├── validation/                # Input validation utilities
│   ├── __init__.py           # Package initialization
│   └── exercises/            # Validation exercises for students
│       └── .gitkeep         # (Placeholder - exercises added in later tasks)
│   # Files to be added:
│   # - validators.py (Example validation functions)
│
├── utils/                     # Utility modules
│   └── __init__.py           # Package initialization
│   # Files to be added:
│   # - error_handlers.py (Custom exceptions and error handling)
│   # - logger.py (Logging configuration)
│
├── exercises/                 # Exercise documentation and solutions
│   └── .gitkeep              # (Placeholder - exercises added in later tasks)
│   # Files to be added:
│   # - EXERCISES.md (Detailed exercise instructions)
│   # - solutions/ (Reference solutions)
│
├── data/                      # Database files (auto-created, git-ignored)
│   └── learning_project.db   # SQLite database (created when setup runs)
│
├── .gitignore                 # Git ignore rules for Python projects
├── requirements.txt           # Python dependencies (minimal)
└── PROJECT_STRUCTURE.md       # This file

```

## Package Descriptions

### config/
Contains configuration settings for the application. Currently includes database configuration with:
- Database file path (using cross-platform Path handling)
- Connection timeout settings
- Thread safety configuration

**Key Learning Points:**
- Centralized configuration management
- Cross-platform path handling with pathlib
- Automatic directory creation

### database/
Houses all database-related code, organized into:
- **schemas/**: SQL CREATE TABLE statements for each topic area
- **migrations/**: Scripts to initialize and update database structure
- **connection.py** (to be added): Database connection management and query execution

**Key Learning Points:**
- Separating database concerns from business logic
- SQL schema design and constraints
- Database connection lifecycle management

### models/
Contains the business logic and CRUD operations for each topic area:
- **library.py**: Complete reference implementation (study this!)
- **todo.py**: Guided implementation with TODOs (complete these!)
- **inventory.py**: Challenge implementation (design and build yourself!)

**Key Learning Points:**
- CRUD operations (Create, Read, Update, Delete)
- Parameterized queries for SQL injection prevention
- Data validation before database operations
- Error handling patterns

### validation/
Provides validation utilities and exercises:
- **validators.py**: Reusable validation functions
- **exercises/**: Validation exercises for students to complete

**Key Learning Points:**
- Input validation patterns
- Clear error messages
- Reusable validation functions
- Validation before database operations

### utils/
Contains utility modules for cross-cutting concerns:
- **error_handlers.py**: Custom exception classes and error handling
- **logger.py**: Logging configuration for debugging

**Key Learning Points:**
- Custom exception hierarchies
- Converting technical errors to user-friendly messages
- Logging for debugging and monitoring

### exercises/
Documentation and solutions for learning exercises:
- **EXERCISES.md**: Detailed exercise instructions with learning objectives
- **solutions/**: Reference implementations for completed exercises

**Key Learning Points:**
- Progressive difficulty levels
- Clear learning objectives
- Hints and tips for each exercise

## Design Principles

### 1. Separation of Concerns
Each package has a specific responsibility:
- `database/` handles data storage
- `models/` handles business logic
- `validation/` handles input validation
- `utils/` provides cross-cutting utilities

### 2. Progressive Difficulty
Three levels of scaffolding:
- **Reference**: Complete implementation to study (Library System)
- **Guided**: Partial implementation with TODOs (Todo System)
- **Challenge**: Minimal scaffolding for independent work (Inventory System)

### 3. Educational Focus
Every file includes:
- Comprehensive docstrings explaining concepts
- Inline comments highlighting learning points
- Clear examples demonstrating patterns
- TODOs with detailed instructions

### 4. Minimal Dependencies
The project uses only Python's built-in `sqlite3` module for core functionality, making it:
- Easy to set up
- Portable across platforms
- Focused on fundamentals

## Next Steps

After setting up the project structure, the next tasks will:
1. Implement database connection management
2. Create SQL schemas for each topic area
3. Build model classes with CRUD operations
4. Add validation utilities and exercises
5. Create comprehensive documentation

## Verification

To verify the project structure is set up correctly:

```bash
# Test that configuration works
python3 -c "from config.database import get_database_path; print(get_database_path())"

# Test that all packages import
python3 -c "import database; import models; import validation; import utils; print('✓ Success')"
```

Both commands should run without errors.

## Learning Path

Students should work through the project in this order:
1. **Study Phase**: Read and understand the Library System implementation
2. **Guided Phase**: Complete TODOs in the Todo System
3. **Challenge Phase**: Design and implement the Inventory System independently

Each phase builds on concepts from the previous phase, ensuring progressive skill development.
