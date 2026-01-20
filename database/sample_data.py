"""
Sample Data Script for Library System

This script populates the database with example data to demonstrate
the Library System in action. It creates:
- A collection of books across different genres
- Several library members
- Active and completed loan records

Students can run this script to:
1. See the system working with realistic data
2. Test queries and operations on populated tables
3. Understand relationships between books, members, and loans
4. Have data to experiment with without creating it manually

Usage:
    python database/sample_data.py

The script will:
- Clear existing data (if any)
- Create sample books, members, and loans
- Display a summary of what was created
- Show examples of active loans and borrowing history

Learning Objectives:
- See how to use the model classes to create data
- Understand relationships between entities
- Learn about realistic test data for development
- Practice querying populated tables
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.library import Book, Member, Loan
from database.connection import get_connection


def clear_existing_data():
    """
    Clear all existing data from the database.
    
    This ensures we start with a clean slate when running the script.
    In a production system, you'd never do this! But for learning
    and testing, it's useful to reset to a known state.
    
    Note: We delete in reverse order of dependencies:
    1. First loans (depends on books and members)
    2. Then members and books (no dependencies)
    """
    print("🗑️  Clearing existing data...")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Delete in order: loans first (has foreign keys), then members and books
        cursor.execute("DELETE FROM loans")
        cursor.execute("DELETE FROM members")
        cursor.execute("DELETE FROM books")
        conn.commit()
        print("   ✓ Existing data cleared")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not clear data: {e}")
        conn.rollback()
    finally:
        conn.close()


def create_sample_books():
    """
    Create a diverse collection of sample books.
    
    This demonstrates:
    - Creating multiple records efficiently
    - Using realistic data (real book titles and ISBNs)
    - Covering different genres and publication years
    - Handling optional fields (some books have publication year, some don't)
    
    Returns:
        dict: Mapping of book names to their IDs for later reference
    """
    print("\n📚 Creating sample books...")
    
    # Define sample books with realistic data
    # Format: (title, author, isbn, published_year)
    sample_books = [
        # Programming & Technology
        ("Python Crash Course", "Eric Matthes", "978-1593279288", 2019),
        ("Clean Code", "Robert C. Martin", "978-0132350884", 2008),
        ("The Pragmatic Programmer", "David Thomas", "978-0135957059", 2019),
        ("Introduction to Algorithms", "Thomas H. Cormen", "978-0262033848", 2009),
        
        # Science & Mathematics
        ("A Brief History of Time", "Stephen Hawking", "978-0553380163", 1988),
        ("The Selfish Gene", "Richard Dawkins", "978-0198788607", 1976),
        ("Cosmos", "Carl Sagan", "978-0345539434", 1980),
        
        # Fiction
        ("1984", "George Orwell", "978-0451524935", 1949),
        ("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 1960),
        ("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", 1925),
        ("Pride and Prejudice", "Jane Austen", "978-0141439518", 1813),
        
        # Non-Fiction
        ("Sapiens", "Yuval Noah Harari", "978-0062316097", 2015),
        ("Educated", "Tara Westover", "978-0399590504", 2018),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "978-0374533557", 2011),
        
        # Business & Self-Help
        ("Atomic Habits", "James Clear", "978-0735211292", 2018),
        ("The 7 Habits of Highly Effective People", "Stephen Covey", "978-1982137274", 1989),
    ]
    
    book_ids = {}
    
    for title, author, isbn, year in sample_books:
        try:
            book_id = Book.create(
                title=title,
                author=author,
                isbn=isbn,
                published_year=year
            )
            book_ids[title] = book_id
            print(f"   ✓ Created: {title} by {author}")
        except Exception as e:
            print(f"   ✗ Failed to create '{title}': {e}")
    
    print(f"\n   📊 Total books created: {len(book_ids)}")
    return book_ids


def create_sample_members():
    """
    Create sample library members.
    
    This demonstrates:
    - Creating member records with unique emails
    - Using realistic names and email formats
    - Building a diverse member base
    
    Returns:
        dict: Mapping of member names to their IDs for later reference
    """
    print("\n👥 Creating sample members...")
    
    # Define sample members
    # Format: (name, email)
    sample_members = [
        ("Alice Johnson", "alice.johnson@email.com"),
        ("Bob Smith", "bob.smith@email.com"),
        ("Carol Williams", "carol.williams@email.com"),
        ("David Brown", "david.brown@email.com"),
        ("Emma Davis", "emma.davis@email.com"),
        ("Frank Miller", "frank.miller@email.com"),
        ("Grace Wilson", "grace.wilson@email.com"),
        ("Henry Taylor", "henry.taylor@email.com"),
    ]
    
    member_ids = {}
    
    for name, email in sample_members:
        try:
            member_id = Member.create(name=name, email=email)
            member_ids[name] = member_id
            print(f"   ✓ Created member: {name} ({email})")
        except Exception as e:
            print(f"   ✗ Failed to create member '{name}': {e}")
    
    print(f"\n   📊 Total members created: {len(member_ids)}")
    return member_ids


def create_sample_loans(book_ids, member_ids):
    """
    Create sample loan records showing both active and completed loans.
    
    This demonstrates:
    - Creating loan records with relationships
    - Setting realistic loan and due dates
    - Showing both active loans (not returned) and completed loans (returned)
    - Using direct SQL inserts to create historical data
    
    Note: We use direct SQL inserts here instead of Loan.create() because
    Loan.create() only creates loans with today's date. For educational
    purposes, we want to show historical data with various dates.
    
    Args:
        book_ids: Dictionary mapping book titles to IDs
        member_ids: Dictionary mapping member names to IDs
    
    Returns:
        tuple: (active_loan_count, completed_loan_count)
    """
    print("\n📖 Creating sample loans...")
    
    # Define sample loans
    # Format: (book_title, member_name, days_ago_borrowed, days_until_due, returned)
    # - days_ago_borrowed: how many days ago the book was borrowed
    # - days_until_due: how many days from borrow date until due
    # - returned: True if book has been returned, False if still checked out
    
    sample_loans = [
        # Active loans (not yet returned)
        ("Python Crash Course", "Alice Johnson", 5, 14, False),
        ("Clean Code", "Bob Smith", 3, 14, False),
        ("1984", "Carol Williams", 7, 21, False),
        ("Sapiens", "David Brown", 2, 14, False),
        ("Atomic Habits", "Emma Davis", 10, 14, False),
        
        # Completed loans (returned)
        ("The Great Gatsby", "Alice Johnson", 30, 14, True),
        ("To Kill a Mockingbird", "Bob Smith", 45, 21, True),
        ("A Brief History of Time", "Frank Miller", 60, 14, True),
        ("The Pragmatic Programmer", "Grace Wilson", 25, 14, True),
        ("Thinking, Fast and Slow", "Henry Taylor", 40, 21, True),
        
        # Overdue loan (borrowed 20 days ago, due in 14 days = 6 days overdue)
        ("Cosmos", "Carol Williams", 20, 14, False),
    ]
    
    active_count = 0
    completed_count = 0
    overdue_count = 0
    
    # Get database connection for direct inserts
    conn = get_connection()
    cursor = conn.cursor()
    
    for book_title, member_name, days_ago, days_due, is_returned in sample_loans:
        try:
            # Get the book and member IDs
            book_id = book_ids.get(book_title)
            member_id = member_ids.get(member_name)
            
            if not book_id or not member_id:
                print(f"   ⚠️  Skipping loan: Book or member not found")
                continue
            
            # Calculate dates
            loan_date = datetime.now().date() - timedelta(days=days_ago)
            due_date = loan_date + timedelta(days=days_due)
            return_date = None
            
            if is_returned:
                # Book was returned a few days after borrowing (before due date)
                return_date = loan_date + timedelta(days=days_due - 2)
            
            # Insert loan directly into database
            # We use direct SQL here to set historical dates
            # In production code, you'd use Loan.create() for current loans
            query = """
                INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                book_id,
                member_id,
                loan_date.isoformat(),
                due_date.isoformat(),
                return_date.isoformat() if return_date else None
            ))
            
            # Update book availability if loan is active (not returned)
            if not is_returned:
                cursor.execute(
                    "UPDATE books SET available = 0 WHERE id = ?",
                    (book_id,)
                )
            
            # Determine loan status
            if is_returned:
                status = "✓ Returned"
                completed_count += 1
            elif datetime.now().date() > due_date:
                status = "⚠️  OVERDUE"
                overdue_count += 1
                active_count += 1
            else:
                status = "📖 Active"
                active_count += 1
            
            print(f"   {status}: '{book_title}' borrowed by {member_name}")
            
        except Exception as e:
            print(f"   ✗ Failed to create loan: {e}")
            conn.rollback()
    
    # Commit all loan records
    conn.commit()
    conn.close()
    
    print(f"\n   📊 Loan Summary:")
    print(f"      - Active loans: {active_count}")
    print(f"      - Completed loans: {completed_count}")
    print(f"      - Overdue loans: {overdue_count}")
    
    return active_count, completed_count


