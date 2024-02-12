from flask_restx import Api
from flask_mongoengine import MongoEngine

db = MongoEngine()
api = Api(version="1.0", title="Users API")

def init_exts(app):
    # initial database
    # db.init_app(app=app)

    # initial restfulapi
    api.init_app(app=app)