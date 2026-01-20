#!/usr/bin/env python3
"""
Flask REST API Example

This is an OPTIONAL advanced example showing how to build a REST API
for your backend using the Flask web framework.

LEARNING OBJECTIVES:
- Understand REST API concepts (GET, POST, PUT, DELETE)
- Build web APIs with Flask
- Handle JSON request/response data
- Implement proper HTTP status codes
- Handle errors in API endpoints

WHAT IS A REST API?
A REST API (Representational State Transfer API) allows applications to
communicate over HTTP using standard methods:
- GET: Retrieve data
- POST: Create new data
- PUT/PATCH: Update existing data
- DELETE: Remove data

APIs return data in JSON format, making them perfect for:
- Web applications (React, Vue, Angular)
- Mobile applications (iOS, Android)
- Other backend services
- Third-party integrations

PREREQUISITES:
You need to install Flask first:
    pip install flask

HOW TO USE THIS FILE:
1. Install Flask: pip install flask
2. Make sure you've run setup.py to initialize the database
3. Run the API server:
   python examples/api_example.py
4. The server will start on http://localhost:5000
5. Test the API using:
   - Web browser for GET requests
   - curl commands (see examples below)
   - Postman or similar API testing tool
6. Study the code to understand how it works
7. Complete the TODO sections to add Todo endpoints

EXAMPLE API REQUESTS:

# Get all books
curl http://localhost:5000/api/books

# Get a specific book
curl http://localhost:5000/api/books/1

# Create a new book
curl -X POST http://localhost:5000/api/books \\
  -H "Content-Type: application/json" \\
  -d '{"title":"Test Book","author":"Test Author","isbn":"1234567890"}'

# Update a book
curl -X PUT http://localhost:5000/api/books/1 \\
  -H "Content-Type: application/json" \\
  -d '{"published_year":2024}'

# Delete a book
curl -X DELETE http://localhost:5000/api/books/1

# Search books
curl "http://localhost:5000/api/books/search?query=Python&field=title"
"""

from flask import Flask, request, jsonify
from typing import Dict, Any
import sys

# Import Library System models
from models.library import Book, Member, Loan, ValidationError, DuplicateError, NotFoundError

# Import Todo System models
from models.todo import Task


# ============================================================================
# FLASK APP SETUP
# ============================================================================

app = Flask(__name__)

# Configure Flask
app.config['JSON_SORT_KEYS'] = False  # Preserve JSON key order
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Pretty-print JSON responses


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def success_response(data: Any, status_code: int = 200) -> tuple:
    """
    Create a successful JSON response.
    
    Args:
        data: Data to return (will be converted to JSON)
        status_code: HTTP status code (default 200 OK)
    
    Returns:
        Tuple of (response, status_code) for Flask
    """
    return jsonify({
        "success": True,
        "data": data
    }), status_code


def error_response(message: str, status_code: int = 400) -> tuple:
    """
    Create an error JSON response.
    
    Args:
        message: Error message
        status_code: HTTP status code (default 400 Bad Request)
    
    Returns:
        Tuple of (response, status_code) for Flask
    """
    return jsonify({
        "success": False,
        "error": message
    }), status_code


# ============================================================================
# LIBRARY SYSTEM API ENDPOINTS (Complete Examples)
# ============================================================================

# -----------------------------------------------------------------------------
# BOOK ENDPOINTS
# -----------------------------------------------------------------------------

@app.route('/api/books', methods=['GET'])
def get_books():
    """
    GET /api/books - Retrieve all books
    
    Query Parameters:
        available_only (bool): If true, only return available books
    
    Response:
        200 OK: List of books
        500 Internal Server Error: Database error
    
    Example:
        GET /api/books
        GET /api/books?available_only=true
    """
    try:
        # Get query parameter (defaults to False if not provided)
        available_only = request.args.get('available_only', 'false').lower() == 'true'
        
        # Get books from database
        books = Book.get_all(available_only=available_only)
        
        # Return success response
        return success_response(books)
        
    except Exception as e:
        return error_response(f"Failed to retrieve books: {str(e)}", 500)


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    """
    GET /api/books/<id> - Retrieve a specific book by ID
    
    Path Parameters:
        book_id (int): ID of the book to retrieve
    
    Response:
        200 OK: Book data
        404 Not Found: Book doesn't exist
        500 Internal Server Error: Database error
    
    Example:
        GET /api/books/1
    """
    try:
        book = Book.get_by_id(book_id)
        
        if book is None:
            return error_response(f"Book with ID {book_id} not found", 404)
        
        return success_response(book)
        
    except Exception as e:
        return error_response(f"Failed to retrieve book: {str(e)}", 500)