def display_summary(book_ids, member_ids, active_loans, completed_loans):
    """
    Display a summary of the created data and some example queries.
    
    This shows students:
    - What data was created
    - How to query the data
    - Examples of useful queries they can try
    """
    print("\n" + "="*70)
    print("📊 SAMPLE DATA SUMMARY")
    print("="*70)
    
    print(f"\n✓ Database populated successfully!")
    print(f"\n  📚 Books: {len(book_ids)}")
    print(f"  👥 Members: {len(member_ids)}")
    print(f"  📖 Active Loans: {active_loans}")
    print(f"  ✓ Completed Loans: {completed_loans}")
    
    print("\n" + "="*70)
    print("🔍 EXAMPLE QUERIES TO TRY")
    print("="*70)
    
    print("\n1. View all books:")
    print("   >>> from models.library import Book")
    print("   >>> books = Book.get_all()")
    print("   >>> for book in books:")
    print("   ...     print(f\"{book['title']} by {book['author']}\")")
    
    print("\n2. Search for books:")
    print("   >>> results = Book.search('Python', 'title')")
    print("   >>> print(f\"Found {len(results)} books\")")
    
    print("\n3. View available books only:")
    print("   >>> available = Book.get_all(available_only=True)")
    print("   >>> print(f\"{len(available)} books available\")")
    
    print("\n4. View all members:")
    print("   >>> from models.library import Member")
    print("   >>> members = Member.get_all()")
    print("   >>> for member in members:")
    print("   ...     print(f\"{member['name']} - {member['email']}\")")
    
    print("\n5. View active loans:")
    print("   >>> from models.library import Loan")
    print("   >>> active = Loan.get_active_loans()")
    print("   >>> for loan in active:")
    print("   ...     print(f\"Book ID {loan['book_id']} due on {loan['due_date']}\")")
    
    print("\n6. View a member's borrowing history:")
    print("   >>> history = Loan.get_by_member(1)  # Member ID 1")
    print("   >>> print(f\"Member has {len(history)} loans\")")
    
    print("\n7. Check for overdue loans:")
    print("   >>> overdue = Loan.get_overdue_loans()")
    print("   >>> print(f\"{len(overdue)} overdue loans\")")
    
    print("\n" + "="*70)
    print("💡 NEXT STEPS")
    print("="*70)
    
    print("\n1. Open a Python interactive shell:")
    print("   $ python")
    
    print("\n2. Try the example queries above")
    
    print("\n3. Experiment with creating your own data:")
    print("   >>> from models.library import Book")
    print("   >>> book_id = Book.create('My Book', 'My Name', '1234567890')")
    
    print("\n4. Practice updating and deleting records:")
    print("   >>> Book.update(book_id, title='Updated Title')")
    print("   >>> Book.delete(book_id)")
    
    print("\n5. Study the model code in models/library.py to understand")
    print("   how these operations work")
    
    print("\n6. Move on to the Todo System exercises to implement")
    print("   similar functionality yourself!")
    
    print("\n" + "="*70 + "\n")


