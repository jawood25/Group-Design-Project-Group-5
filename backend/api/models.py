# /api/models.py
import datetime
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
    city = db.StringField()
    location = db.StringField()
    hour = db.IntField()
    min = db.IntField()
    difficulty = db.StringField()
    desc = db.StringField()

    dislike = db.IntField(default=0)
    like = db.IntField(default=0)
    saves = db.IntField(default=0)
    distance = db.FloatField(default=0.0)
    creator_username = db.StringField(required=True)
    comment = db.ReferenceField(Comment, reverse_delete_rule='PULL')

    # Returns a string representation of the Route instance
    def __repr__(self):
        return f"Route {self.id}"

    # Class method to retrieve a route by its ID
    @classmethod
    def get_by_rid(cls, rid):
        return cls.objects(id=rid).first()

    def toDICT(self):
        cls_dict = {}
        cls_dict['coordinates'] = self.coordinates
        cls_dict['city'] = self.city
        cls_dict['location'] = self.location
        cls_dict['hours'] = self.hour
        cls_dict['minutes'] = self.min
        cls_dict['difficulty'] = self.difficulty
        cls_dict['desc'] = self.desc
        cls_dict['dislike'] = self.dislike
        cls_dict['like'] = self.like
        cls_dict['saves'] = self.saves
        cls_dict['distance'] = self.distance
        cls_dict['creator_username'] = self.creator_username

        return cls_dict


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
