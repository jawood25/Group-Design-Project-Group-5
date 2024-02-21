from flask import request,jsonify
from flask_restx import Resource, fields
from mongoengine.errors import ValidationError, NotUniqueError
from .exts import api
from .models import Route, User

# Define a Resource for testing database connectivity
@api.route('/api/testdb/')
class DbTest(Resource):
    def get(self):
        # Example method to test database by adding a test user
        # _username = "test31"
        # _url = "111"
        # _city = "111"
        # _location = "111"
        # _hours = 111
        # _minutes = 111
        # _difficulty = "111"
        # _desc = "111"
        # user = User.get_by_username(_username)  # Fetch route by username
        route = Route.objects(city="Dublin").first()
        print(route.id)
        # try:
        #
        #     # if not user:
        #     #     return {"success": False, "msg": "User not exist"}, 401
        #     # new_route = Route(creator_username=_username, kmlURL=_url,
        #     #                   city=_city,location=_location, hour=_hours,
        #     #                   min=_minutes, difficulty=_difficulty, desc=_desc)
        #     # new_route.save()
        #     # user.routes.append(new_route)
        #     # user.save()
        # except ValidationError as ve:
        #     # handle data validation errors
        #     return {"success": False, "msg": str(ve)}, 403
        # except NotUniqueError:
        #     # handle non-unique error
        #     return {"success": False, "msg": "This username is already taken"}, 403
        # except Exception as e:
        #     # catch all other exceptions
        #     return {"success": False, "msg": str(e)}, 403

        # return {'msg': 'add to db'}, 200
        return {"success": True, "route_id": str(route.id),
                "msg": "Route is created"}, 200
