"""
Inventory Management System Models - CHALLENGE IMPLEMENTATION

This module provides the data models for the Inventory Management System.
This is a CHALLENGE exercise where you design and implement everything yourself.

LEARNING OBJECTIVES:
- Design and implement complete CRUD operations independently
- Handle complex relationships (one-to-many, many-to-many)
- Implement business logic (stock management, validation)
- Apply error handling patterns learned from library.py and todo.py

REQUIREMENTS:
Your implementation should support these use cases:
- UC-11: Add a Product with validation
- UC-12: Update Stock Levels (prevent negative stock)
- UC-13: Search Products by Category (JOIN operations)
- UC-14: Find Products by Supplier (JOIN operations)
- UC-15: Low Stock Alert (filtering and sorting)

STUDY FIRST:
Before implementing, review:
- models/library.py for complete CRUD examples
- models/todo.py for guided patterns
- database/connection.py for query execution functions
- validation/validators.py for validation patterns
- utils/error_handlers.py for exception handling

HINTS:
- Start with the simplest operations (create, get_by_id)
- Add validation before database operations
- Use parameterized queries to prevent SQL injection
- Handle errors gracefully with try-except blocks
- Test each function as you implement it
"""

from typing import List, Dict, Optional
from database.connection import execute_query, execute_update
from utils.error_handlers import ValidationError, NotFoundError, DuplicateError
from validation.validators import validate_not_empty, validate_choice
import sqlite3


# ============================================================================
# PRODUCT MODEL
# ============================================================================

