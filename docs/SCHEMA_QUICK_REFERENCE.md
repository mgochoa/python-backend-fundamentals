# Database Schema Quick Reference

Quick visual reference for all database schemas in the project.

## 📚 Library System (Reference)

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│     BOOKS       │         │      LOANS       │         │    MEMBERS      │
├─────────────────┤         ├──────────────────┤         ├─────────────────┤
│ id (PK)         │◄────────│ book_id (FK)     │         │ id (PK)         │
│ title           │         │ member_id (FK)   │────────►│ name            │
│ author          │         │ loan_date        │         │ email (UNIQUE)  │
│ isbn (UNIQUE)   │         │ due_date         │         │ join_date       │
│ published_year  │         │ return_date      │         └─────────────────┘
│ available       │         └──────────────────┘
│ created_at      │
└─────────────────┘

Relationships:
• One book → many loans (over time)
• One member → many loans
• Loan tracks: who borrowed what, when, and if returned
```

## ✅ Todo System (Guided)

```
┌─────────────────┐         ┌──────────────────┐
│   CATEGORIES    │         │      TASKS       │
├─────────────────┤         ├──────────────────┤
│ id (PK)         │◄────────│ id (PK)          │
│ name (UNIQUE)   │         │ title            │
│ created_at      │         │ description      │
└─────────────────┘         │ status           │
                            │ priority         │
                            │ due_date         │
                            │ category_id (FK) │
                            │ created_at       │
                            └──────────────────┘

Relationships:
• One category → many tasks
• Task can exist without category (optional FK)

Status: pending | in_progress | completed
Priority: low | medium | high
```

## 📦 Inventory System (Challenge)

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   SUPPLIERS     │         │    PRODUCTS      │         │   CATEGORIES    │
├─────────────────┤         ├──────────────────┤         ├─────────────────┤
│ id (PK)         │◄────────│ id (PK)          │         │ id (PK)         │
│ name (UNIQUE)   │         │ name             │         │ name (UNIQUE)   │
│ contact_email   │         │ description      │         │ description     │
│ contact_phone   │         │ price            │         │ created_at      │
│ created_at      │         │ stock_quantity   │         └─────────────────┘
└─────────────────┘         │ supplier_id (FK) │                 ▲
                            │ created_at       │                 │
                            └──────────────────┘                 │
                                     │                           │
                                     │                           │
                                     ▼                           │
                            ┌──────────────────┐                 │
                            │PRODUCT_CATEGORIES│                 │
                            ├──────────────────┤                 │
                            │ product_id (FK)  │─────────────────┘
                            │ category_id (FK) │
                            └──────────────────┘
                            (Junction Table)

Relationships:
• One supplier → many products
• Many products ↔ many categories (via junction table)
• Product can exist without supplier (optional FK)
```

## 🔑 Key Concepts

### Primary Keys (PK)
```
id INTEGER PRIMARY KEY AUTOINCREMENT
```
- Uniquely identifies each record
- Auto-increments (1, 2, 3, ...)
- Every table should have one

### Foreign Keys (FK)
```
book_id INTEGER NOT NULL,
FOREIGN KEY (book_id) REFERENCES books(id)
```
- Links to another table's primary key
- Creates relationships between tables
- Ensures referential integrity

### Unique Constraints
```
isbn TEXT UNIQUE NOT NULL
email TEXT UNIQUE NOT NULL
```
- Prevents duplicate values
- Use for: ISBN, email, username, SKU

### Default Values
```
status TEXT NOT NULL DEFAULT 'pending'
available INTEGER DEFAULT 1
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```
- Automatically set if not provided
- Use for: status, flags, timestamps

### NULL vs NOT NULL
```
title TEXT NOT NULL          -- Required field
description TEXT             -- Optional field (NULL allowed)
```
- NOT NULL: Field must have a value
- NULL allowed: Field is optional

## 📊 Relationship Types

### One-to-Many (1:N)
```
One book → many loans
One member → many loans
One category → many tasks
One supplier → many products
```
Implementation: Foreign key in the "many" table

### Many-to-Many (M:N)
```
Many products ↔ many categories
```
Implementation: Junction table with two foreign keys
```sql
CREATE TABLE product_categories (
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    PRIMARY KEY (product_id, category_id)
);
```

