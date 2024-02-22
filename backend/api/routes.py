from flask import current_app,request,jsonify
from flask_restx import Resource, fields
from mongoengine.errors import ValidationError, NotUniqueError
from .exts import api
from .models import Route, User

# Define API models for data validation and documentation
# need JSON data
upload_model = api.model('UploadModel', {
    "username": fields.String(required=True, min_length=2, max_length=32),
    "kmlURL" : fields.String(required=True, max_length=100),
    "city": fields.String(required=True, min_length=2, max_length=32),
    "location": fields.String(required=True, min_length=2, max_length=32),
    "hours": fields.Integer(required=True),
    "minutes": fields.Integer(required=True),
    "difficulty": fields.String(required=True, min_length=2, max_length=32),
    "desc": fields.String(required=True, max_length=200)
})
userroutes_model = api.model('UserRoutesModel', {
    "username": fields.String(required=True, min_length=2, max_length=32),
})
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
            new_user.password = _password
            new_user.save()  # Save the new user to the database
        except Exception as e:
            current_app.logger.error(e)
            # catch all other exceptions
            return {"success": False, "msg": str(e)}, 401

        return {"success": True, "username": new_user.username,
                "msg": "User was successfully registered"}, 200

# Define a Resource for user login
@api.route('/api/login/', methods=['POST'])
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
            current_app.logger.error(e)
            # catch all other exceptions
            return {"success": False, "msg": str(e)}, 403

        # Successful login response
        return {"success": True, "username": user.username,
                "msg": "User was successfully logined"}, 200

# Define a Resource to upload a route
@api.route('/api/upload/')
class UploadRoute(Resource):
    @api.expect(upload_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        req_data = request.get_json()
        _username = req_data.get("username")
        _url = req_data.get("kmlURL")
        _city = req_data.get("city")
        _location = req_data.get("location")
        _hours = req_data.get("hours")
        _minutes = req_data.get("minutes")
        _difficulty = req_data.get("difficulty")
        _desc = req_data.get("desc")
        user = User.get_by_username(_username)  # Fetch route by username
        try:
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            new_route = Route(creator_username=_username, kmlURL=_url,
                              city=_city, location=_location, hour=_hours,
                              min=_minutes, difficulty=_difficulty, desc=_desc)
            new_route.save()
            user.add_create_routes(new_route)
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True,"route_id": str(new_route.id),
                "msg": "Route is created"}, 200

@api.route('/api/userroutes/')
class UserRoutes(Resource):
    @api.expect(userroutes_model, validate=True)  # Expecting data matching the route_model
    def post(self):

        req_data = request.get_json()
        _username = req_data.get("username")
        user = User.get_by_username(_username)  # Fetch route by username
        try:
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            routes = user.get_create_routes()
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True, "route_ids": jsonify(routes),
                "msg": "Route is created"}, 200
