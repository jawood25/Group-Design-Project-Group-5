# /api/models.py
import datetime
import math
from werkzeug.security import generate_password_hash, check_password_hash
from .exts import db  # Importing the database instance from an external module


# pylint: disable=no-member
# Defines a Comment document associated with users and their interactions
class Comment(db.Document):
    author = db.StringField(required=True)  # pylint: disable=E1101
    date_posted = db.DateTimeField(default=datetime.datetime.utcnow())  # pylint: disable=E1101
    dislikes = db.IntField(default=0)  # pylint: disable=E1101
    likes = db.IntField(default=0)  # pylint: disable=E1101
    body = db.StringField(required=True)

    def __init__(self, *args, **kwargs):
        kwargs.pop('route_id', None)
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.author}'s comment"

    def toDICT(self):
        return {
            'author': self.author,
            'date_posted': self.date_posted.strftime('%Y-%m-%dT%H:%M:%S'),
            'dislikes': self.dislikes,
            'likes': self.likes,
            'body': self.body
        }


# Defines a Route document for storing information about specific routes
class Route(db.Document):
    coordinates = db.ListField(db.ListField(db.FloatField()))
    map_center = db.DictField(default={"lat": 0.0, "lng": 0.0})
    city = db.StringField()
    location = db.StringField()
    hour = db.IntField()
    min = db.IntField()
    difficulty = db.StringField()
    mobility = db.StringField()
    dislike = db.IntField(default=0)
    like = db.IntField(default=0)
    saves = db.IntField(default=0)
    distance = db.FloatField(default=0.0)
    creator_username = db.StringField(required=True)
    comment = db.ListField(db.ReferenceField(Comment, reverse_delete_rule='PULL'))

    def __init__(self, *args, **kwargs):
        map_center = kwargs.pop('mapCenter', None)
        if map_center:
            kwargs['map_center'] = map_center
        hours = kwargs.pop('hours', None)
        if hours:
            kwargs['hour'] = hours
        minutes = kwargs.pop('minutes', None)
        if minutes:
            kwargs['min'] = minutes
        username = kwargs.pop('username', None)
        if username:
            kwargs['creator_username'] = username
        super().__init__(*args, **kwargs)
        self.update_distance_and_time()

    def __repr__(self):
        return f"Route {self.id}"

    def update_distance_and_time(self):
        self.cal_distance()
        self.cal_time()

    def cal_time(self):
        speed_map = {"Bike": 20, "Run": 10, "Walk": 5}
        speed = speed_map.get(self.mobility, 10)  # Default speed is 10 km/h
        self.min = round((self.distance / speed) * 60)

    def cal_distance(self):
        def haversine_distance(coord1, coord2):
            lat1, lon1 = map(math.radians, coord1)
            lat2, lon2 = map(math.radians, coord2)
            dlat, dlon = lat2 - lat1, lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            radius = 6371  # Earth radius in kilometers
            return radius * c

        if len(self.coordinates) > 1:
            self.distance = round(sum(haversine_distance(self.coordinates[i], self.coordinates[i + 1])
                                      for i in range(len(self.coordinates) - 1)), 3)

    def add_comment(self, comment):
        self.comment.append(comment)
        self.save()

    def get_comments(self):
        return [comment.toDICT() for comment in self.comment]

    @classmethod
    def search_routes(cls, args):

        # Simplify addition with default values from args
        total_minutes = args.get('minutes', 0)
        distance_margin = args.get('distanceMargin', 0)
        time_margin = args.get('timeMargin', 0)

        # Build the query based on the provided parameters
        query_fields = ['city', 'location', 'difficulty',
                        'mobility', 'comment', 'creator_username'
                        ]
        query_params = {f"{field}__icontains": args[field]
                        for field in query_fields if field in args
                        }

        if 'distance' in args:
            query_params['distance__gte'] = args['distance'] - distance_margin
            query_params['distance__lte'] = args['distance'] + distance_margin
        if total_minutes > 0:
            query_params['min__gte'] = total_minutes - time_margin
            query_params['min__lte'] = total_minutes + time_margin

        if all(k in args for k in ['map_center_lat', 'map_center_lng']):
            query_params['map_center__lat'] = args['map_center_lat']
            query_params['map_center__lng'] = args['map_center_lng']

        targets = Route.objects(**query_params).order_by('-like', '-saves')

        return [target.toDICT() for target in targets]

    @classmethod
    def update_route(cls, route_id, update_data):
        """
        Class method to update route details.

        :param route_id: The ID of the route to be updated.
        :param update_data: A dictionary containing fields to update and their new values.
        :return: The result of the update.
        """
        route = cls.objects(id=route_id).first()
        if not route:
            return False, "Route does not exist"

        for field, value in update_data.items():
            if hasattr(route, field):
                setattr(route, field, value)

        route.save()
        return True, "Route updated successfully"

    def delete_route(self):
        for user in User.objects(saved_routes=self):
            user.update(pull__saved_routes=self)
        for comment in self.comment:
            comment.delete()
        User.get_by_username(self.creator_username).remove_created_route(self)
        self.delete()

    @classmethod
    def all_routes(cls):
        # Fetch all routes
        return [route.toDICT() for route in cls.objects()]

    # Class method to retrieve a route by its ID
    @classmethod
    def get_by_rid(cls, rid):
        return cls.objects(id=rid).first()

    def toDICT(self):
        return {
            'id': str(self.id),
            'coordinates': self.coordinates,
            'map_center': self.map_center,
            'city': self.city,
            'location': self.location,
            'hour': self.hour,
            'minutes': self.min,
            'difficulty': self.difficulty,
            'comment': self.get_comments(),
            'dislike': self.dislike,
            'like': self.like,
            'saves': self.saves,
            'distance': self.distance,
            'mobility': self.mobility,
            'creator_username': self.creator_username
        }