@app.route('/api/books', methods=['POST'])
def create_book():
    """
    POST /api/books - Create a new book
    
    Request Body (JSON):
        {
            "title": "Book Title",
            "author": "Author Name",
            "isbn": "1234567890",
            "published_year": 2024  // optional
        }
    
    Response:
        201 Created: Book created successfully with ID
        400 Bad Request: Validation error or missing fields
        409 Conflict: Duplicate ISBN
        500 Internal Server Error: Database error
    
    Example:
        POST /api/books
        Content-Type: application/json
        {"title":"Python Book","author":"John Doe","isbn":"1234567890"}
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return error_response("Request body must be JSON", 400)
        
        required_fields = ['title', 'author', 'isbn']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return error_response(f"Missing required fields: {', '.join(missing_fields)}", 400)
        
        # Create book
        book_id = Book.create(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            published_year=data.get('published_year')  # Optional field
        )
        
        # Return success response with 201 Created status
        return success_response({
            "id": book_id,
            "message": "Book created successfully"
        }, 201)
        
    except ValidationError as e:
        return error_response(str(e), 400)
    except DuplicateError as e:
        return error_response(str(e), 409)
    except Exception as e:
        return error_response(f"Failed to create book: {str(e)}", 500)


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id: int):
    """
    PUT /api/books/<id> - Update a book
    
    Path Parameters:
        book_id (int): ID of the book to update
    
    Request Body (JSON):
        {
            "title": "New Title",  // optional
            "author": "New Author",  // optional
            "published_year": 2024  // optional
        }
    
    Response:
        200 OK: Book updated successfully
        400 Bad Request: Validation error
        404 Not Found: Book doesn't exist
        500 Internal Server Error: Database error
    
    Example:
        PUT /api/books/1
        Content-Type: application/json
        {"published_year":2024}
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return error_response("Request body must be JSON", 400)
        
        # Update book with provided fields
        success = Book.update(book_id, **data)
        
        if not success:
            return error_response(f"Book with ID {book_id} not found", 404)
        
        return success_response({
            "id": book_id,
            "message": "Book updated successfully"
        })
        
    except ValidationError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Failed to update book: {str(e)}", 500)


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int):
    """
    DELETE /api/books/<id> - Delete a book
    
    Path Parameters:
        book_id (int): ID of the book to delete
    
    Response:
        200 OK: Book deleted successfully
        404 Not Found: Book doesn't exist
        500 Internal Server Error: Database error
    
    Example:
        DELETE /api/books/1
    """
    try:
        success = Book.delete(book_id)
        
        if not success:
            return error_response(f"Book with ID {book_id} not found", 404)
        
        return success_response({
            "id": book_id,
            "message": "Book deleted successfully"
        })
        
    except Exception as e:
        return error_response(f"Failed to delete book: {str(e)}", 500)


@app.route('/api/books/search', methods=['GET'])
def search_books():
    """
    GET /api/books/search - Search for books
    
    Query Parameters:
        query (str): Search term (required)
        field (str): Field to search in - 'title' or 'author' (default: 'title')
    
    Response:
        200 OK: List of matching books
        400 Bad Request: Missing query parameter
        500 Internal Server Error: Database error
    
    Example:
        GET /api/books/search?query=Python&field=title
    """
    try:
        # Get query parameters
        query = request.args.get('query')
        field = request.args.get('field', 'title')
        
        if not query:
            return error_response("Missing required parameter: query", 400)
        
        if field not in ['title', 'author']:
            return error_response("Field must be 'title' or 'author'", 400)
        
        # Search books
        books = Book.search(query, search_field=field)
        
        return success_response(books)
        
    except Exception as e:
        return error_response(f"Failed to search books: {str(e)}", 500)


# -----------------------------------------------------------------------------
# MEMBER ENDPOINTS
# -----------------------------------------------------------------------------

@app.route('/api/members', methods=['GET'])
def get_members():
    """GET /api/members - Retrieve all members"""
    try:
        members = Member.get_all()
        return success_response(members)
    except Exception as e:
        return error_response(f"Failed to retrieve members: {str(e)}", 500)


@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id: int):
    """GET /api/members/<id> - Retrieve a specific member"""
    try:
        member = Member.get_by_id(member_id)
        if member is None:
            return error_response(f"Member with ID {member_id} not found", 404)
        return success_response(member)
    except Exception as e:
        return error_response(f"Failed to retrieve member: {str(e)}", 500)


