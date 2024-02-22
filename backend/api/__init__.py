import os
import re
import logging

from flask import Flask
from flask_cors import CORS
from logging.handlers import RotatingFileHandler
from .exts import init_exts
from .routes import *
from .config import config
from .test import *


# Define a log filter to remove ANSI escape sequences from log messages
class RemoveAnsiEscapeCodesFilter(logging.Filter):
    def filter(self, record):
        ansi_escape = re.compile(r'\x1b\[([0-9]+)(;[0-9]+)*m')
        record.msg = ansi_escape.sub('', record.msg)
        return True


# Define the log directory and file path
log_directory = 'logs'
log_file_path = os.path.join(log_directory, 'log')

# Check if the log directory exists, create it if it does not
if not os.path.exists(log_directory):
    os.makedirs(log_directory)  # This will create the directory and any necessary parent directories

# Set basic logging configuration with a specific format and date format
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Create a file handler with UTF-8 encoding and a specific formatter
file_handler = RotatingFileHandler(log_directory, maxBytes=100 * 1024 * 1024, backupCount=5, encoding='utf-8')
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
file_handler.setFormatter(formatter)

# Configure the 'api' logger
api_logger = logging.getLogger('api')
api_logger.setLevel(logging.DEBUG)  # Set log level for 'api' logger
api_logger.addHandler(file_handler)  # Add file handler to 'api' logger

# Configure the 'werkzeug' logger with the same file handler and filter
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)  # Set log level for 'werkzeug' logger
werkzeug_logger.addFilter(RemoveAnsiEscapeCodesFilter())  # Apply the ANSI escape sequence filter
werkzeug_logger.addHandler(file_handler)  # Add file handler to 'werkzeug' logger


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
