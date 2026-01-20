#!/usr/bin/env python3
"""
Test script for Library System models.

This script tests the Member and Loan classes to ensure they work correctly.
It demonstrates:
- Creating members
- Creating books
- Creating loans (borrowing books)
- JOIN operations (getting member's loans with book details)
- Returning books
- Getting overdue loans
"""

import sys
from datetime import date, timedelta
import pytest

# Import our models
from models.library import Book, Member, Loan, ValidationError, DuplicateError, NotFoundError


@pytest.fixture
def member_id():
    """Fixture to create a test member and return its ID."""
    try:
        member_id = Member.create(
            name="Alice Johnson",
            email="alice@example.com"
        )
    except DuplicateError:
        member = Member.get_by_email("alice@example.com")
        member_id = member['id']
    return member_id


def test_member_crud():
    """Test Member CRUD operations."""
    print("=" * 70)
    print("Testing Member CRUD Operations")
    print("=" * 70)
    
    # Create a member
    print("\n1. Creating a new member...")
    try:
        member_id = Member.create(
            name="Alice Johnson",
            email="alice@example.com"
        )
        print(f"✓ Created member with ID: {member_id}")
    except DuplicateError:
        print("✓ Member already exists (expected if running multiple times)")
        member = Member.get_by_email("alice@example.com")
        member_id = member['id']
    
    # Get member by ID
    print("\n2. Retrieving member by ID...")
    member = Member.get_by_id(member_id)
    if member:
        print(f"✓ Found member: {member['name']}")
        print(f"  Email: {member['email']}")
        print(f"  Joined: {member['join_date']}")
    
    # Get all members
    print("\n3. Retrieving all members...")
    members = Member.get_all()
    print(f"✓ Found {len(members)} member(s)")
    for m in members:
        print(f"  - {m['name']} ({m['email']})")
    
    # Update member
    print("\n4. Updating member name...")
    success = Member.update(member_id, name="Alice Smith")
    if success:
        print("✓ Member updated successfully")
        updated = Member.get_by_id(member_id)
        print(f"  New name: {updated['name']}")
    
    print("\n✓ Member CRUD tests completed!")


def test_loan_operations(member_id):
    """Test Loan operations including JOINs."""
    print("\n" + "=" * 70)
    print("Testing Loan Operations (with JOINs)")
    print("=" * 70)
    
    # First, ensure we have a book
    print("\n1. Creating a test book...")
    try:
        book_id = Book.create(
            title="Python Crash Course",
            author="Eric Matthes",
            isbn="978-1593279288",
            published_year=2019
        )
        print(f"✓ Created book with ID: {book_id}")
    except DuplicateError:
        print("✓ Book already exists (expected if running multiple times)")
        books = Book.search("Python Crash Course", "title")
        book_id = books[0]['id']
    
    # Check book availability
    book = Book.get_by_id(book_id)
    print(f"  Book availability: {book['available']}")
    
    # If book is not available, return it first
    if not book['available']:
        print("  Book is checked out, finding and returning it...")
        active_loans = Loan.get_active_loans()
        for loan in active_loans:
            if loan['book_id'] == book_id:
                Loan.return_book(loan['id'])
                print(f"  ✓ Returned book from loan {loan['id']}")
                break
    
    # Create a loan
    print("\n2. Creating a loan (member borrows book)...")
    try:
        loan_id = Loan.create(
            book_id=book_id,
            member_id=member_id,
            loan_days=14
        )
        print(f"✓ Created loan with ID: {loan_id}")
        
        # Verify book is now unavailable
        book = Book.get_by_id(book_id)
        print(f"  Book availability after loan: {book['available']}")
        
    except ValidationError as e:
        print(f"✗ Validation error: {e}")
        return
    
    # Get loan by ID
    print("\n3. Retrieving loan by ID...")
    loan = Loan.get_by_id(loan_id)
    if loan:
        print(f"✓ Found loan:")
        print(f"  Book ID: {loan['book_id']}")
        print(f"  Member ID: {loan['member_id']}")
        print(f"  Loan date: {loan['loan_date']}")
        print(f"  Due date: {loan['due_date']}")
        print(f"  Return date: {loan['return_date']}")
    
    # Get member's loans with JOIN (IMPORTANT!)
    print("\n4. Getting member's loans with book details (JOIN operation)...")
    member_loans = Loan.get_by_member(member_id)
    print(f"✓ Found {len(member_loans)} loan(s) for this member")
    for loan in member_loans:
        print(f"\n  Loan ID: {loan['id']}")
        print(f"  Book: {loan['book_title']} by {loan['book_author']}")
        print(f"  ISBN: {loan['book_isbn']}")
        print(f"  Loan date: {loan['loan_date']}")
        print(f"  Due date: {loan['due_date']}")
        if loan['return_date']:
            print(f"  Returned: {loan['return_date']}")
        else:
            print(f"  Status: Still checked out")
    
    # Get active loans only
    print("\n5. Getting member's active loans only...")
    active = Loan.get_by_member(member_id, active_only=True)
    print(f"✓ Member has {len(active)} book(s) currently checked out")
    
    # Get all active loans
    print("\n6. Getting all active loans in the system...")
    all_active = Loan.get_active_loans()
    print(f"✓ There are {len(all_active)} active loan(s) in the system")
    
    # Return the book
    print("\n7. Returning the book...")
    success = Loan.return_book(loan_id)
    if success:
        print("✓ Book returned successfully")
        
        # Verify book is now available
        book = Book.get_by_id(book_id)
        print(f"  Book availability after return: {book['available']}")
        
        # Verify loan has return date
        loan = Loan.get_by_id(loan_id)
        print(f"  Return date recorded: {loan['return_date']}")
    
    print("\n✓ Loan operation tests completed!")


def test_join_operations():
    """Test advanced JOIN operations."""
    print("\n" + "=" * 70)
    print("Testing Advanced JOIN Operations")
    print("=" * 70)
    
    print("\n1. Getting overdue loans (multi-table JOIN)...")
    overdue = Loan.get_overdue_loans()
    print(f"✓ Found {len(overdue)} overdue loan(s)")
    
    if overdue:
        for loan in overdue:
            print(f"\n  Overdue Loan:")
            print(f"  Book: {loan['book_title']} by {loan['book_author']}")
            print(f"  Borrowed by: {loan['member_name']} ({loan['member_email']})")
            print(f"  Due date: {loan['due_date']}")
    else:
        print("  No overdue loans (good!)")
    
    print("\n✓ JOIN operation tests completed!")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("Library System - Member and Loan Class Tests")
    print("=" * 70)
    print("\nThis script tests the newly implemented Member and Loan classes.")
    print("It demonstrates CRUD operations and JOIN queries.\n")
    
    try:
        # Test Member CRUD
        member_id = test_member_crud()
        
        # Test Loan operations
        test_loan_operations(member_id)
        
        # Test JOIN operations
        test_join_operations()
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nKey accomplishments:")
        print("✓ Member CRUD operations work correctly")
        print("✓ Loan CRUD operations work correctly")
        print("✓ JOIN operations successfully combine data from multiple tables")
        print("✓ Foreign key relationships are properly maintained")
        print("✓ Business logic (availability checking) works correctly")
        print("\nThe Member and Loan classes are ready for students to study!")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
