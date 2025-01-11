"""
WSGI entry point for the StorageManager application.

This module initializes and runs the Flask application defined in the `app` package.
When executed as the main module, it starts the Flask development server.

Attributes:
    app (Flask): The Flask application instance imported from the `app` package.
"""
from app import app


# Add the application directory to the Python path
if __name__ == "__main__":
    app.run()