class Product:
    """
    Product model for inventory management.
    
    A product represents an item in the inventory with pricing, stock quantity,
    and relationships to suppliers and categories.
    
    CHALLENGE: Implement all methods following the patterns from Book and Task classes.
    """
    
    @staticmethod
    def create(name: str, description: str, price: float, stock_quantity: int, 
               supplier_id: int) -> int:
        """
        Create a new product in the inventory.
        
        Args:
            name: Product name (required, cannot be empty)
            description: Product description (optional, can be empty string)
            price: Product price (required, must be positive)
            stock_quantity: Initial stock quantity (required, must be non-negative)
            supplier_id: ID of the supplier (required, must exist in suppliers table)
        
        Returns:
            int: ID of the newly created product
        
        Raises:
            ValidationError: If any input validation fails
            NotFoundError: If supplier_id doesn't exist
            DatabaseError: If database operation fails
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Validate all inputs:
           - name must not be empty (use validate_not_empty)
           - price must be positive (price > 0)
           - stock_quantity must be non-negative (>= 0)
           - supplier_id must exist in suppliers table
        
        2. Execute INSERT query with parameterized values
        
        3. Return the ID of the newly created product (use cursor.lastrowid)
        
        4. Handle errors:
           - sqlite3.IntegrityError for foreign key violations
           - Other database errors appropriately
        
        HINTS:
        - Study Book.create() in models/library.py for the pattern
        - Use execute_update() from database/connection.py
        - Query: INSERT INTO products (name, description, price, stock_quantity, supplier_id)
                 VALUES (?, ?, ?, ?, ?)
        """
        pass
    
    @staticmethod
    def get_by_id(product_id: int) -> Optional[Dict]:
        """
        Retrieve a product by its ID.
        
        Args:
            product_id: ID of the product to retrieve
        
        Returns:
            Dict with product data if found, None if not found
            Dictionary keys: id, name, description, price, stock_quantity, 
                           supplier_id, created_at, updated_at
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Execute SELECT query with WHERE clause
        2. Return first result as dictionary, or None if not found
        
        HINTS:
        - Study Book.get_by_id() or Task.get_by_id() for the pattern
        - Use execute_query() from database/connection.py
        - Query: SELECT * FROM products WHERE id = ?
        - execute_query returns a list, so check if list is empty
        """
        pass
    
    @staticmethod
    def get_all(category_id: Optional[int] = None, in_stock_only: bool = False) -> List[Dict]:
        """
        Retrieve all products, with optional filtering.
        
        Args:
            category_id: If provided, filter products by this category (requires JOIN)
            in_stock_only: If True, only return products with stock_quantity > 0
        
        Returns:
            List of dictionaries, each containing product data
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Build query dynamically based on filters
        2. If category_id provided, JOIN with product_categories table
        3. If in_stock_only is True, add WHERE stock_quantity > 0
        4. Order results by product name alphabetically
        
        HINTS:
        - Start with base query: SELECT p.* FROM products p
        - If category_id: JOIN product_categories pc ON p.id = pc.product_id
        - Build WHERE clauses conditionally
        - Use ORDER BY p.name
        - Study Book.get_all() for filtering patterns
        
        EXAMPLE QUERY WITH CATEGORY FILTER:
        SELECT p.* FROM products p
        JOIN product_categories pc ON p.id = pc.product_id
        WHERE pc.category_id = ?
        ORDER BY p.name
        """
        pass
    
    @staticmethod
    def get_by_supplier(supplier_id: int) -> List[Dict]:
        """
        Retrieve all products from a specific supplier.
        
        Args:
            supplier_id: ID of the supplier
        
        Returns:
            List of dictionaries containing product data
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Query products WHERE supplier_id matches
        2. Order by product name
        3. Return empty list if no products found
        
        HINTS:
        - Query: SELECT * FROM products WHERE supplier_id = ? ORDER BY name
        - Use execute_query()
        """
        pass
    
    @staticmethod
    def get_low_stock(threshold: int = 10) -> List[Dict]:
        """
        Retrieve products with stock below a threshold.
        
        Args:
            threshold: Stock quantity threshold (default 10)
        
        Returns:
            List of dictionaries with product data and supplier information
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Query products WHERE stock_quantity < threshold
        2. JOIN with suppliers table to include supplier information
        3. Order by stock_quantity ascending (lowest first)
        4. Include both product and supplier data in results
        
        HINTS:
        - Use JOIN to get supplier information
        - Query: SELECT p.*, s.name as supplier_name, s.contact_email as supplier_email
                 FROM products p
                 JOIN suppliers s ON p.supplier_id = s.id
                 WHERE p.stock_quantity < ?
                 ORDER BY p.stock_quantity ASC
        """
        pass
    
    @staticmethod
    def update_stock(product_id: int, quantity_change: int) -> bool:
        """
        Update product stock quantity by adding or subtracting.
        
        Args:
            product_id: ID of the product to update
            quantity_change: Amount to add (positive) or subtract (negative)
        
        Returns:
            bool: True if update successful, False if product not found
        
        Raises:
            ValidationError: If resulting stock would be negative
            NotFoundError: If product doesn't exist
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Get current product to check current stock
        2. Calculate new stock: current_stock + quantity_change
        3. Validate new stock is not negative
        4. Update stock_quantity in database
        5. Return True if successful
        
        HINTS:
        - First call get_by_id() to get current product
        - Check if product exists (raise NotFoundError if not)
        - Calculate new_stock = product['stock_quantity'] + quantity_change
        - Validate new_stock >= 0 (raise ValidationError if negative)
        - Query: UPDATE products SET stock_quantity = ? WHERE id = ?
        
        BUSINESS LOGIC:
        - Positive quantity_change = restocking (adding inventory)
        - Negative quantity_change = sale or removal (subtracting inventory)
        - Never allow negative stock
        """
        pass
    
    @staticmethod
    def update(product_id: int, **kwargs) -> bool:
        """
        Update product fields dynamically.
        
        Args:
            product_id: ID of the product to update
            **kwargs: Fields to update (name, description, price, supplier_id)
        
        Returns:
            bool: True if update successful, False if product not found
        
        Raises:
            ValidationError: If validation fails for any field
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Validate each field being updated
        2. Build UPDATE query dynamically based on provided fields
        3. Execute update with parameterized values
        4. Return True if rows affected > 0
        
        HINTS:
        - Study Book.update() for dynamic field updates
        - Validate: name (not empty), price (> 0), supplier_id (exists)
        - Build query: UPDATE products SET field1 = ?, field2 = ? WHERE id = ?
        - Don't allow updating stock_quantity here (use update_stock instead)
        """
        pass
    
    @staticmethod
    def delete(product_id: int) -> bool:
        """
        Delete a product from the inventory.
        
        Args:
            product_id: ID of the product to delete
        
        Returns:
            bool: True if deleted, False if product not found
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Execute DELETE query
        2. Return True if rows affected > 0
        
        HINTS:
        - Query: DELETE FROM products WHERE id = ?
        - Use execute_update()
        - Study Book.delete() for the pattern
        
        NOTE:
        If you set up ON DELETE CASCADE in product_categories table,
        deleting a product will automatically delete its category links.
        """
        pass
    
    @staticmethod
    def add_category(product_id: int, category_id: int) -> bool:
        """
        Add a product to a category (create many-to-many relationship).
        
        Args:
            product_id: ID of the product
            category_id: ID of the category
        
        Returns:
            bool: True if added successfully
        
        Raises:
            DuplicateError: If product is already in this category
            NotFoundError: If product or category doesn't exist
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Verify product exists
        2. Verify category exists
        3. Insert into product_categories junction table
        4. Handle duplicate constraint violation
        
        HINTS:
        - Query: INSERT INTO product_categories (product_id, category_id) VALUES (?, ?)
        - Catch sqlite3.IntegrityError for duplicates
        - Use execute_update()
        """
        pass
    
    @staticmethod
    def remove_category(product_id: int, category_id: int) -> bool:
        """
        Remove a product from a category.
        
        Args:
            product_id: ID of the product
            category_id: ID of the category
        
        Returns:
            bool: True if removed, False if relationship didn't exist
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. Delete from product_categories junction table
        2. Return True if rows affected > 0
        
        HINTS:
        - Query: DELETE FROM product_categories WHERE product_id = ? AND category_id = ?
        """
        pass
    
    @staticmethod
    def get_categories(product_id: int) -> List[Dict]:
        """
        Get all categories for a product.
        
        Args:
            product_id: ID of the product
        
        Returns:
            List of category dictionaries
        
        TODO: Implement this method
        
        REQUIREMENTS:
        1. JOIN product_categories and categories tables
        2. Filter by product_id
        3. Return category information
        
        HINTS:
        - Query: SELECT c.* FROM categories c
                 JOIN product_categories pc ON c.id = pc.category_id
                 WHERE pc.product_id = ?
        """
        pass


