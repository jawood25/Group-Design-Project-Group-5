# /api/exts.py
from flask_mongoengine import MongoEngine
from flask_restx import Api

# Create instances of the MongoEngine and Api classes
db = MongoEngine()  # Initializes MongoDB support via MongoEngine
api = Api(version="1.0", title="Users API", description="A simple Users API")


def init_exts(app):
    """
    Initializes Flask extensions with the given app context.

    This function takes a Flask application instance as its argument and initializes
    the MongoEngine and Flask-RestX extensions by passing the app instance to them.
    This setup is crucial for integrating these extensions into the Flask application.

    Args:
        app: The Flask application instance.
    """
    # Initialize MongoEngine with the app instance for MongoDB support
    db.init_app(app=app)

    # Initialize Flask-RestX Api with the app instance for API functionality
    api.init_app(app=app)
