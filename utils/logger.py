"""
Logging Configuration Module

This module sets up logging for the application to help with debugging and monitoring.
Students will learn about:
- Python's built-in logging module
- Different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Logging to files and console
- Formatting log messages
- Using loggers in application code

Key Concepts:
1. Log Levels: Different severity levels for different types of messages
2. Handlers: Where log messages go (console, file, etc.)
3. Formatters: How log messages are formatted
4. Logger Hierarchy: Organizing loggers by module
5. Best Practices: When to log and what to log

Why Logging Matters:
- Helps debug issues in production
- Tracks application behavior over time
- Records errors for later analysis
- Provides audit trail of operations
- Essential for maintaining production systems
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str = "backend_learning",
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True
) -> logging.Logger:
    """
    Set up and configure a logger for the application.
    
    This function creates a logger with both file and console output.
    It's designed to be educational, showing students how to configure
    logging for their applications.
    
    Args:
        name: Name of the logger (usually the module name)
        level: Minimum log level to record (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to write logs to a file
        log_to_console: Whether to write logs to console (terminal)
    
    Returns:
        logging.Logger: Configured logger ready to use
    
    Example:
        >>> logger = setup_logger("my_module")
        >>> logger.info("Application started")
        >>> logger.warning("This is a warning")
        >>> logger.error("An error occurred")
    
    Learning Notes:
    - Loggers are organized in a hierarchy by name (e.g., "app.database.connection")
    - Log levels from lowest to highest: DEBUG < INFO < WARNING < ERROR < CRITICAL
    - Only messages at or above the configured level are recorded
    - Multiple handlers can be attached to send logs to different destinations
    """
    # Create or get the logger
    # If a logger with this name already exists, it will be returned
    logger = logging.getLogger(name)
    
    # Set the minimum log level
    # Messages below this level will be ignored
    logger.setLevel(level)
    
    # Prevent logs from propagating to parent loggers
    # This avoids duplicate log messages
    logger.propagate = False
    
    # Clear any existing handlers
    # This prevents duplicate handlers if setup_logger is called multiple times
    logger.handlers.clear()
    
    # Create a formatter for log messages
    # This defines how each log message will look
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Format explanation:
    # %(asctime)s - Timestamp when the log was created
    # %(name)s - Name of the logger
    # %(levelname)s - Log level (INFO, WARNING, ERROR, etc.)
    # %(message)s - The actual log message
    
    # Add console handler if requested
    if log_to_console:
        # StreamHandler writes to sys.stdout (the console/terminal)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create log filename with current date
        # This creates a new log file each day
        log_filename = f"backend_learning_{datetime.now().strftime('%Y%m%d')}.log"
        log_path = log_dir / log_filename
        
        # FileHandler writes to a file
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create a default logger for the application
# Other modules can import and use this logger
default_logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    This is a convenience function that creates a child logger
    under the main application logger.
    
    Args:
        name: Name for the logger (typically __name__ from the calling module)
    
    Returns:
        logging.Logger: Logger configured for the module
    
    Example:
        >>> # In your module file
        >>> logger = get_logger(__name__)
        >>> logger.info("Module initialized")
    
    Learning Notes:
    - Using __name__ as the logger name creates a hierarchy
    - For example, if __name__ is "models.library", the logger will be
      "backend_learning.models.library"
    - This helps organize logs by module
    - Child loggers inherit settings from parent loggers
    """
    return logging.getLogger(f"backend_learning.{name}")


# Example usage and demonstrations for students
def demonstrate_logging():
    """
    Demonstrate different logging levels and use cases.
    
    This function shows students when to use each log level.
    Run this function to see example log output.
    """
    logger = setup_logger("demo", level=logging.DEBUG)
    
    print("\n=== Logging Demonstration ===\n")
    
    # DEBUG: Detailed information for diagnosing problems
    # Use for: Variable values, function calls, detailed flow
    logger.debug("This is a DEBUG message - detailed diagnostic information")
    logger.debug("Variable value: x = 42")
    
    # INFO: General informational messages
    # Use for: Confirming things are working, major steps in process
    logger.info("This is an INFO message - application is running normally")
    logger.info("Database connection established")
    logger.info("Processing 100 records")
    
    # WARNING: Something unexpected happened, but application continues
    # Use for: Deprecated features, unusual situations, potential problems
    logger.warning("This is a WARNING message - something unusual happened")
    logger.warning("Database query took 5 seconds (expected < 1 second)")
    logger.warning("Using deprecated function, please update your code")
    
    # ERROR: A serious problem occurred, operation failed
    # Use for: Exceptions, failed operations, errors that need attention
    logger.error("This is an ERROR message - an operation failed")
    logger.error("Failed to save record to database")
    logger.error("Invalid user input: email format incorrect")
    
    # CRITICAL: A very serious error, application may not continue
    # Use for: System failures, data corruption, unrecoverable errors
    logger.critical("This is a CRITICAL message - system failure")
    logger.critical("Database connection lost and cannot reconnect")
    logger.critical("Out of disk space, cannot write data")
    
    print("\n=== End of Demonstration ===\n")
    print("Check the logs/ directory for the log file!")


def demonstrate_exception_logging():
    """
    Demonstrate logging exceptions with full traceback.
    
    This shows students how to log exceptions properly,
    including the full stack trace for debugging.
    """
    logger = setup_logger("exception_demo")
    
    print("\n=== Exception Logging Demonstration ===\n")
    
    try:
        # Simulate an error
        result = 10 / 0
    except ZeroDivisionError as e:
        # Log the exception with full traceback
        # exc_info=True includes the stack trace
        logger.error("Division by zero error occurred", exc_info=True)
        
        # Alternative: use logger.exception() which automatically includes exc_info
        logger.exception("This also logs the full exception details")
    
    print("\n=== End of Exception Demonstration ===\n")


# Best Practices Documentation
"""
LOGGING BEST PRACTICES:

1. Choose the Right Log Level:
   - DEBUG: Detailed diagnostic info (usually only in development)
   - INFO: Confirmation that things are working as expected
   - WARNING: Something unexpected, but not an error
   - ERROR: A serious problem, operation failed
   - CRITICAL: System failure, application may crash

2. What to Log:
   ✓ Application startup and shutdown
   ✓ Configuration changes
   ✓ User authentication attempts
   ✓ Database operations (especially failures)
   ✓ External API calls
   ✓ Errors and exceptions
   ✓ Performance issues (slow queries, timeouts)
   
   ✗ Sensitive data (passwords, credit cards, personal info)
   ✗ Too much detail in production (use DEBUG level for that)
   ✗ Redundant information

3. Log Message Format:
   - Be clear and specific
   - Include context (user ID, record ID, etc.)
   - Use consistent terminology
   - Good: "Failed to create book: ISBN '978-1234567890' already exists"
   - Bad: "Error in create function"

4. Exception Logging:
   - Always log exceptions with exc_info=True or use logger.exception()
   - Include context about what operation was being performed
   - Log at ERROR or CRITICAL level

5. Performance Considerations:
   - Logging has a small performance cost
   - Use DEBUG level for verbose logging, disable in production
   - Don't log inside tight loops
   - Consider async logging for high-volume applications

6. Log File Management:
   - Rotate log files to prevent them from growing too large
   - Archive old logs
   - Set up log monitoring and alerting in production
   - Consider using a log aggregation service (e.g., ELK stack)

COMMON PATTERNS:

Pattern 1: Logging Function Entry/Exit (DEBUG level)
    def process_data(data):
        logger.debug(f"Entering process_data with {len(data)} items")
        # ... processing ...
        logger.debug("Exiting process_data successfully")

Pattern 2: Logging Operations (INFO level)
    def create_book(title, author):
        logger.info(f"Creating book: '{title}' by {author}")
        # ... create book ...
        logger.info(f"Book created successfully with ID {book_id}")

Pattern 3: Logging Errors with Context (ERROR level)
    try:
        book = Book.create(title, author, isbn)
    except ValidationError as e:
        logger.error(f"Validation failed for book '{title}': {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error creating book '{title}'")
        raise

Pattern 4: Logging Performance Issues (WARNING level)
    start_time = time.time()
    results = execute_query(query)
    duration = time.time() - start_time
    if duration > 1.0:
        logger.warning(f"Slow query detected: {duration:.2f}s - {query}")

EXERCISES FOR STUDENTS:

1. Add logging to your Todo model functions
   - Log when tasks are created, updated, or deleted
   - Log validation errors
   - Log database errors

2. Experiment with different log levels
   - Run your application with DEBUG level
   - Run it with WARNING level
   - Notice what information you see at each level

3. Add exception logging
   - Wrap database operations in try-except
   - Log exceptions with full traceback
   - Practice writing helpful error messages

4. Review log files
   - Run your application and generate some logs
   - Open the log file and review the output
   - Practice reading stack traces

NEXT STEPS:
- Import and use logging in your model files
- Add logging to error handlers
- Practice writing clear, helpful log messages
- Learn about log rotation and management
"""


# If this file is run directly, show demonstrations
if __name__ == "__main__":
    print("Running logging demonstrations...")
    demonstrate_logging()
    demonstrate_exception_logging()
    print("\nDemonstrations complete!")
    print("Check the logs/ directory for log files.")

