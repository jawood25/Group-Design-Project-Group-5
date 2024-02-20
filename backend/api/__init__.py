import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .exts import init_exts
from .routes import *

from .test import *

load_dotenv()
NAME=os.getenv("DB_NAME")
HOST=os.getenv("DB_HOST")
USERNAME=os.getenv("DB_USERNAME")
PASSWORD=os.getenv("DB_PASSWORD")

# Function to create and configure the Flask app
def create_apis():
    # Initialize the Flask app
    app = Flask(__name__)
    # Enable CORS for all domains on all routes
    CORS(app)

    # Configure MongoDB settings for the Flask app
    app.config['MONGODB_SETTINGS'] = {
        'db': NAME,  # Name of the database
        'host': HOST,  # MongoDB Atlas cluster URL
        'username': USERNAME,  # Username for MongoDB
        'password': PASSWORD,  # Password for MongoDB
        'retryWrites': True,  # Enable retryable writes
        'w': 'majority'  # Write concern set to "majority" for data integrity
    }

    # Call the init_exts function to initialize Flask extensions with the app context
    init_exts(app=app)

    # Return the configured Flask app
    return app
