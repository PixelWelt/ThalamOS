#!/var/www/flask-app/venv/bin/python3.11
import sys
import os

# Add the application directory to the Python path
sys.path.insert(0, '/var/www/flask-app/')

# Import your Flask app
from app import app as application  
print(f"Flask application: {application}")