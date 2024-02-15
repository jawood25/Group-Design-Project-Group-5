import certifi
from flask import Flask
from flask_cors import CORS
from .exts import init_exts
from .routes import *


def create_apis():
    app = Flask(__name__)
    CORS(app)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'pathpal',
        'host': 'mongodb+srv://cluster0.b6yu9ji.mongodb.net',
        'username': 'PathPalAdmin',
        'password': 'YOAybG23XVTqQnri',
        'retryWrites': True,
        'w': 'majority'
    }

    init_exts(app=app)

    return app
