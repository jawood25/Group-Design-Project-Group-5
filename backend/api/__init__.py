from flask import Flask
from flask_cors import CORS
from .exts import init_exts
from .routes import *

from .test import *

# Function to create and configure the Flask app
def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    # Enable CORS for all domains on all routes
    CORS(app)
    app.config.from_object('api.config.BaseConfig')
    # Call the init_exts function to initialize Flask extensions with the app context
    init_exts(app=app)

    # Return the configured Flask app
    return app
