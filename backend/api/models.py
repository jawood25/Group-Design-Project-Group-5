import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .exts import db  # Importing the database instance from an external module


# Defines a Comment document associated with users and their interactions
class Comment(db.Document):
    author_username = db.StringField(required=True)
    date_posted = db.DateTimeField(default=datetime.datetime.utcnow())
    dislikes = db.IntField(default=0)
    likes = db.IntField(default=0)
    body = db.StringField(required=True)


# Defines a Route document for storing information about specific routes
class Route(db.Document):
    kmlURL = db.StringField()
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
#     number_of_events = db.IntField(default=0)
#     events = db.ListField(db.ReferenceField('Event'))
