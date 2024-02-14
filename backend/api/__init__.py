from flask import Flask
from flask_cors import CORS
from .exts import init_exts
from .routes import *

def create_apis():
    app = Flask(__name__)
    CORS(app)

    db_uri = ""
    app.config["MONGO_URI"] = db_uri

    app.config['MONGODB_SETTINGS'] = {
        'db': 'your_database_name',
        'host': 'localhost',
        'port': 27017,
        # 'username': 'your_username',
        # 'password': 'your_password',
    }

    init_exts(app=app)

    return app
