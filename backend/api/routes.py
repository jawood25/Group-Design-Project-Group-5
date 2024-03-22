# /api/routes.py
# import json
from flask import current_app, request
from flask_restx import Resource, fields, reqparse
from .exts import api
from .models import Route, User, Comment, Event
import math

# Define API model for user search
user_search_model = api.model('UserSearchModel', {
    "username": fields.String(min_length=2, max_length=32),
    "email": fields.String(min_length=6, max_length=50)
})

# Define API models for validating and documenting incoming data
uploadroute_model = api.model('UploadRouteModel', {
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
    "comment": fields.String(max_length=200)
})

editroute_model = api.model('EditRouteModel', {
    # Model for route upload, includes various route details
    "route_id": fields.String(required=True, min_length=2, max_length=32),
    "username": fields.String(min_length=2, max_length=32),
    "coordinates": fields.List(fields.List(fields.Float, min_items=2, max_items=2, required=True)),
    "mapCenter": fields.Nested(api.model('MapCenterModel', {
        "lat": fields.Float(required=True),
        "lng": fields.Float(required=True)
    })),
    "city": fields.String(min_length=2, max_length=32),
    "location": fields.String(min_length=2, max_length=32),
    "difficulty": fields.String(min_length=2, max_length=32),
    "mobility": fields.String(min_length=2, max_length=6),
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

savedroutes_model = api.model('SavedRoutesModel', {
    # Model for fetching saved routes
    "username": fields.String(required=True, min_length=2, max_length=32),
})

addingcomment_model = api.model('AddingCommentModel', {
    # Model for adding comments
    "route_id": fields.String(required=True, min_length=2, max_length=32),
    "body": fields.String(required=True, min_length=2, max_length=200),
    "author": fields.String(required=True, min_length=2, max_length=32)
})

routescomment_model = api.model('RoutesCommentModel', {
    # Model for fetching comments
    "route_id": fields.String(required=True, min_length=2, max_length=32),
})

addingfriend_model = api.model('AddingFriendModel', {
    # Model for adding comments
    "username": fields.String(required=True, min_length=2, max_length=32),
    "friend_username": fields.String(required=True, min_length=2, max_length=32)
})

usersfriend_model = api.model('UsersFriendModel', {
    # Model for fetching comments
    "username": fields.String(required=True, min_length=2, max_length=32),
})

uploadevent_model = api.model('UploadEventModel', {
    # Model for route upload, includes various route details
    "hostname": fields.String(required=True, min_length=2, max_length=32),
    "name": fields.String(required=True, min_length=2, max_length=32),
    "interested": fields.Integer(default=0),
    "venue": fields.String(required=True, min_length=2, max_length=32),
    "date": fields.String(required=True, min_length=2, max_length=32),
    "route_id": fields.String(required=True, min_length=2, max_length=32)
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
@api.route('/api/sign-up/')
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
@api.route('/api/login/')
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
    @api.expect(uploadroute_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _username = req_data.get("username")

        # Create a new route with the provided details
        try:
            user = User.get_by_username(_username)  # Fetch route by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            new_comment = Comment(body=req_data.get("comment"), author=req_data.get("username"))
            new_route = Route(**req_data)  # Create a new route
            new_route.add_comment(new_comment)
            user.add_create_routes(new_route)
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True, "route_id": str(new_route.id),
                "msg": "Route is created"}, 200


@api.route('/api/editroute/')
class EditRoute(Resource):
    @api.expect(editroute_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _rid = req_data.get("route_id")

        try:
            if Route.update_route(_rid, req_data):
                return {"success": True, "msg": "Route is updated"}, 200
            else:
                return {"success": False, "msg": "Route not exist"}, 401
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

    @api.expect(editroute_model, validate=True)  # Expecting data matching the route_model
    def delete(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _rid = req_data.get("route_id")

        try:
            route = Route.get_by_rid(_rid)
            if route:
                route.delete()
                return {"success": True, "msg": "Route has been deleted"}, 200
            else:
                return {"success": False, "msg": "Route does not exist"}, 401
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403


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
                "msg": "Routes retrieved successfully"}, 200


@api.route('/api/savingroutes/')
class SavingRoute(Resource):
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
            route = Route.get_by_rid(_route_id)
            user.add_saved_routes(route)
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True, "route": str(route.id), "msg": "Route is saved"}, 200


@api.route('/api/savedroutes/')
class SavedRoutes(Resource):
    @api.expect(savedroutes_model, validate=True)  # Expecting data matching the route_model
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

        print(111)
        return {"success": True, "routes": routes,
                "msg": "Routes retrieved successfully"}, 200


@api.route('/api/allUR/')
class AllRoutes(Resource):
    def post(self):
        # Fetch all routes from the database
        try:
            routes = Route.all_routes()
        except Exception as e:
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 500

        return {"success": True, "routes": routes, "msg": "Routes retrieved successfully"}, 200


@api.route('/api/addingcomment/')
class AddComment(Resource):
    @api.expect(addingcomment_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _route_id = req_data.get("route_id")

        # Create a new route with the provided details
        try:
            route = Route.get_by_rid(_route_id)  # Fetch route by username
            if not route:
                return {"success": False, "msg": "Route not exist"}, 401
            new_comment = Comment(**req_data)  # Create a new route
            route.add_comment(new_comment)
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403
        return {"success": True, "comment": str(new_comment.id), "msg": "Comment is created"}, 200


@api.route('/api/routescomment/')
class RoutesComment(Resource):
    @api.expect(routescomment_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _route_id = req_data.get("route_id")

        # Create a new route with the provided details
        try:
            route = Route.get_by_rid(_route_id)  # Fetch route by username
            if not route:
                return {"success": False, "msg": "Route not exist"}, 401
            comments = route.get_comments()
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403
        return {"success": True, "comment": comments, "msg": "Comments retrieved successfully"}, 200


@api.route('/api/addingfriend/')
class AddingFriend(Resource):
    @api.expect(addingfriend_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()

        # Create a new route with the provided details
        try:
            user = User.get_by_username(req_data.get("username"))  # Fetch route by username
            friend = User.get_by_username(req_data.get("friend_username"))  # Fetch route by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            if not friend:
                return {"success": False, "msg": "Friend not exist"}, 401
            if not user.add_friend(friend):
                return {"success": False, "msg": "Friend is already added"}, 402
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403
        return {"success": True, "user": user.username, "msg": "Friend is added"}, 200


@api.route('/api/usersfriends/')
class UsersFriends(Resource):
    @api.expect(usersfriend_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()

        # Create a new route with the provided details
        try:
            user = User.get_by_username(req_data.get("username"))  # Fetch route by username
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            friends = user.get_friends()
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403
        return {"success": True, "friends": friends, "msg": "Friends retrieved successfully"}, 200


@api.route('/api/uploadevent/')
class UploadEvent(Resource):
    @api.expect(uploadevent_model, validate=True)  # Expecting data matching the route_model
    def post(self):
        # Extract JSON data from the request
        req_data = request.get_json()
        _username = req_data.get("hostname")
        _rid = req_data.get("route_id")

        # Create a new route with the provided details
        try:
            user = User.get_by_username(_username)  # Fetch route by username
            route = Route.get_by_rid(_rid)
            if not user:
                return {"success": False, "msg": "User not exist"}, 401
            if not route:
                return {"success": False, "msg": "Route not exist"}, 401
            new_event = Event(**req_data)  # Create a new route
        except Exception as e:
            # catch all other exceptions
            current_app.logger.error(e)
            return {"success": False, "msg": str(e)}, 403

        return {"success": True, "event": new_event.toDICT(),
                "msg": "Route is created"}, 200


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
