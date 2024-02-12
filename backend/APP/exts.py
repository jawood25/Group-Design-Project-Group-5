from flask_pymongo import PyMongo
from flask_restful import Api

db = PyMongo()
api = Api()

def init_exts(app):
    # initial database
    # db.init_app(app=app)

    # initial restfulapi
    api.init_app(app=app)