
from flask import Flask
from flask_cors import CORS

from .exts import init_exts
from .routes import *
from .config import config


# Function to create and configure the Flask app
def create_app(config_name='development'):
    # Initialize the Flask app
    app = Flask(__name__)
    # Load the configuration settings for the Flask app
    app.config.from_object(config[config_name])
    # Enable CORS for all domains on all routes
    CORS(app)
    # Call the init_exts function to initialize Flask extensions with the app context
    init_exts(app=app)

    # Return the configured Flask app
    return app
