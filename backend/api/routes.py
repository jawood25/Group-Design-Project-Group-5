from .exts import api
from flask import jsonify, request
from flask_restx import Resource, fields

from .models import *

route_model = api.model('RouteModel', {"rId": fields.Integer(required=True)})
signup_model = api.model('SignUpModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                         # "email": fields.String(required=True, min_length=4, max_length=64),
                                         "password": fields.String(required=True, min_length=4, max_length=16)
                                         })

login_model = api.model('LoginModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                       "password": fields.String(required=True, min_length=4, max_length=16)
                                       })

@api.route('/api/testdb')
class dbTest(Resource):
    def get(self):
        _username = "test"
        _password = "testpassword"
        new_user = User(username=_username, password=_password)
        new_user.save()
        return {'msg': 'add to db'}

@api.route('/api/check-login-status/')
class UserStatus(Resource):
    def get(self):
        return {'message': 'test from UserStatus'}


@api.route('/api/sign-up/')
class UserSignUp(Resource):
    @api.expect(signup_model, validate=True)
    def post(self):
        req_data = request.get_json()

        _username = req_data.get("username")
        # _email = req_data.get("email")
        _password = req_data.get("password")
        try:
            user = User.objects(pk=_username).first()
            if user:
                return {"success": False,
                        "msg": "User exist"}, 400
            new_user = user(username=_username, password=_password)
            new_user.save()
        except Exception as e:
            return {"success": False,
                    "msg": e}, 401

        return {"success": True,
                "userID": new_user.id,
                "msg": "The user was successfully registered"}, 200


@api.route('/api/login/')
class UserLogin(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        req_data = request.get_json()
        _username = req_data.get("username")
        _password = req_data.get("password")
        try:
            user = User.objects(pk=_username).first()
            if user is None:
                return {"success": False,
                        "msg": "User not exist"}, 400
            if _password != user.password:
                return {"success": False,
                        "msg": "Wrong credentials."}, 401
        except Exception as e:
            return {"success": False,
                    "msg": e}, 403

        return {
            # "token": token,
            "username": user.username}, 200

@api.route('/api/draw/')
class DrawRoute(Resource):
    @api.expect(route_model, validate=True)
    def get(self):
        req_data = request.get_json()
        _rId = req_data.get("rId")
        route = Route.objects(pk=_rId).first()
        if route is None:
            return {"success": False,
                    "msg": "Route not exist"}, 400
        return {"success": True,
                "startpoint": route.startPoint,
                "msg": "Route is found"}, 200
