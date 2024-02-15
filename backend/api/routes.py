from .exts import api
from flask import jsonify, request
from flask_restx import Resource, fields

from .models import *


# Define API models for data validation and documentation
# need JSON data
route_model = api.model('RouteModel', {
    "rId": fields.Integer(required=True)  # Model for route fetching, requires a route ID
})

# example:
# {
#   "username": "someUsername",
#   "password": "somePassword"
# }
signup_model = api.model('SignUpModel', {
    # Model for user sign-up, requires username and password (email commented out)
    "username": fields.String(required=True, min_length=2, max_length=32),
    "password": fields.String(required=True, min_length=4, max_length=16)
})

login_model = api.model('LoginModel', {
    # Model for user login, requires username and password
    "username": fields.String(required=True, min_length=2, max_length=32),
    "password": fields.String(required=True, min_length=4, max_length=16)
})

# Define a Resource for testing database connectivity
@api.route('/api/testdb')
class dbTest(Resource):
    def get(self):
        # Example method to test database by adding a test user
        _username = "test2"
        _password = "testpassword"
        user = User.objects(username=_username).first()
        if user:
            return {"success": False, "msg": "User exist"}, 400
        User(username=_username,password=_password).save()
        return {'msg': 'add to db'},200

# Define a Resource to check user login status (example implementation)
@api.route('/api/check-login-status/')
class UserStatus(Resource):
    def get(self):
        return {'message': 'test from UserStatus'}

# Define a Resource for user sign-up
@api.route('/api/sign-up/')
class UserSignUp(Resource):
    @api.expect(signup_model, validate=True)  # Expecting data matching the signup_model
    def post(self):
        req_data = request.get_json()  # Extract JSON data from the request

        _username = req_data.get("username")
        _password = req_data.get("password")
        try:
            user = User.objects(username=_username).first()  # Check if user already exists
            if user:
                return {"success": False, "msg": "User exist"}, 400
            new_user = User(username=_username, password=_password)  # Create new user if not exist
            new_user.save()  # Save the new user to the database
        except Exception as e:
            return {"success": False, "msg": str(e)}, 401

        return {"success": True, "userID": str(new_user.id), "msg": "The user was successfully registered"}, 200

# Define a Resource for user login
@api.route('/api/login/')
class UserLogin(Resource):
    @api.expect(login_model, validate=True)  # Expecting data matching the login_model
    def post(self):
        req_data = request.get_json()
        _username = req_data.get("username")
        _password = req_data.get("password")
        #user = User.objects().first()  # Fetch user by username
        try:
            user = User.objects(username=_username).first()  # Fetch user by username
            if user is None:
                return {"success": False, "msg": "User not exist"}, 401
            if _password != user.password:
                # If user not found or password mismatch
                return {"success": False, "msg": "Wrong credentials."}, 400
        except Exception as e:
            return {"success": False, "msg": str(e)}, 403

        # Successful login response
        return {"username": user.username}, 200

# Define a Resource to draw/fetch a route
@api.route('/api/draw/')
class DrawRoute(Resource):
    @api.expect(route_model, validate=True)  # Expecting data matching the route_model
    def get(self):
        req_data = request.get_json()
        _rId = req_data.get("rId")
        route = Route.objects(pk=_rId).first()  # Fetch route by ID
        if route is None:
            return {"success": False, "msg": "Route not exist"}, 400

        return {"success": True, "startpoint": route.startPoint, "msg": "Route is found"}, 200
