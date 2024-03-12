# /api/routes.py
# import json
from flask import current_app, request
from flask_restx import Resource, fields, reqparse
from .exts import api
from .models import Route, User

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
    "hours": fields.Integer(required=True),
    "minutes": fields.Integer(required=True),
    "difficulty": fields.String(required=True, min_length=2, max_length=32),
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

# Define API model for route search
search_model = api.model('SearchModel', {
    "city": fields.String(min_length=2, max_length=32),
    "location": fields.String(min_length=2, max_length=32),
    "difficulty": fields.String(min_length=2, max_length=32),
    "comment": fields.String(min_length=2, max_length=200),
    "creator_username": fields.String(min_length=2, max_length=50),
    "distance": fields.Float(),
    "hours": fields.Integer(),
    "minutes": fields.Integer()
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

        try:
            user = User.get_by_username(req_data.get("username"))  # Fetch route by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            new_route = Route(**req_data) # Create a new route
            new_route.save()
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


# Define a Resource for route search
@api.route('/api/searchroute/')
class SearchRoute(Resource):
    @api.expect(search_model, validate=True)
    def post(self):
        # Parse request data
        parser = reqparse.RequestParser()
        parser.add_argument('city', type=str, help='City name')
        parser.add_argument('location', type=str, help='Location name')
        parser.add_argument('difficulty', type=str, help='Difficulty level')
        parser.add_argument('comment', type=str, help='Comments')
        parser.add_argument('creator_username', type=str, help='Creator of the route username')
        parser.add_argument('distance', type=float, help='Distance')
        parser.add_argument('hours', type=int, help='Hours')
        parser.add_argument('minutes', type=int, help='Minutes')
        parser.add_argument('map_center_lat', type=float, help='Latitude of the map center')
        parser.add_argument('map_center_lng', type=float, help='Longitude of the map center')
        args = parser.parse_args()

        # Convert hours and minutes to total minutes
        total_minutes = 0
        if args['hours']:
            total_minutes += args['hours'] * 60
        if args['minutes']:
            total_minutes += args['minutes']

        # Build the query based on the provided parameters
        query_params = {}
        if args['city']:
            query_params['city__icontains'] = args['city']
        if args['location']:
            query_params['location__icontains'] = args['location']
        if args['difficulty']:
            query_params['difficulty__icontains'] = args['difficulty']
        if args['comment']:
            query_params['comment__icontains'] = args['comment']
        if args['creator_username']:
            query_params['creator_username'] = args['creator_username']
        if args['distance']:
            query_params['distance__gte'] = args['distance']
        if total_minutes > 0:
            query_params['hour__gte'] = total_minutes
        if args['map_center_lat'] and args['map_center_lng']:
            query_params['map_center__lat'] = args['map_center_lat']
            query_params['map_center__lng'] = args['map_center_lng']

        # Execute the query and sort by likes and saves
        try:
            routes = Route.objects(**query_params).order_by('-like', '-saves')
        except Exception as e:
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 500

        # Convert routes to dictionary format
        result = []
        for route in routes:
            result.append(route.toDICT())

        return {"success": True, "routes": result, "msg": "Routes retrieved successfully"}, 200


# Define a Resource for searching users
@api.route('/api/searchuser/')
class SearchUser(Resource):
    @api.expect(user_search_model, validate=True)
    def post(self):
        # Parse request data
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('email', type=str, help='Email address')
        args = parser.parse_args()

        # Build the query based on the provided parameters
        query_params = {}
        if args['username']:
            query_params['username__icontains'] = args['username']
        if args['email']:
            query_params['email__icontains'] = args['email']

        # Execute the query
        try:
            users = User.objects(**query_params)
        except Exception as e:
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 500

        # Convert users to dictionary format
        result = []
        for user in users:
            result.append({
                "username": user.username,
                "email": user.email,
                # Add other user attributes as needed
            })

        return {"success": True, "users": result, "msg": "Users retrieved successfully"}, 200
