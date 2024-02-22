import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    HOST = 'localhost'
    PORT = 3001

    DBNAME = os.getenv("DB_NAME")
    DBHOST = os.getenv("DB_HOST")
    DBUSERNAME = os.getenv("DB_USERNAME")
    DBPASSWORD = os.getenv("DB_PASSWORD")

    # Configure MongoDB settings for the Flask app
    MONGODB_SETTINGS = {
        'db': DBNAME,  # Name of the database
        'host': DBHOST,  # MongoDB Atlas cluster URL
        'username': DBUSERNAME,  # Username for MongoDB
        'password': DBPASSWORD,  # Password for MongoDB
        'retryWrites': True,  # Enable retryable writes
        'w': 'majority'  # Write concern set to "majority" for data integrity
    }


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


config = {
    "development": DevelopmentConfig,  # Development environment configuration
    "production": ProductionConfig  # Production environment configuration
}
