import os, random, string
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
load_dotenv()


class BaseConfig(object):

    DEBUG = True
    HOST = 'localhost'
    PORT = 3001

    DBNAME = os.getenv("DB_NAME")
    DBHOST = os.getenv("DB_HOST")
    DBUSERNAME = os.getenv("DB_USERNAME")
    DBPASSWORD = os.getenv("DB_PASSWORD")

    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', None)
    if not JWT_SECRET_KEY:
        JWT_SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Configure MongoDB settings for the Flask app
    MONGODB_SETTINGS ={
        'db': DBNAME,  # Name of the database
        'host': DBHOST,  # MongoDB Atlas cluster URL
        'username': DBUSERNAME,  # Username for MongoDB
        'password': DBPASSWORD,  # Password for MongoDB
        'retryWrites': True,  # Enable retryable writes
        'w': 'majority'  # Write concern set to "majority" for data integrity
    }