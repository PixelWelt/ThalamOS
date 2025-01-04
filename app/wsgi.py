#!/var/www/flask-app/venv/bin/python3.11
from app import app
import sys
import os

# Add the application directory to the Python path
sys.path.insert(0, '/app')
if __name__ == "__main__":
	app.run()
