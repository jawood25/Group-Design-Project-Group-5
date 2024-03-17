# /api/routes.py
# import json
from flask import current_app, request
from flask_restx import Resource, fields, reqparse
from .exts import api
from .models import Route, User
import math

# Define API model for user search
user_search_model = api.model('UserSearchModel', {
    "username": fields.String(min_length=2, max_length=32),
    "email": fields.String(min_length=6, max_length=50)
})

# Define API models for validating and documenting incoming data
upload_model = api.model('UploadModel', {
    # Model for route upload, includes various route details
    "username": fields.String(required=True, min_length=2, max_length=32),
    "coordinates": fields.List(fields.List(fields.Float, min_items=2, max_items=2, required=True), required=True),
    "mapCenter": fields.Nested(api.model('MapCenterModel', {
        "lat": fields.Float(required=True),
        "lng": fields.Float(required=True)
    }), required=True),
    "city": fields.String(required=True, min_length=2, max_length=32),
    "location": fields.String(required=True, min_length=2, max_length=32),
    "difficulty": fields.String(required=True, min_length=2, max_length=32),
    "mobility": fields.String(required=True, min_length=2, max_length=6),
    "comment": fields.String(required=True, max_length=200)
})

userroutes_model = api.model('UserRoutesModel', {
    # Model for fetching routes created by a user
    "username": fields.String(required=True, min_length=2, max_length=32),
})

signup_model = api.model('SignUpModel', {
    # Model for user sign-up, includes username and password
    "username": fields.String(required=True, min_length=2, max_length=32),
    "password": fields.String(required=True, min_length=4, max_length=16)
})

login_model = api.model('LoginModel', {
    # Model for user login, includes username and password
    "username": fields.String(required=True, min_length=2, max_length=32),
    "password": fields.String(required=True, min_length=4, max_length=16)
})

savingroutes_model = api.model('SaveRoutesModel', {
    # Model for saving routes
    "username": fields.String(required=True, min_length=2, max_length=32),
    "route_id": fields.String(required=True, min_length=2, max_length=32)
})

savedrouts_model = api.model('SavedRoutesModel', {
    # Model for fetching saved routes
    "username": fields.String(required=True, min_length=2, max_length=32),
})

# Define API model for route search
search_model = api.model('SearchModel', {
    "city": fields.String(min_length=2, max_length=32),
    "location": fields.String(min_length=2, max_length=32),
    "difficulty": fields.String(min_length=2, max_length=32),
    "mobility": fields.String(min_length=2, max_length=6),
    "comment": fields.String(min_length=2, max_length=200),
    "creator_username": fields.String(min_length=2, max_length=50),
    "distance": fields.Float(),
    "distanceMargin": fields.Float(),
    "min": fields.Integer(),
    "timeMargin": fields.Float()
})


# Define a Resource for user sign-up
@api.route('/api/sign-up/', methods=['POST'])
class UserSignUp(Resource):
    @api.expect(signup_model, validate=True)  # Expecting data matching the signup_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()  # Extract JSON data from the request
        _username = req_data.get("username")

        # Create a new user with the provided details
        try:
            user = User.get_by_username(_username)  # Check if user already exists
            if user:
                return {"success": False, "msg": "User exist"}, 405
            new_user = User(**req_data)  # Create a new user
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
        # Extract JSON data from the request
        req_data = request.get_json()
        _username = req_data.get("username")
        _password = req_data.get("password")

        # Check if user exists and password matches
        try:
            user = User.get_by_username(_username)  # Fetch user by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            if not user.check_password(_password):
                # If user not found or password mismatch
                return {"success": False, "msg": "Wrong credentials."}, 405
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
        # Extract JSON data from the request
        req_data = request.get_json()
        _username = req_data.get("username")

        # Create a new route with the provided details
        try:
            user = User.get_by_username(_username)  # Fetch route by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            new_route = Route(**req_data)  # Create a new route
            user.add_create_routes(new_route)
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True, "route_id": str(new_route.id),
                "msg": "Route is created"}, 200


@api.route('/api/userroutes/')
class UserRoutes(Resource):
    @api.expect(userroutes_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _username = req_data.get("username")
        # Fetch routes created by the user
        try:
            user = User.get_by_username(_username)  # Fetch route by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            routes = user.get_create_routes()
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True, "routes": routes,
                "msg": "Route is created"}, 200


@api.route('/api/savingroutes/')
class UploadRoute(Resource):
    @api.expect(savingroutes_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _username = req_data.get("username")
        _route_id = req_data.get("route_id")

        # Create a new route with the provided details
        try:
            user = User.get_by_username(_username)  # Fetch route by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            route = Route.get_by_id(_route_id)
            user.add_saved_routes(route)
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True, "msg": "Route is created"}, 200

@api.route('/api/savedroutes/')
class UserRoutes(Resource):
    @api.expect(savedrouts_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _username = req_data.get("username")
        # Fetch routes created by the user
        try:
            user = User.get_by_username(_username)  # Fetch route by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            routes = user.get_saved_routes()
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True, "routes": routes,
                "msg": "Route is created"}, 200

@api.route('/api/allUR/')
class UserRoutes(Resource):
    def post(self):
        # Fetch all routes from the database
        try:
            routes = Route.all_routes()
        except Exception as e:
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 500

        return {"success": True, "routes": routes, "msg": "Routes retrieved successfully"}, 200


# Define a Resource for route search
@api.route('/api/searchroute/')
class SearchRoute(Resource):
    @api.expect(search_model, validate=True)
    def post(self):
        # Parse request data
        args = api.payload

        # Execute the query and sort by likes and saves
        try:
            routes = Route.search_routes(args)
        except Exception as e:
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 500

        return {"success": True, "routes": routes, "msg": "Routes retrieved successfully"}, 200


# Define a Resource for searching users
@api.route('/api/searchuser/')
class SearchUser(Resource):
    @api.expect(user_search_model, validate=True)
    def post(self):
        # Parse request data
        args = api.payload

        # Execute the query
        try:
            users = User.search_user(args)
        except Exception as e:
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 500

        return {"success": True, "users": users, "msg": "Users retrieved successfully"}, 200