def main():
    """
    Main function to populate the database with sample data.
    
    This orchestrates the entire process:
    1. Clear existing data
    2. Create books
    3. Create members
    4. Create loans
    5. Display summary
    """
    print("="*70)
    print("🎓 LIBRARY SYSTEM - SAMPLE DATA SCRIPT")
    print("="*70)
    print("\nThis script will populate the database with example data")
    print("for the Library System, including books, members, and loans.")
    print("\nNote: This will clear any existing data in the database!")
    print("="*70)
    
    try:
        # Step 1: Clear existing data
        clear_existing_data()
        
        # Step 2: Create sample books
        book_ids = create_sample_books()
        
        # Step 3: Create sample members
        member_ids = create_sample_members()
        
        # Step 4: Create sample loans
        active_loans, completed_loans = create_sample_loans(book_ids, member_ids)
        
        # Step 5: Display summary and examples
        display_summary(book_ids, member_ids, active_loans, completed_loans)
        
        print("✅ Sample data created successfully!")
        print("\nYou can now explore the data using the example queries above.")
        print("Or run: python main.py")
        
    except Exception as e:
        print(f"\n❌ Error creating sample data: {e}")
        print("\nMake sure you have:")
        print("1. Run setup.py to initialize the database")
        print("2. All required modules are available")
        print("3. The database file is not locked by another process")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
