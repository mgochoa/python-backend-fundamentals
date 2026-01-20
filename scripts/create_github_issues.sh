#!/bin/bash

# Script to create GitHub issues from GITHUB_USER_STORIES.md
# Requires: gh CLI (GitHub CLI) to be installed and authenticated
# Usage: ./create_github_issues.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== GitHub Issues Creator ===${NC}"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

echo -e "${GREEN}✓ GitHub CLI is installed and authenticated${NC}"
echo ""

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo -e "${BLUE}Repository: ${REPO}${NC}"
echo ""

# Ask for confirmation
read -p "Create issues in this repository? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${YELLOW}Creating issues...${NC}"
echo ""

# Story 1: Project Setup
gh issue create \
  --title "Story 1: Project Setup" \
  --label "setup,beginner" \
  --body "**Difficulty**: Beginner  
**Estimated Time**: 30 minutes  

**User Story**:
As a student, I want to set up the Python Backend Learning Project on my computer, so that I can start learning backend development.

**Acceptance Criteria**:
- [ ] Python 3.7+ is installed and verified
- [ ] Project is cloned/downloaded to local machine
- [ ] Database is initialized successfully (\`python setup.py\`)
- [ ] Demo script runs without errors (\`python main.py\`)
- [ ] Sample data is loaded (\`python database/sample_data.py\`)

**Learning Objectives**:
- Setting up a Python project
- Running Python scripts
- Understanding project structure

**Implementation Notes**:
- Follow the README.md \"Getting Started\" section
- Verify each step produces expected output
- Check troubleshooting section if you encounter errors"

echo -e "${GREEN}✓ Created Story 1: Project Setup${NC}"

# Story 2: Study Library System - Books
gh issue create \
  --title "Story 2: Study Library System - Books" \
  --label "reference,beginner,study" \
  --body "**Difficulty**: Beginner  
**Estimated Time**: 2 hours  
**Dependencies**: Story 1

**User Story**:
As a student, I want to study the complete Book model implementation, so that I understand how to implement CRUD operations.

**Acceptance Criteria**:
- [ ] Read and understand \`models/library.py\` Book class
- [ ] Understand \`Book.create()\` - INSERT operations
- [ ] Understand \`Book.get_by_id()\` - SELECT with WHERE
- [ ] Understand \`Book.get_all()\` - SELECT with filtering
- [ ] Understand \`Book.update()\` - UPDATE operations
- [ ] Understand \`Book.delete()\` - DELETE operations
- [ ] Understand \`Book.search()\` - LIKE queries
- [ ] Can explain validation and error handling patterns

**Learning Objectives**:
- CRUD operations (Create, Read, Update, Delete)
- SQL INSERT, SELECT, UPDATE, DELETE
- Parameterized queries
- Data validation
- Error handling

**Implementation Notes**:
- Read the code comments carefully - they explain \"why\" not just \"what\"
- Try running operations in Python REPL to see them work
- Study the validation functions used
- Note the error handling patterns"

echo -e "${GREEN}✓ Created Story 2: Study Library System - Books${NC}"

# Story 3: Study Library System - Relationships
gh issue create \
  --title "Story 3: Study Library System - Relationships" \
  --label "reference,intermediate,study" \
  --body "**Difficulty**: Intermediate  
**Estimated Time**: 2 hours  
**Dependencies**: Story 2

**User Story**:
As a student, I want to study the Member and Loan models, so that I understand how to work with relationships between tables.

**Acceptance Criteria**:
- [ ] Read and understand Member class in \`models/library.py\`
- [ ] Read and understand Loan class in \`models/library.py\`
- [ ] Understand foreign key relationships
- [ ] Understand \`Loan.create()\` - creating related records
- [ ] Understand \`Loan.get_by_member()\` - JOIN operations
- [ ] Understand \`Loan.return_book()\` - updating related records
- [ ] Can explain how books, members, and loans are connected

**Learning Objectives**:
- Foreign keys and relationships
- JOIN operations
- Multi-table queries
- Business logic implementation

**Implementation Notes**:
- Focus on how foreign keys link tables
- Study the JOIN query in \`get_by_member()\`
- Understand how \`Loan.create()\` updates book availability
- Note the transaction patterns"

echo -e "${GREEN}✓ Created Story 3: Study Library System - Relationships${NC}"

# Story 4: Implement Todo Validators
gh issue create \
  --title "Story 4: Implement Todo Validators" \
  --label "guided,beginner,validation" \
  --body "**Difficulty**: Beginner  
**Estimated Time**: 1 hour  
**Dependencies**: Story 2

**User Story**:
As a student, I want to implement validation functions for the Todo system, so that I can ensure data integrity.

**Acceptance Criteria**:
- [ ] Implement \`validate_task_title()\` in \`validation/exercises/todo_validators.py\`
- [ ] Implement \`validate_task_status()\` in \`validation/exercises/todo_validators.py\`
- [ ] Implement \`validate_task_priority()\` in \`validation/exercises/todo_validators.py\`
- [ ] All validation functions raise \`ValidationError\` for invalid input
- [ ] All validation functions have clear error messages
- [ ] Test each function with valid and invalid inputs

**Learning Objectives**:
- Input validation patterns
- Raising exceptions
- Writing clear error messages
- Testing validation logic

**Implementation Notes**:
- Follow the TODO comments in the file
- Study \`validators.py\` for examples
- Use \`validate_choice()\` pattern for status and priority
- Test in Python REPL before moving on

**Related Use Case**: UC-6 (Create a Task), UC-8 (Update Task Status)"

echo -e "${GREEN}✓ Created Story 4: Implement Todo Validators${NC}"

# Story 5: Implement Task.create()
gh issue create \
  --title "Story 5: Implement Task.create()" \
  --label "guided,beginner,crud" \
  --body "**Difficulty**: Beginner  
**Estimated Time**: 2 hours  
**Dependencies**: Story 4

**User Story**:
As a user, I want to create a new task with a title and description, so that I can track things I need to do.

**Acceptance Criteria**:
- [ ] Task must have a non-empty title
- [ ] Description is optional
- [ ] Task starts with 'pending' status
- [ ] Task has a priority (low/medium/high)
- [ ] System returns task ID
- [ ] Validation errors are handled properly
- [ ] Function is tested and working

**Learning Objectives**:
- INSERT operations
- Using validation functions
- Parameterized queries
- Returning inserted ID
- Error handling

**Implementation Notes**:
- Complete \`Task.create()\` in \`models/todo.py\`
- Follow the TODO comments step by step
- Use validation functions from Story 4
- Study \`Book.create()\` for the pattern
- Test with both valid and invalid inputs

**Related Use Case**: UC-6 (Create a Task)"

echo -e "${GREEN}✓ Created Story 5: Implement Task.create()${NC}"

# Story 6: Implement Task.get_all()
gh issue create \
  --title "Story 6: Implement Task.get_all()" \
  --label "guided,intermediate,crud" \
  --body "**Difficulty**: Intermediate  
**Estimated Time**: 1.5 hours  
**Dependencies**: Story 5

**User Story**:
As a user, I want to see all my tasks, so that I know what I need to do.

**Acceptance Criteria**:
- [ ] Shows all tasks with their details
- [ ] Can filter by status (pending/in_progress/completed)
- [ ] Sorted by creation date (newest first)
- [ ] Returns empty list if no tasks found
- [ ] Validates status parameter if provided
- [ ] Function is tested and working

**Learning Objectives**:
- SELECT queries
- Optional filtering with WHERE
- ORDER BY for sorting
- Dynamic query building
- Handling optional parameters

**Implementation Notes**:
- Complete \`Task.get_all()\` in \`models/todo.py\`
- Study \`Book.get_all()\` for the pattern
- Build query dynamically based on parameters
- Remember to validate status if provided
- Test with and without filters

**Related Use Case**: UC-7 (List All Tasks)"

echo -e "${GREEN}✓ Created Story 6: Implement Task.get_all()${NC}"

# Story 7: Implement Task.update_status()
gh issue create \
  --title "Story 7: Implement Task.update_status()" \
  --label "guided,intermediate,crud" \
  --body "**Difficulty**: Intermediate  
**Estimated Time**: 1 hour  
**Dependencies**: Story 6

**User Story**:
As a user, I want to mark a task as in progress or completed, so that I can track my progress.

**Acceptance Criteria**:
- [ ] Can change status to any valid value
- [ ] System validates status values
- [ ] Returns True if task was updated
- [ ] Returns False if task doesn't exist
- [ ] Raises ValidationError for invalid status
- [ ] Function is tested and working

**Learning Objectives**:
- UPDATE operations
- Validation before updates
- Checking affected rows
- Boolean return values
- Error handling

**Implementation Notes**:
- Complete \`Task.update_status()\` in \`models/todo.py\`
- Validate status before executing query
- Use \`execute_update()\` and check affected rows
- Study \`Book.update()\` for the pattern
- Test with existing and non-existing task IDs

**Related Use Case**: UC-8 (Update Task Status)"

echo -e "${GREEN}✓ Created Story 7: Implement Task.update_status()${NC}"

# Story 8: Implement Task.delete()
gh issue create \
  --title "Story 8: Implement Task.delete()" \
  --label "guided,intermediate,crud" \
  --body "**Difficulty**: Intermediate  
**Estimated Time**: 45 minutes  
**Dependencies**: Story 7

**User Story**:
As a user, I want to delete a task I no longer need, so that my task list stays clean.

**Acceptance Criteria**:
- [ ] Task is permanently removed from database
- [ ] Returns True if task was deleted
- [ ] Returns False if task doesn't exist
- [ ] Does not affect other tasks
- [ ] Function is tested and working

**Learning Objectives**:
- DELETE operations
- WHERE clauses (critical!)
- Checking affected rows
- Safe deletion patterns

**Implementation Notes**:
- Complete \`Task.delete()\` in \`models/todo.py\`
- ALWAYS include WHERE clause in DELETE
- Study \`Book.delete()\` - it's almost identical
- Use \`execute_update()\` and check affected rows
- Test with existing and non-existing task IDs

**Related Use Case**: UC-9 (Delete a Task)"

echo -e "${GREEN}✓ Created Story 8: Implement Task.delete()${NC}"

# Story 9: Implement Category System
gh issue create \
  --title "Story 9: Implement Category System (Optional)" \
  --label "guided,advanced,relationships" \
  --body "**Difficulty**: Advanced  
**Estimated Time**: 3 hours  
**Dependencies**: Story 8

**User Story**:
As a user, I want to assign tasks to categories, so that I can organize related tasks together.

**Acceptance Criteria**:
- [ ] Can create categories with unique names
- [ ] Can assign a task to a category
- [ ] Can list tasks by category
- [ ] Can list all categories
- [ ] Foreign key relationship works correctly
- [ ] All CRUD operations implemented
- [ ] Functions are tested and working

**Learning Objectives**:
- Foreign keys
- One-to-many relationships
- Schema design
- Complete model implementation
- JOIN operations

**Implementation Notes**:
- First, update \`database/schemas/todo_schema.sql\` to add categories table
- Add \`category_id\` field to tasks table
- Implement Category class in \`models/todo.py\`
- Follow the pattern from Member and Loan classes
- Test relationships work correctly

**Related Use Case**: UC-10 (Organize Tasks by Category)"

echo -e "${GREEN}✓ Created Story 9: Implement Category System${NC}"

# Story 10: Design Inventory Schema
gh issue create \
  --title "Story 10: Design Inventory Schema" \
  --label "challenge,advanced,design" \
  --body "**Difficulty**: Advanced  
**Estimated Time**: 2 hours  
**Dependencies**: Story 9

**User Story**:
As a student, I want to design a complete database schema for an inventory system, so that I can practice database design independently.

**Acceptance Criteria**:
- [ ] Products table with all required fields
- [ ] Categories table with appropriate structure
- [ ] Suppliers table with contact information
- [ ] Product-Category junction table (many-to-many)
- [ ] Foreign key relationships defined
- [ ] Appropriate constraints (NOT NULL, UNIQUE, CHECK)
- [ ] Schema is valid SQL and executes without errors

**Learning Objectives**:
- Database schema design
- Many-to-many relationships
- Junction tables
- Constraints and data types
- Independent design decisions

**Implementation Notes**:
- Edit \`database/schemas/inventory_schema.sql\`
- Study the library schema for patterns
- Consider what fields each table needs
- Think about relationships between entities
- Test schema by running \`python setup.py --force\`

**Related Use Cases**: UC-11 through UC-15 (all Inventory use cases)"

echo -e "${GREEN}✓ Created Story 10: Design Inventory Schema${NC}"

# Story 11: Implement Product CRUD Operations
gh issue create \
  --title "Story 11: Implement Product CRUD Operations" \
  --label "challenge,advanced,crud" \
  --body "**Difficulty**: Advanced  
**Estimated Time**: 4 hours  
**Dependencies**: Story 10

**User Story**:
As a store manager, I want to manage products in the inventory system, so that I can track what's in stock.

**Acceptance Criteria**:
- [ ] \`Product.create()\` - adds new products with validation
- [ ] \`Product.get_by_id()\` - retrieves product by ID
- [ ] \`Product.get_all()\` - lists all products with optional filters
- [ ] \`Product.update()\` - updates product fields
- [ ] \`Product.delete()\` - removes products
- [ ] All validation works correctly
- [ ] All functions tested and working

**Learning Objectives**:
- Complete CRUD implementation
- Complex validation (price, stock)
- Independent problem-solving
- Applying learned patterns

**Implementation Notes**:
- Implement methods in \`models/inventory.py\`
- Follow patterns from Book and Task models
- Validate price is positive
- Validate stock is non-negative
- Handle foreign key relationships

**Related Use Case**: UC-11 (Add a Product)"

echo -e "${GREEN}✓ Created Story 11: Implement Product CRUD Operations${NC}"

# Story 12: Implement Stock Management
gh issue create \
  --title "Story 12: Implement Stock Management" \
  --label "challenge,advanced,business-logic" \
  --body "**Difficulty**: Advanced  
**Estimated Time**: 2 hours  
**Dependencies**: Story 11

**User Story**:
As a store manager, I want to update product stock quantities, so that inventory reflects current levels.

**Acceptance Criteria**:
- [ ] \`Product.update_stock()\` - adjusts stock quantity
- [ ] Can increase or decrease stock
- [ ] Stock cannot go negative
- [ ] Returns error if stock would go negative
- [ ] Function is tested with various scenarios

**Learning Objectives**:
- Business logic implementation
- Constraint enforcement
- Edge case handling
- Transaction safety

**Implementation Notes**:
- Implement \`Product.update_stock()\` in \`models/inventory.py\`
- Check current stock before updating
- Prevent negative stock quantities
- Consider using transactions
- Test edge cases (stock = 0, large decreases)

**Related Use Case**: UC-12 (Update Stock Levels)"

echo -e "${GREEN}✓ Created Story 12: Implement Stock Management${NC}"

# Story 13: Implement Category and Supplier Models
gh issue create \
  --title "Story 13: Implement Category and Supplier Models" \
  --label "challenge,advanced,crud" \
  --body "**Difficulty**: Advanced  
**Estimated Time**: 3 hours  
**Dependencies**: Story 11

**User Story**:
As a store manager, I want to manage categories and suppliers, so that I can organize products and track suppliers.

**Acceptance Criteria**:
- [ ] Category class with full CRUD operations
- [ ] Supplier class with full CRUD operations
- [ ] \`Category.get_products()\` - lists products in category
- [ ] \`Supplier.get_products()\` - lists products from supplier
- [ ] All functions tested and working

**Learning Objectives**:
- Multiple model implementation
- One-to-many relationships
- JOIN queries
- Independent implementation

**Implementation Notes**:
- Implement Category and Supplier classes in \`models/inventory.py\`
- Follow patterns from Member and Loan classes
- Implement JOIN queries for getting related products
- Test relationships work correctly

**Related Use Cases**: UC-13 (Search by Category), UC-14 (Find by Supplier)"

echo -e "${GREEN}✓ Created Story 13: Implement Category and Supplier Models${NC}"

# Story 14: Implement Many-to-Many Relationships
gh issue create \
  --title "Story 14: Implement Many-to-Many Relationships" \
  --label "challenge,advanced,relationships" \
  --body "**Difficulty**: Advanced  
**Estimated Time**: 2 hours  
**Dependencies**: Story 13

**User Story**:
As a store manager, I want products to belong to multiple categories, so that I can organize inventory flexibly.

**Acceptance Criteria**:
- [ ] \`Product.add_category()\` - links product to category
- [ ] \`Product.remove_category()\` - unlinks product from category
- [ ] \`Product.get_categories()\` - lists all categories for a product
- [ ] Junction table is used correctly
- [ ] All functions tested and working

**Learning Objectives**:
- Many-to-many relationships
- Junction tables
- Complex JOIN queries
- Relationship management

**Implementation Notes**:
- Implement methods in Product class
- Use the product_categories junction table
- Study many-to-many patterns
- Test adding/removing multiple categories

**Related Use Case**: UC-13 (Search Products by Category)"

echo -e "${GREEN}✓ Created Story 14: Implement Many-to-Many Relationships${NC}"

# Story 15: Implement Low Stock Alerts
gh issue create \
  --title "Story 15: Implement Low Stock Alerts" \
  --label "challenge,advanced,queries" \
  --body "**Difficulty**: Advanced  
**Estimated Time**: 1.5 hours  
**Dependencies**: Story 12, Story 13

**User Story**:
As a store manager, I want to see products with low stock, so that I can reorder before running out.

**Acceptance Criteria**:
- [ ] \`Product.get_low_stock()\` - returns products below threshold
- [ ] Includes supplier information (JOIN)
- [ ] Sorted by stock level (lowest first)
- [ ] Threshold is configurable
- [ ] Function is tested and working

**Learning Objectives**:
- Complex queries
- JOIN operations
- Business logic
- Sorting and filtering

**Implementation Notes**:
- Implement \`Product.get_low_stock()\` in \`models/inventory.py\`
- Use JOIN to include supplier information
- Filter with WHERE stock_quantity < threshold
- Sort by stock_quantity ASC
- Test with various thresholds

**Related Use Case**: UC-15 (Low Stock Alert)"

echo -e "${GREEN}✓ Created Story 15: Implement Low Stock Alerts${NC}"

echo ""
echo -e "${BLUE}=== Bonus Stories ===${NC}"
echo ""

# Story 16: Add Due Dates to Tasks
gh issue create \
  --title "Story 16: Add Due Dates to Tasks (Bonus)" \
  --label "bonus,intermediate" \
  --body "**Difficulty**: Intermediate  
**Estimated Time**: 2 hours  
**Dependencies**: Story 8

**User Story**:
As a user, I want to set due dates for tasks, so that I can track deadlines.

**Acceptance Criteria**:
- [ ] Add \`due_date\` field to tasks table
- [ ] Implement \`Task.set_due_date()\`
- [ ] Implement \`Task.get_overdue()\` - returns overdue tasks
- [ ] Implement \`Task.get_due_soon()\` - returns tasks due within X days
- [ ] Validate due dates are not in the past

**Learning Objectives**:
- Date/time handling
- Date-based queries
- Schema modifications"

echo -e "${GREEN}✓ Created Story 16: Add Due Dates to Tasks${NC}"

# Story 17: Create CLI Interface
gh issue create \
  --title "Story 17: Create CLI Interface (Bonus)" \
  --label "bonus,intermediate,interface" \
  --body "**Difficulty**: Intermediate  
**Estimated Time**: 3 hours  
**Dependencies**: Story 8

**User Story**:
As a user, I want a command-line interface for the Todo system, so that I can manage tasks from the terminal.

**Acceptance Criteria**:
- [ ] CLI supports all CRUD operations
- [ ] Uses argparse for command parsing
- [ ] Provides helpful error messages
- [ ] Includes help text for all commands
- [ ] Tested with various commands

**Learning Objectives**:
- CLI development
- argparse module
- User interface design
- Error handling in interfaces"

echo -e "${GREEN}✓ Created Story 17: Create CLI Interface${NC}"

# Story 18: Create REST API
gh issue create \
  --title "Story 18: Create REST API (Bonus)" \
  --label "bonus,advanced,api" \
  --body "**Difficulty**: Advanced  
**Estimated Time**: 4 hours  
**Dependencies**: Story 8

**User Story**:
As a developer, I want a REST API for the Todo system, so that I can integrate it with other applications.

**Acceptance Criteria**:
- [ ] Flask API with all CRUD endpoints
- [ ] JSON request/response handling
- [ ] Proper HTTP status codes
- [ ] Error handling and validation
- [ ] API documentation

**Learning Objectives**:
- REST API design
- Flask framework
- HTTP methods and status codes
- JSON handling
- API best practices"

echo -e "${GREEN}✓ Created Story 18: Create REST API${NC}"

echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo -e "${GREEN}✓ Successfully created 18 GitHub issues!${NC}"
echo ""
echo "View your issues at: https://github.com/${REPO}/issues"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Create a GitHub Project board"
echo "2. Add these issues to your project"
echo "3. Organize them into columns (To Study, To Do, In Progress, Done)"
echo "4. Start with Story 1!"
echo ""
