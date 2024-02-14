from flask import Flask
from flask_cors import CORS
from .exts import init_exts
from .routes import *

def create_apis():
    app = Flask(__name__)
    CORS(app)

    db_uri = "mongodb+srv://PathPalAdmin:YOAybG23XVTqQnri@cluster0.b6yu9ji.mongodb.net/pathpal?retryWrites=true&w=majority&directConnection=true"
    app.config["MONGO_URI"] = db_uri

    # app.config['MONGODB_SETTINGS'] = {
    #     'db': 'pathpal',
    #     'host': 'cluster0.b6yu9ji.mongodb.net',
    #     'username': 'PathPalAdmin',
    #     'password': 'YOAybG23XVTqQnri',
    #     'retryWrites': True,
    #     'w': 'majority'
    # }

    init_exts(app=app)

    return app