# ============================================================================
# CATEGORY MODEL
# ============================================================================

class Category:
    """
    Category model for organizing products.
    
    Categories help organize products into logical groups.
    A product can belong to multiple categories (many-to-many relationship).
    
    CHALLENGE: Implement all methods.
    """
    
    @staticmethod
    def create(name: str, description: str = "") -> int:
        """
        Create a new category.
        
        Args:
            name: Category name (required, must be unique)
            description: Category description (optional)
        
        Returns:
            int: ID of the newly created category
        
        Raises:
            ValidationError: If name is empty
            DuplicateError: If category name already exists
        
        TODO: Implement this method
        
        HINTS:
        - Validate name is not empty
        - Query: INSERT INTO categories (name, description) VALUES (?, ?)
        - Handle sqlite3.IntegrityError for duplicate names
        """
        pass
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Dict]:
        """
        Retrieve a category by ID.
        
        TODO: Implement following the pattern from Product.get_by_id()
        """
        pass
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Retrieve all categories, ordered by name.
        
        TODO: Implement this method
        
        HINTS:
        - Query: SELECT * FROM categories ORDER BY name
        """
        pass
    
    @staticmethod
    def update(category_id: int, **kwargs) -> bool:
        """
        Update category fields.
        
        TODO: Implement following the pattern from Product.update()
        """
        pass
    
    @staticmethod
    def delete(category_id: int) -> bool:
        """
        Delete a category.
        
        TODO: Implement this method
        
        NOTE: If you set up ON DELETE CASCADE, deleting a category will
        automatically remove all product-category relationships.
        """
        pass
    
    @staticmethod
    def get_products(category_id: int) -> List[Dict]:
        """
        Get all products in a category.
        
        Args:
            category_id: ID of the category
        
        Returns:
            List of product dictionaries
        
        TODO: Implement this method
        
        HINTS:
        - This is the reverse of Product.get_categories()
        - Query: SELECT p.* FROM products p
                 JOIN product_categories pc ON p.id = pc.product_id
                 WHERE pc.category_id = ?
                 ORDER BY p.name
        """
        pass


# ============================================================================
# SUPPLIER MODEL
# ============================================================================

class Supplier:
    """
    Supplier model for managing product suppliers.
    
    Suppliers provide products. Each product has one supplier (one-to-many).
    
    CHALLENGE: Implement all methods.
    """
    
    @staticmethod
    def create(name: str, contact_name: str = "", contact_email: str = "",
               contact_phone: str = "", address: str = "") -> int:
        """
        Create a new supplier.
        
        Args:
            name: Supplier name (required, must be unique)
            contact_name: Contact person name (optional)
            contact_email: Contact email (optional)
            contact_phone: Contact phone (optional)
            address: Supplier address (optional)
        
        Returns:
            int: ID of the newly created supplier
        
        Raises:
            ValidationError: If name is empty or email format is invalid
            DuplicateError: If supplier name already exists
        
        TODO: Implement this method
        
        HINTS:
        - Validate name is not empty
        - If contact_email provided, validate email format (use validate_email from validators.py)
        - Query: INSERT INTO suppliers (name, contact_name, contact_email, contact_phone, address)
                 VALUES (?, ?, ?, ?, ?)
        - Handle sqlite3.IntegrityError for duplicate names
        """
        pass
    
    @staticmethod
    def get_by_id(supplier_id: int) -> Optional[Dict]:
        """
        Retrieve a supplier by ID.
        
        TODO: Implement following the pattern from Product.get_by_id()
        """
        pass
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Retrieve all suppliers, ordered by name.
        
        TODO: Implement this method
        """
        pass
    
    @staticmethod
    def update(supplier_id: int, **kwargs) -> bool:
        """
        Update supplier fields.
        
        TODO: Implement following the pattern from Product.update()
        
        HINT: Validate email format if contact_email is being updated
        """
        pass
    
    @staticmethod
    def delete(supplier_id: int) -> bool:
        """
        Delete a supplier.
        
        TODO: Implement this method
        
        WARNING: This will fail if any products reference this supplier
        (foreign key constraint). You may want to check for products first
        and raise a ValidationError with a helpful message.
        """
        pass
    
    @staticmethod
    def get_products(supplier_id: int) -> List[Dict]:
        """
        Get all products from a supplier.
        
        Args:
            supplier_id: ID of the supplier
        
        Returns:
            List of product dictionaries
        
        TODO: Implement this method
        
        HINTS:
        - This is the same as Product.get_by_supplier()
        - Query: SELECT * FROM products WHERE supplier_id = ? ORDER BY name
        """
        pass