@app.route('/api/members', methods=['POST'])
def create_member():
    """POST /api/members - Create a new member"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body must be JSON", 400)
        
        required_fields = ['name', 'email']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return error_response(f"Missing required fields: {', '.join(missing_fields)}", 400)
        
        member_id = Member.create(name=data['name'], email=data['email'])
        
        return success_response({
            "id": member_id,
            "message": "Member created successfully"
        }, 201)
        
    except ValidationError as e:
        return error_response(str(e), 400)
    except DuplicateError as e:
        return error_response(str(e), 409)
    except Exception as e:
        return error_response(f"Failed to create member: {str(e)}", 500)


# ============================================================================
# TODO SYSTEM API ENDPOINTS (For Students to Implement)
# ============================================================================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    TODO: GET /api/tasks - Retrieve all tasks
    
    This should:
    1. Get optional 'status' query parameter for filtering
    2. Call Task.get_all() with status filter
    3. Return success response with tasks
    4. Handle errors appropriately
    
    Query Parameters:
        status (str): Filter by status - 'pending', 'in_progress', or 'completed'
    
    Response:
        200 OK: List of tasks
        500 Internal Server Error: Database error
    
    HINTS:
    - Follow the pattern from get_books()
    - Use request.args.get('status') to get query parameter
    - Call Task.get_all(status=status) if status provided
    
    EXAMPLE IMPLEMENTATION:
    try:
        status = request.args.get('status')
        tasks = Task.get_all(status=status)
        return success_response(tasks)
    except Exception as e:
        return error_response(f"Failed to retrieve tasks: {str(e)}", 500)
    """
    return error_response("TODO: Implement get_tasks endpoint", 501)


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    """
    TODO: GET /api/tasks/<id> - Retrieve a specific task
    
    This should:
    1. Call Task.get_by_id(task_id)
    2. Return 404 if task not found
    3. Return success response with task data
    
    HINTS:
    - Follow the pattern from get_book()
    - Check if task is None and return 404 error
    """
    return error_response("TODO: Implement get_task endpoint", 501)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """
    TODO: POST /api/tasks - Create a new task
    
    This should:
    1. Get JSON data from request
    2. Validate required fields (title)
    3. Call Task.create() with data
    4. Return 201 Created with task ID
    5. Handle ValidationError (400) and other errors (500)
    
    Request Body (JSON):
        {
            "title": "Task Title",
            "description": "Task Description",  // optional
            "status": "pending",  // optional
            "priority": "medium"  // optional
        }
    
    Response:
        201 Created: Task created successfully
        400 Bad Request: Validation error
        500 Internal Server Error: Database error
    
    HINTS:
    - Follow the pattern from create_book()
    - Required field: title
    - Optional fields: description, status, priority
    - Use data.get('field') for optional fields
    """
    return error_response("TODO: Implement create_task endpoint", 501)


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    """
    TODO: PUT /api/tasks/<id> - Update a task
    
    This should:
    1. Get JSON data from request
    2. Call Task.update_status() or Task.update() depending on fields
    3. Return 404 if task not found
    4. Return success response
    
    HINTS:
    - Follow the pattern from update_book()
    - Handle status updates specially if needed
    """
    return error_response("TODO: Implement update_task endpoint", 501)


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    """
    TODO: DELETE /api/tasks/<id> - Delete a task
    
    This should:
    1. Call Task.delete(task_id)
    2. Return 404 if task not found
    3. Return success response
    
    HINTS:
    - Follow the pattern from delete_book()
    - Very similar implementation
    """
    return error_response("TODO: Implement delete_task endpoint", 501)


# ============================================================================
# ROOT ENDPOINT (API Information)
# ============================================================================

@app.route('/')
def index():
    """
    Root endpoint - provides API information and available endpoints.
    """
    return jsonify({
        "name": "Python Backend Learning Project API",
        "version": "1.0.0",
        "description": "REST API for Library and Todo systems",
        "endpoints": {
            "library_system": {
                "books": {
                    "GET /api/books": "Get all books",
                    "GET /api/books/<id>": "Get book by ID",
                    "POST /api/books": "Create new book",
                    "PUT /api/books/<id>": "Update book",
                    "DELETE /api/books/<id>": "Delete book",
                    "GET /api/books/search": "Search books"
                },
                "members": {
                    "GET /api/members": "Get all members",
                    "GET /api/members/<id>": "Get member by ID",
                    "POST /api/members": "Create new member"
                }
            },
            "todo_system": {
                "tasks": {
                    "GET /api/tasks": "Get all tasks (TODO)",
                    "GET /api/tasks/<id>": "Get task by ID (TODO)",
                    "POST /api/tasks": "Create new task (TODO)",
                    "PUT /api/tasks/<id>": "Update task (TODO)",
                    "DELETE /api/tasks/<id>": "Delete task (TODO)"
                }
            }
        },
        "documentation": "See code comments for detailed endpoint documentation"
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return error_response("Endpoint not found", 404)


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors"""
    return error_response("Method not allowed for this endpoint", 405)


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error"""
    return error_response("Internal server error", 500)


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """
    Main entry point for the API server.
    
    Starts the Flask development server.
    """
    print("\n" + "=" * 70)
    print("  PYTHON BACKEND LEARNING PROJECT - REST API")
    print("=" * 70)
    print("\nStarting Flask development server...")
    print("API will be available at: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /                     - API information")
    print("  GET  /api/books            - List all books")
    print("  GET  /api/books/<id>       - Get book by ID")
    print("  POST /api/books            - Create new book")
    print("  PUT  /api/books/<id>       - Update book")
    print("  DELETE /api/books/<id>     - Delete book")
    print("  GET  /api/books/search     - Search books")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    # Run Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
