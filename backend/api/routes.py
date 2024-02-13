from .exts import api
from flask import jsonify,request
from flask_restx import Resource, fields

from .models import Route

route_model = api.model('RouteModel', {"rId": fields.Integer(required=True)})

# test for login
@api.route('/api/login/')
class Login(Resource):
    def post(self):
        data = request.json
        return {'message': data}, 200
    
# test for sign-up
@api.route('/api/sign-up/')
class SignUp(Resource):
    def post(self):
        data = request.json
        return {'message': data}, 200


@api.route('/api/user/')
class User(Resource):
    pass


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
                "startpoint":route.startPoint,
                "msg": "Route is found"}, 200