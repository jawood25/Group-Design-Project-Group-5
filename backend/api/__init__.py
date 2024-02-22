import re
import logging

from flask import Flask
from flask_cors import CORS
from logging.handlers import RotatingFileHandler
from .exts import init_exts
from .routes import *
from .config import config
from .test import *


class NoColorFilter(logging.Filter):
    def filter(self, record):
        # 使用正则表达式去除 ANSI 颜色代码
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        record.msg = ansi_escape.sub('', record.msg)
        return True


# Set the logging level
logging.basicConfig(level=logging.DEBUG)  # Debug level for debugging
# Create a log recorder, specifying the path where logs are saved, the maximum size of each log file, and the maximum number of log files
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
file_log_handler.addFilter(NoColorFilter())
# Create the format for logging records: log level, filename and line number of the log message, and the log message itself
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# Set the logging format for the newly created log recorder
file_log_handler.setFormatter(formatter)
# Add the log recorder to the global logging tool object (used by the application instance app) for logging
logging.getLogger().addHandler(file_log_handler)


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
