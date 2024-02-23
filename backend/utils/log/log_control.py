# IN DEVELOPMENT
import os
import re
import logging
from logging.handlers import RotatingFileHandler

# Define a log filter to remove ANSI escape sequences from log messages
class RemoveAnsiEscapeCodesFilter(logging.Filter):
    def filter(self, record):
        ansi_escape = re.compile(r'\x1b\[([0-9]+)(;[0-9]+)*m')
        record.msg = ansi_escape.sub('', record.msg)
        return True


# Define the log directory and file path
log_directory = 'logs'
log_file_path = os.path.join(log_directory, 'api.log')

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
