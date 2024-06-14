# /api/config.py
import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class BaseConfig:
    """
    Base configuration class. Contains default settings and environment-dependent
    database connection settings.
    """
    # Default server settings
    HOST = 'localhost'
    PORT = 3001

    # Environment-dependent database settings
    DBNAME = os.getenv("DB_NAME")
    DBHOST = os.getenv("DB_HOST")
    DBUSERNAME = os.getenv("DB_USERNAME")
    DBPASSWORD = os.getenv("DB_PASSWORD")

    # MongoDB connection settings using environment variables
    MONGODB_SETTINGS = {
        'db': DBNAME,
        'host': f"mongodb+srv://{DBHOST}",
        'username': DBUSERNAME,
        'password': DBPASSWORD,
        'retryWrites': True,
        'w': 'majority'
    }


class DevelopmentConfig(BaseConfig):
    """
    Configuration for the development environment. Enables debug mode.
    """
    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    Configuration for the production environment. Inherits settings from BaseConfig
    without modification.
    """
    pass


class TestingConfig(BaseConfig):
    """
    Configuration for the testing environment. Overrides database settings for
    testing and enables debug mode.
    """
    DEBUG = True
    DBNAME = 'pytest'
    DBHOST = os.getenv("DB_HOST")  # Database host URL
    DBUSERNAME = os.getenv("DB_USERNAME")  # Database username
    DBPASSWORD = os.getenv("DB_PASSWORD")  # Database password

    MONGO_URI = f"mongodb+srv://{DBUSERNAME}:{DBPASSWORD}@{DBHOST}/{DBNAME}" \
                f"?retryWrites=true&w=majority&authSource=admin"

    MONGODB_SETTINGS = {
        'host': MONGO_URI
    }


# Mapping of configuration names to configuration classes
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
