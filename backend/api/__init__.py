from flask import Flask
from flask_cors import CORS
from .exts import init_exts
from .routes import *

# Function to create and configure the Flask app
def create_apis():
    # Initialize the Flask app
    app = Flask(__name__)
    # Enable CORS for all domains on all routes
    CORS(app)

    # Configure MongoDB settings for the Flask app
    app.config['MONGODB_SETTINGS'] = {
        'db': 'pathpal',  # Name of the database
        'host': 'mongodb+srv://cluster0.b6yu9ji.mongodb.net',  # MongoDB Atlas cluster URL
        'username': 'PathPalAdmin',  # Username for MongoDB
        'password': 'YOAybG23XVTqQnri',  # Password for MongoDB
        'retryWrites': True,  # Enable retryable writes
        'w': 'majority'  # Write concern set to "majority" for data integrity
    }

    # Call the init_exts function to initialize Flask extensions with the app context
    init_exts(app=app)

    # Return the configured Flask app
    return app