## 🎯 Common Patterns

### Status Tracking
```sql
-- Track state with status field
status TEXT NOT NULL DEFAULT 'pending'

-- Track completion with timestamp
return_date DATE  -- NULL = not returned, DATE = returned
```

### Timestamps
```sql
-- When created
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

-- When updated (requires trigger or app logic)
updated_at TIMESTAMP

-- When completed
completed_at TIMESTAMP
```

### Optional Relationships
```sql
-- Can be NULL (optional)
category_id INTEGER,
supplier_id INTEGER,

-- Must have value (required)
book_id INTEGER NOT NULL,
member_id INTEGER NOT NULL,
```

## 🔍 Quick Queries

### Get all with relationship
```sql
-- Library: Books with their loans
SELECT b.title, l.loan_date, m.name
FROM books b
LEFT JOIN loans l ON b.id = l.book_id
LEFT JOIN members m ON l.member_id = m.id;

-- Todo: Tasks with categories
SELECT t.title, c.name as category
FROM tasks t
LEFT JOIN categories c ON t.category_id = c.id;

-- Inventory: Products with suppliers
SELECT p.name, s.name as supplier
FROM products p
LEFT JOIN suppliers s ON p.supplier_id = s.id;
```

### Filter by status
```sql
-- Active loans (not returned)
SELECT * FROM loans WHERE return_date IS NULL;

-- Pending tasks
SELECT * FROM tasks WHERE status = 'pending';

-- Low stock products
SELECT * FROM products WHERE stock_quantity < 10;
```

### Many-to-many queries
```sql
-- Products in a category
SELECT p.name
FROM products p
JOIN product_categories pc ON p.id = pc.product_id
JOIN categories c ON pc.category_id = c.id
WHERE c.name = 'Electronics';

-- All categories for a product
SELECT c.name
FROM categories c
JOIN product_categories pc ON c.id = pc.category_id
WHERE pc.product_id = 1;
```

## 📝 Design Checklist

When designing a new table:

- [ ] Primary key (id INTEGER PRIMARY KEY AUTOINCREMENT)
- [ ] Required fields (NOT NULL)
- [ ] Unique constraints (UNIQUE)
- [ ] Default values (DEFAULT)
- [ ] Foreign keys (FOREIGN KEY)
- [ ] Timestamps (created_at)
- [ ] Appropriate data types (INTEGER, TEXT, DATE, TIMESTAMP)

When designing relationships:

- [ ] Identify relationship type (1:Many or Many:Many)
- [ ] Add foreign key(s) in appropriate table(s)
- [ ] Create junction table if Many:Many
- [ ] Decide if relationship is optional or required
- [ ] Add appropriate constraints

## 🚀 Next Steps

1. **Study**: Review `docs/DATABASE_SCHEMAS.md` for detailed diagrams
2. **Explore**: Open schemas in `database/schemas/`
3. **Practice**: Complete TODOs in `database/schemas/todo_schema.sql`
4. **Challenge**: Design inventory schema from scratch
5. **Implement**: Create model classes in `models/`

---

**See Also**:
- [DATABASE_SCHEMAS.md](DATABASE_SCHEMAS.md) - Detailed ER diagrams and examples
- [CONCEPTS.md](../CONCEPTS.md) - Database fundamentals
- [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Command reference


---

## 🔗 Navigation

**You are here**: docs/SCHEMA_QUICK_REFERENCE.md (Quick lookup)

**Detailed Diagrams**: [Database Schemas](DATABASE_SCHEMAS.md)

**While Coding**:
- 📋 [Workflow](../WORKFLOW.md) - Step-by-step guide
- ⚡ [Quick Reference](../QUICK_REFERENCE.md) - Commands
- 🧪 Test: `python test_my_code.py`
- 🎮 Playground: `python playground.py`

**Learning**:
- 📖 [Concepts](../CONCEPTS.md) - Database fundamentals
- 📋 [Exercises](../exercises/EXERCISES.md) - Detailed guides
- 🔧 [Troubleshooting](../TROUBLESHOOTING.md) - Get help

**Back to Start**:
- 👋 [Start Here](../START_HERE.md)
- 📖 [README](../README.md)
