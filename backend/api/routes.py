from .exts import api
from flask import jsonify, request
from flask_restx import Resource, fields

from .models import *

route_model = api.model('RouteModel', {"rId": fields.Integer(required=True)})
signup_model = api.model('SignUpModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                         "email": fields.String(required=True, min_length=4, max_length=64),
                                         "password": fields.String(required=True, min_length=4, max_length=16)
                                         })

login_model = api.model('LoginModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                       "password": fields.String(required=True, min_length=4, max_length=16)
                                       })


@api.route('/api/data/')
class Data(Resource):
    def get(self):
        return {'message': 'test from Flask'}


@api.route('/api/user/check-login-status')
class UserStatus(Resource):
    def get(self):
        return {'message': 'test from UserStatus'}


@api.route('/api/user/sign-up')
class UserSignUp(Resource):
    @api.expect(signup_model, validate=True)
    def post(self):
        return {'message': 'test from UserSignUp'}


# @api.route('/api/user/login')
# class UserLogin(Resource):
#     @api.expect(login_model, validate=True)
#     def post(self):
#         req_data = request.get_json()
#         _username = req_data.get("username")
#         _password = req_data.get("password")
#
#         user = User.objects(pk=_username).first()
#
#         if user is None:
#             return {"success": False,
#                     "msg": "User not exist"}, 400
#         if _password != user.password:
#             return {"success": False,
#                     "msg": "Wrong credentials."}, 400
#
#         # return {"success": True,
#         #         "startpoint": route.startPoint,
#         #         "msg": "Route is found"}, 200
#         #
#
#         # # create access token uwing JWT
#         # token = jwt.encode({'email': _username, 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)
#         #
#         # user_exists.set_jwt_auth_active(True)
#         # user_exists.save()
#         #
#         # return {"success": True,
#         #         "token": token,
#         #         "user": user_exists.toJSON()}, 200
#
#         return {'message': 'test from UserLogin'}


@api.route('/api/route/draw')
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