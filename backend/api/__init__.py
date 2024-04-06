# /api/__init__.py
from flask import Flask
from flask_cors import CORS

from .config import config  # Importing configuration settings
from .exts import init_exts  # Importing extension initializer
from .routes import *  # Importing all routes


def create_app(config_name='development'):
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_name (str): The configuration name to use for the Flask app.
                           Defaults to 'development'.

    Returns:
        Flask: The configured Flask application instance.
    """

    # Initialize Flask application
    app = Flask(__name__)

    # Load app configuration from 'config' dict based on the provided config_name
    app.config.from_object(config[config_name])

    # Enable Cross-Origin Resource Sharing (CORS) for all domains across all routes
    CORS(app)

    # Initialize Flask extensions with the current app context
    init_exts(app=app)

    # Return the configured Flask app instance
    return app
