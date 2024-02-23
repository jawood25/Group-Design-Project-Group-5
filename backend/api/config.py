import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

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
        'host': DBHOST,  # Database host URL
        'username': DBUSERNAME,  # Database username
        'password': DBPASSWORD,  # Database password
        'retryWrites': True,  # Enable retryable writes for reliability
        'w': 'majority'  # Ensure write operations are acknowledged by the majority of replica set members
    }


class DevelopmentConfig(BaseConfig):
    # Configuration for the development environment
    DEBUG = True  # Enable debug mode


class ProductionConfig(BaseConfig):
    # Configuration for the production environment
    pass  # No specific changes from BaseConfig


class TestingConfig(BaseConfig):
    # Configuration for the testing environment
    DEBUG = True  # Enable debug mode for testing


# Dictionary to select the configuration based on the environment
config = {
    "development": DevelopmentConfig,  # Development configuration
    "production": ProductionConfig,  # Production configuration
    "testing": TestingConfig  # Testing configuration
}
