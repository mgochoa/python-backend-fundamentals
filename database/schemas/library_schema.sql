-- ============================================================================
-- Library System Database Schema
-- ============================================================================
-- This schema demonstrates a complete database design for a library management
-- system. It includes three related tables with proper constraints and
-- relationships. Study this schema to understand:
--   - How to define tables with appropriate data types
--   - How to use constraints to enforce data integrity
--   - How to create relationships between tables using foreign keys
--   - How to set default values for fields
-- ============================================================================

-- ============================================================================
-- BOOKS TABLE
-- ============================================================================
-- Stores information about books in the library collection.
-- This table demonstrates:
--   - PRIMARY KEY: Ensures each book has a unique identifier
--   - UNIQUE constraint: Prevents duplicate ISBNs
--   - NOT NULL constraints: Ensures required fields are always provided
--   - DEFAULT values: Automatically sets values when not specified
-- ============================================================================

CREATE TABLE IF NOT EXISTS books (
    -- Primary key: Uniquely identifies each book record
    -- AUTOINCREMENT ensures IDs are never reused, even after deletion
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Title of the book
    -- NOT NULL: Every book must have a title (required field)
    title TEXT NOT NULL,
    
    -- Author name
    -- NOT NULL: Every book must have an author (required field)
    author TEXT NOT NULL,
    
    -- International Standard Book Number
    -- UNIQUE: No two books can have the same ISBN (prevents duplicates)
    -- NOT NULL: ISBN is required for cataloging purposes
    isbn TEXT UNIQUE NOT NULL,
    
    -- Year the book was published
    -- Optional field (can be NULL if publication year is unknown)
    published_year INTEGER,
    
    -- Availability status: 1 (true) = available, 0 (false) = checked out
    -- DEFAULT 1: New books are available by default
    -- This is a simple boolean represented as INTEGER (SQLite doesn't have BOOLEAN type)
    available INTEGER DEFAULT 1,
    
    -- Timestamp when the book record was created
    -- DEFAULT CURRENT_TIMESTAMP: Automatically set to current date/time when record is created
    -- Useful for tracking when books were added to the system
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- MEMBERS TABLE
-- ============================================================================
-- Stores information about library members (patrons).
-- This table demonstrates:
--   - Email validation through UNIQUE constraint
--   - Date fields with automatic defaults
--   - How to store user/customer information
-- ============================================================================

CREATE TABLE IF NOT EXISTS members (
    -- Primary key: Uniquely identifies each member
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Member's full name
    -- NOT NULL: Every member must have a name
    name TEXT NOT NULL,
    
    -- Member's email address
    -- UNIQUE: Each email can only be registered once (prevents duplicate accounts)
    -- NOT NULL: Email is required for communication and account identification
    -- Note: For production systems, you'd also want to validate email format in application code
    email TEXT UNIQUE NOT NULL,
    
    -- Date when the member joined the library
    -- DEFAULT CURRENT_DATE: Automatically set to today's date when member signs up
    -- Uses DATE type (stores as 'YYYY-MM-DD' format in SQLite)
    join_date DATE DEFAULT CURRENT_DATE
);

-- ============================================================================
-- LOANS TABLE
-- ============================================================================
-- Tracks which books are borrowed by which members.
-- This table demonstrates:
--   - FOREIGN KEY constraints: Creates relationships between tables
--   - How to model many-to-many relationships (a book can be loaned many times,
--     a member can borrow many books)
--   - Using NULL values to track state (return_date is NULL until book is returned)
-- ============================================================================

CREATE TABLE IF NOT EXISTS loans (
    -- Primary key: Uniquely identifies each loan transaction
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Reference to the book being borrowed
    -- FOREIGN KEY: Links to books.id, ensuring the book exists
    -- NOT NULL: A loan must reference a specific book
    -- If a book is deleted, this constraint prevents orphaned loan records
    book_id INTEGER NOT NULL,
    
    -- Reference to the member borrowing the book
    -- FOREIGN KEY: Links to members.id, ensuring the member exists
    -- NOT NULL: A loan must reference a specific member
    member_id INTEGER NOT NULL,
    
    -- Date when the book was borrowed
    -- DEFAULT CURRENT_DATE: Automatically set to today when loan is created
    loan_date DATE DEFAULT CURRENT_DATE,
    
    -- Date when the book should be returned
    -- NOT NULL: Every loan must have a due date (typically 2-4 weeks from loan_date)
    -- This is set by application code, not automatically
    due_date DATE NOT NULL,
    
    -- Date when the book was actually returned
    -- NULL by default: NULL means book is still checked out
    -- When book is returned, this field is updated with the return date
    -- This allows us to track both active loans (return_date IS NULL) and
    -- completed loans (return_date IS NOT NULL)
    return_date DATE,
    
    -- Foreign key constraint for book_id
    -- ON DELETE RESTRICT would prevent deleting a book that has loan records
    -- (not specified here, so SQLite uses default behavior)
    FOREIGN KEY (book_id) REFERENCES books(id),
    
    -- Foreign key constraint for member_id
    -- Links this loan to a specific member in the members table
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- ============================================================================
-- INDEXES (Optional - for performance)
-- ============================================================================
-- Indexes speed up queries but are not strictly necessary for small databases.
-- Uncomment these if you want to learn about database optimization:

-- CREATE INDEX idx_books_isbn ON books(isbn);
-- CREATE INDEX idx_members_email ON members(email);
-- CREATE INDEX idx_loans_book_id ON loans(book_id);
-- CREATE INDEX idx_loans_member_id ON loans(member_id);
-- CREATE INDEX idx_loans_return_date ON loans(return_date);

-- ============================================================================
-- LEARNING NOTES
-- ============================================================================
-- Key Concepts Demonstrated:
--
-- 1. PRIMARY KEY: Ensures each row is uniquely identifiable
--    - Use AUTOINCREMENT to automatically generate sequential IDs
--
-- 2. NOT NULL: Enforces that a field must have a value
--    - Use for required fields that should never be empty
--
-- 3. UNIQUE: Ensures no duplicate values in a column
--    - Use for fields like ISBN, email that must be unique
--
-- 4. DEFAULT: Provides automatic values when not specified
--    - Useful for timestamps, boolean flags, status fields
--
-- 5. FOREIGN KEY: Creates relationships between tables
--    - Ensures referential integrity (can't reference non-existent records)
--    - Models real-world relationships (books borrowed by members)
--
-- 6. Data Types in SQLite:
--    - INTEGER: Whole numbers (IDs, years, boolean as 0/1)
--    - TEXT: Strings of any length (names, titles, emails)
--    - DATE: Dates in 'YYYY-MM-DD' format
--    - TIMESTAMP: Date and time in 'YYYY-MM-DD HH:MM:SS' format
--
-- 7. NULL vs NOT NULL:
--    - NULL means "no value" or "unknown"
--    - Use NULL for optional fields (published_year, return_date)
--    - Use NOT NULL for required fields (title, author, isbn)
--
-- 8. Naming Conventions:
--    - Tables: plural nouns (books, members, loans)
--    - Columns: lowercase with underscores (created_at, book_id)
--    - Foreign keys: singular_table_id (book_id, member_id)
--
-- ============================================================================
-- NEXT STEPS FOR LEARNING
-- ============================================================================
-- After studying this schema:
-- 1. Run setup.py to create the database with this schema
-- 2. Look at models/library.py to see how to interact with these tables
-- 3. Try writing SELECT queries to retrieve data from these tables
-- 4. Study the loans table to understand how relationships work
-- 5. Move on to the Todo System schema to practice creating your own tables
-- ============================================================================
