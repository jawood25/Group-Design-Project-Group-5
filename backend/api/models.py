import datetime
from mongoengine import StringField, IntField, ListField, ReferenceField, DateTimeField, FloatField
from werkzeug.security import generate_password_hash, check_password_hash
from .exts import db  # Importing the database instance from an external module


# Defines a Comment document associated with users and their interactions
class Comment(db.Document):
    author_username = StringField(required=True)
    date_posted = DateTimeField(default=datetime.datetime.utcnow())
    dislikes = IntField(default=0)
    likes = IntField(default=0)
    body = StringField(required=True)


# Defines a Route document for storing information about specific routes
class Route(db.Document):
    kmlURL = StringField()
    city = StringField()
    location = StringField()
    hour = IntField()
    min = IntField()
    difficulty = StringField()
    desc = StringField()

    dislike = IntField(default=0)
    like = IntField(default=0)
    saves = IntField(default=0)
    distance = FloatField(default=0.0)
    creator_username = StringField(required=True)
    comment = ReferenceField(Comment, reverse_delete_rule='PULL')

    # Returns a string representation of the Route instance
    def __repr__(self):
        return f"Route {self.id}"

    # Class method to retrieve a route by its ID
    @classmethod
    def get_by_rid(cls, rid):
        return cls.objects(id=rid).first()


# Defines a User document with various fields to store user information
class User(db.Document):
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    email = StringField()
    name = StringField()
    age = IntField(default=0)
    phone = IntField(default=0)
    create_routes = ListField(ReferenceField(Route, reverse_delete_rule='PULL'))
    saved_routes = ListField(ReferenceField(Route, reverse_delete_rule='PULL'))
    friends = ListField(ReferenceField('self', reverse_delete_rule='PULL'))

    # Returns a string representation of the User instance
    def __repr__(self):
        return f"User {self.username}"

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

    def get_create_routes(self):
        routes = [route.to_json() for route in self.create_routes]
        return routes
    def get_create_routes_id(self):
        routes = [str(route.id) for route in self.create_routes]
        return routes


    def get_saved_routes(self):
        routes = [route.to_json() for route in self.saved_routes]
        return routes

    def add_create_routes(self, new_route):
        self.create_routes.append(new_route)
        self.save()

    def add_saved_routes(self, new_route):
        self.saved_routes.append(new_route)
        self.save()

    # Class method to retrieve a user by their username
    @classmethod
    def get_by_username(cls, username):
        return cls.objects(username=username).first()


"""code for further use"""

# class EventList(Document):
#     number_of_events = IntField(default=0)
#     events = ListField(ReferenceField('Event'))
