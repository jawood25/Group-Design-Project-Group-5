# /api/config.py
import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


# pylint: disable=too-few-public-methods
class BaseConfig():
    # Base configuration
    HOST = 'localhost'  # Default host
    PORT = 3001  # Default port

    # Environment variables for database connection
    DBNAME = os.getenv("DB_NAME")  # Database name
    DBHOST = os.getenv("DB_HOST")  # Database host URL
    DBUSERNAME = os.getenv("DB_USERNAME")  # Database username
    DBPASSWORD = os.getenv("DB_PASSWORD")  # Database password

    # MongoDB connection settings
    MONGODB_SETTINGS = {
        'db': DBNAME,  # Name of the database
        'host': f"mongodb+srv://{DBHOST}",  # Database host URL
        'username': DBUSERNAME,  # Database username
        'password': DBPASSWORD,  # Database password
        'retryWrites': True,  # Retry writes in case of failure
        'w': 'majority'  # Write acknowledgment level
    }


# pylint: disable=too-few-public-methods
class DevelopmentConfig(BaseConfig):
    # Configuration for the development environment
    DEBUG = True  # Enable debug mode


# pylint: disable=too-few-public-methods
class ProductionConfig(BaseConfig):
    # Configuration for the production environment
    pass  # No specific changes from BaseConfig


# pylint: disable=too-few-public-methods
class TestingConfig(BaseConfig):
    # Configuration for the testing environment
    DEBUG = True  # Enable debug mode for testing
    # Environment variables for database connection
    DBNAME = 'pytest'
    DBHOST = os.getenv("DB_HOST")  # Database host URL
    DBUSERNAME = os.getenv("DB_USERNAME")  # Database username
    DBPASSWORD = os.getenv("DB_PASSWORD")  # Database password

    MONGO_URI = f"mongodb+srv://{DBUSERNAME}:{DBPASSWORD}@{DBHOST}/{DBNAME}" \
                f"?retryWrites=true&w=majority&authSource=admin"

    # MongoDB connection settings
    MONGODB_SETTINGS = {
        'host': MONGO_URI
    }


# Dictionary to select the configuration based on the environment
config = {
    "development": DevelopmentConfig,  # Development configuration
    "production": ProductionConfig,  # Production configuration
    "testing": TestingConfig  # Testing configuration
}
