from flask import request
from flask_restx import Resource, fields
from mongoengine.errors import ValidationError, NotUniqueError
from .exts import api
from .models import Route, User


# Define API models for data validation and documentation
# need JSON data
route_model = api.model('RouteModel', {
    "rid": fields.Integer(required=True)  # Model for route fetching, requires a route ID
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
@api.route('/api/testdb/')
class DbTest(Resource):
    def get(self):
        # Example method to test database by adding a test user
        _username = "test31"
        _password = "testpassword"
        user = User.get_by_username(_username)
        if user:
            return {"success": False, "msg": "User exist"}, 400
        new_user = User(username=_username)
        new_user.set_password(_password)
        new_user.save()
        return {'msg': 'add to db'},200

# Define a Resource to check user login status (example implementation)
@api.route('/api/check-login-status/')
class UserStatus(Resource):
    def get(self):
        return {'message': 'test from UserStatus'}

# Define a Resource for user sign-up
@api.route('/api/sign-up/', methods=['POST'])
class UserSignUp(Resource):
    @api.expect(signup_model, validate=True)  # Expecting data matching the signup_model
    def post(self):
        req_data = request.get_json()  # Extract JSON data from the request
        _username = req_data.get("username")
        _password = req_data.get("password")

        try:
            user = User.get_by_username(_username)  # Check if user already exists
            if user:
                return {"success": False, "msg": "User exist"}, 400
            new_user = User(username=_username)  # Create new user if not exist
            new_user.set_password(_password)
            new_user.save()  # Save the new user to the database
        except ValidationError as ve:
            # handle data validation errors
            return {"success": False, "msg": str(ve)}, 401
        except NotUniqueError as nue:
            # handle non-unique error
            return {"success": False, "msg": "This username is already taken"}, 401
        except Exception as e:
            # catch all other exceptions
            return {"success": False, "msg": "An unexpected error occurred"}, 401

        return {"success": True,"username": user.username,
                "msg": "User was successfully registered"}, 200

# Define a Resource for user login
@api.route('/api/login/',methods=['POST'])
class UserLogin(Resource):
    @api.expect(login_model, validate=True)  # Expecting data matching the login_model
    def post(self):
        req_data = request.get_json()
        _username = req_data.get("username")
        _password = req_data.get("password")

        try:
            user = User.get_by_username(_username)  # Fetch user by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            if not user.check_password(_password):
                # If user not found or password mismatch
                return {"success": False, "msg": "Wrong credentials."}, 400
        except Exception as e:
            return {"success": False, "msg": str(e)}, 403

        # Successful login response
        return {"success": True,"username": user.username,
                "msg": "User was successfully logined"}, 200

# Define a Resource to draw/fetch a route
@api.route('/api/draw/')
class DrawRoute(Resource):
    @api.expect(route_model, validate=True)  # Expecting data matching the route_model
    def get(self):
        req_data = request.get_json()
        _rid = req_data.get("rid")
        route = Route.get_by_id(_rid)  # Fetch route by ID
        if not route:
            return {"success": False, "msg": "Route not exist"}, 400

        return {"success": True, "startpoint": route.startPoint,
                "msg": "Route is found"}, 200
