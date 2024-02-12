from flask import Flask
from flask_cors import CORS
from .exts import init_exts
from .urls import *

def create_app():
    app = Flask(__name__)
    CORS(app)

    db_url = ""
    app.config["MONGO_URI"] = db_url

    init_exts(app=app)

    return app
