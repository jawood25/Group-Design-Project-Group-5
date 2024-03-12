# /api/models.py
import datetime
import math
from werkzeug.security import generate_password_hash, check_password_hash
from .exts import db  # Importing the database instance from an external module


# pylint: disable=no-member
# Defines a Comment document associated with users and their interactions
class Comment(db.Document):
    author_username = db.StringField(required=True)  # pylint: disable=E1101
    date_posted = db.DateTimeField(default=datetime.datetime.utcnow())  # pylint: disable=E1101
    dislikes = db.IntField(default=0)  # pylint: disable=E1101
    likes = db.IntField(default=0)  # pylint: disable=E1101
    body = db.StringField(required=True)


# Defines a Route document for storing information about specific routes
class Route(db.Document):
    coordinates = db.ListField(db.ListField(db.FloatField()))
    map_center = db.DictField(default={"lat": 0.0, "lng": 0.0})
    # mapCenter = db.DictField(default={"lat": 0.0, "lng": 0.0})
    city = db.StringField()
    location = db.StringField()
    hour = db.IntField()
    # hours = db.IntField()
    min = db.IntField()
    # minutes = db.IntField()
    difficulty = db.StringField()
    comment = db.StringField()

    dislike = db.IntField(default=0)
    like = db.IntField(default=0)
    saves = db.IntField(default=0)
    distance = db.FloatField(default=0.0)
    creator_username = db.StringField(required=True)

    # username = db.StringField(required=True)

    # comment = db.ReferenceField(Comment, reverse_delete_rule='PULL')

    def __init__(self, *args, **kwargs):
        if 'mapCenter' in kwargs:
            kwargs['map_center'] = kwargs.pop('mapCenter')
        if 'hours' in kwargs:
            kwargs['hour'] = kwargs.pop('hours')
        if 'minutes' in kwargs:
            kwargs['min'] = kwargs.pop('minutes')
        if 'username' in kwargs:
            kwargs['creator_username'] = kwargs.pop('username')

        super(Route, self).__init__(*args, **kwargs)
        self.set_distance(self.coordinates)

    # Returns a string representation of the Route instance
    def __str__(self):
        return f"Route {self.id}"

    def set_distance(self, coordinates):
        def haversine_distance(coord1, coord2):
            # Coordinates are expected as (latitude, longitude) pairs in decimal degrees
            lat1, lon1 = math.radians(coord1[1]), math.radians(coord1[0])
            lat2, lon2 = math.radians(coord2[1]), math.radians(coord2[0])

            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            # Radius of the Earth in kilometers
            R = 6371.0

            # Calculate the distance
            distance = R * c

            return distance

        total_distance = 0

        # Iterate through the list of coordinates and calculate distance for each consecutive pair
        for i in range(len(coordinates) - 1):
            total_distance += haversine_distance(coordinates[i], coordinates[i + 1])

        self.distance = round(total_distance, 3)

    # Class method to retrieve a route by its ID
    @classmethod
    def get_by_rid(cls, rid):
        return cls.objects(id=rid).first()

    def toDICT(self):
        return {
            'coordinates': self.coordinates,
            'map_center': self.map_center,
            'city': self.city,
            'location': self.location,
            'hours': self.hour,
            'minutes': self.min,
            'difficulty': self.difficulty,
            'comment': self.comment,
            'dislike': self.dislike,
            'like': self.like,
            'saves': self.saves,
            'distance': self.distance,
            'creator_username': self.creator_username
        }


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
    friends = db.ListField(db.ReferenceField('self', reverse_delete_rule='PULL'))

    def __init__(self, *args, **kwargs):
        password = None
        if 'password' in kwargs:
            password = kwargs.pop('password')
        super(User, self).__init__(*args, **kwargs)
        if password:
            self.password = password


    # Returns a string representation of the User instance
    def __str__(self):
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

    # Method to get routes created by the user
    def get_create_routes(self):
        routes = [route.toDICT() for route in self.create_routes]
        return routes

    # Method to get routes' id created by the user
    def get_create_routes_id(self):
        routes = [str(route.id) for route in self.create_routes]
        return routes

    # Method to get routes saved by the user
    # in development
    # def get_saved_routes(self):
    #     routes = [route.to_json() for route in self.saved_routes]
    #     return routes

    # Method to add a route to the user's created routes
    def add_create_routes(self, new_route):
        self.create_routes.append(new_route)
        self.save()

    # Method to add a route to the user's saveed routes
    # in development
    # def add_saved_routes(self, new_route):
    #     self.saved_routes.append(new_route)
    #     self.save()

    # Class method to retrieve a user by their username
    @classmethod
    def get_by_username(cls, username):
        return cls.objects(username=username).first()


"""code for further use"""

# class EventList(Document):
#     number_of_events = db.IntField(default=0)
#     events = db.ListField(db.ReferenceField('Event'))

# pylint: enable=no-member