class SharedRoute(db.EmbeddedDocument):
    route = db.StringField(required=True)  # ID of the route shared
    shared_by = db.StringField(required=True)  # Username of the user who shared the route


# Defines a User document with various fields to store user information
class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    email = db.StringField()
    name = db.StringField()
    age = db.IntField(default=0)
    phone = db.IntField(default=0)
    create_routes = db.ListField(db.ReferenceField(Route, reverse_delete_rule='PULL'))
    saved_routes = db.ListField(db.ReferenceField(Route, reverse_delete_rule='PULL'))
    shared_routes = db.ListField(db.EmbeddedDocumentField(SharedRoute))  # Updated to use SharedRoute
    friends = db.ListField(db.ReferenceField('self', reverse_delete_rule='PULL'))

    def __init__(self, *args, **kwargs):
        password = None
        if 'password' in kwargs:
            password = kwargs.pop('password')
        super().__init__(*args, **kwargs)
        if password:
            self.password = password

    # Returns a string representation of the User instance
    def __repr__(self):
        return f"User {self.username}"

    # set password as a write-only attribute
    @property
    def password(self):
        raise AttributeError("not a readable attribute")

    # Method to set the password for the user
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check if the provided password matches the user's password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_create_routes(self, new_route):
        self.create_routes.append(new_route)
        self.save()

    def remove_created_route(self, route):
        self.create_routes.remove(route)
        self.save()

    # Method to get routes created by the user
    def get_created_routes(self):
        return [route.toDICT() for route in self.create_routes]

    # Method to get routes' id created by the user
    def get_created_routes_id(self):
        return [str(route.id) for route in self.create_routes]

    # Method to add a route to the user's saveed routes
    def add_saved_routes(self, route):
        route.saves += 1
        route.save()
        self.saved_routes.append(route)
        self.save()

    def remove_saved_route(self, route):
        route.save -= 1
        route.save()
        self.saved_routes.remove(route)
        self.save()
        return True

    def get_saved_routes(self):
        return [route.toDICT() for route in self.saved_routes]

    # Method to get routes saved by the user
    def get_saved_routes_id(self):
        return [str(route.id) for route in self.saved_routes]

    def add_shared_route(self, route, shared_by):
        self.shared_routes.append(SharedRoute(route=route, shared_by=shared_by))
        self.save()

    def get_shared_routes(self):
        return [{
            'route': shared_route.route,
            'shared_by': shared_route.shared_by
        } for shared_route in self.shared_routes]

    def add_friend(self, friend):
        self.friends.append(friend)
        self.save()
        return True

    def delete_friend(self, friend):
        self.friends.remove(friend)
        self.save()
        return True

    def get_friends_id(self):
        return [str(friend.id) for friend in self.friends]

    def get_friends(self):
        friendinfo = [{
            **friend.toDICT(),  # Unpack the dictionary returned by toDICT.
            'create_routes': friend.get_created_routes_id(),
            'saved_routes': friend.get_saved_routes_id(),
            'friends': friend.get_friends_id()
        } for friend in self.friends]

        return friendinfo

    @classmethod
    def search_user(cls, args):
        # Define the fields that can be searched on
        valid_fields = ['username', 'email']  # Add more fields as needed
        query_params = {f"{field}__icontains": args[field]
                        for field in valid_fields if args.get(field) is not None
                        }

        # Assuming your ORM supports lazy loading, this query won't hit the database until iterated
        users_query = User.objects(**query_params)

        # Use list comprehension for more concise and Pythonic syntax

        return [{"username": user.username, "email": user.email} for user in users_query]

    # Class method to retrieve a user by their username
    @classmethod
    def get_by_username(cls, username):
        return cls.objects(username=username).first()

    def toDICT(self):
        return {
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "age": self.age,
            "phone": self.phone,
            "create_routes": self.get_created_routes(),  # Convert routes to list of IDs
            "saved_routes": self.get_saved_routes(),  # Convert routes to list of IDs
            "friends": self.get_friends(),  # Convert friends to list of IDs
            "shared_routes": self.get_shared_routes()
        }


class Event(db.Document):
    name = db.StringField(required=True)
    venue = db.StringField(required=True)
    interested = db.IntField(default=0)
    date = db.DateTimeField(required=True)
    host = db.ReferenceField(User, reverse_delete_rule='PULL')
    route = db.ReferenceField(Route, reverse_delete_rule='PULL')

    def __init__(self, *args, **kwargs):
        host = kwargs.pop('hostname', None)
        if host:
            kwargs['host'] = User.get_by_username(host)
        rid = kwargs.pop('route_id', None)
        if rid:
            kwargs['route'] = Route.get_by_rid(rid)
        if 'date' in kwargs:
            kwargs['date'] = datetime.datetime.strptime(kwargs['date'], '%Y-%m-%dT%H:%M:%S')
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"Event {self.name}"

    def toDICT(self):
        return {
            'name': self.name,
            'venue': self.venue,
            'interested': self.interested,
            'date': self.date.strftime('%Y-%m-%dT%H:%M:%S'),
            'host': self.host.username,
            'route': self.route.toDICT()
        }