# ============================================================================
# TESTING YOUR IMPLEMENTATION
# ============================================================================
"""
After implementing the models, test them with these steps:

1. Initialize the database:
   - First, complete the schema in database/schemas/inventory_schema.sql
   - Run: python setup.py

2. Test in Python REPL:
   >>> from models.inventory import Product, Category, Supplier
   
   # Create a supplier
   >>> supplier_id = Supplier.create("Tech Supplies Inc", contact_email="contact@tech.com")
   >>> print(f"Created supplier: {supplier_id}")
   
   # Create a category
   >>> category_id = Category.create("Electronics", "Electronic devices")
   >>> print(f"Created category: {category_id}")
   
   # Create a product
   >>> product_id = Product.create("Wireless Mouse", "Ergonomic mouse", 29.99, 50, supplier_id)
   >>> print(f"Created product: {product_id}")
   
   # Add product to category
   >>> Product.add_category(product_id, category_id)
   
   # Get product details
   >>> product = Product.get_by_id(product_id)
   >>> print(product)
   
   # Update stock
   >>> Product.update_stock(product_id, -5)  # Sold 5 units
   >>> product = Product.get_by_id(product_id)
   >>> print(f"New stock: {product['stock_quantity']}")
   
   # Get low stock products
   >>> low_stock = Product.get_low_stock(threshold=100)
   >>> for p in low_stock:
   ...     print(f"{p['name']}: {p['stock_quantity']} units")

3. Write unit tests (optional but recommended):
   - Create test_inventory_models.py
   - Test each CRUD operation
   - Test edge cases (negative stock, duplicate names, etc.)

GOOD LUCK! Remember to study the library.py and todo.py models for patterns.
"""
