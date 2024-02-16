import datetime
from mongoengine import StringField, IntField, ListField, ReferenceField, DateTimeField
from .exts import db  # Importing the database instance from an external module


# Defines a User document with various fields to store user information
class User(db.Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = StringField()
    name = StringField()
    age = IntField(default=0)
    phone = IntField(default=0)
    friends = ListField(ReferenceField('self', reverse_delete_rule='PULL'))

    # Returns a string representation of the User instance
    def __repr__(self):
        return f"User {self.username}"

    # Method to set the password for the user
    def set_password(self, password):
        self.password = password

    # Method to check if the provided password matches the user's password
    def check_password(self, password):
        return self.password == password

    # Class method to retrieve a user by their username
    @classmethod
    def get_by_username(cls, username):
        return cls.objects(username=username).first()

    ### code for further use ###

    # email = StringField(required=True,primary_key=True)
    # name = StringField(required=True)
    # age = IntField()
    # phone = IntField(unique=True)
    # friends = ListField(ReferenceField('self', reverse_delete_rule='PULL'))


# Defines a Comment document associated with users and their interactions
class Comment(db.Document):
    author = ReferenceField(User, required=True)
    date_posted = DateTimeField(default=datetime.datetime.utcnow())
    dislikes = IntField(default=0)
    likes = IntField(default=0)
    body = StringField(required=True)


# Defines a Route document for storing information about specific routes
class Route(db.Document):
    startPoint = StringField(required=True)
    description = StringField()
    dislike = IntField(default=0)
    like = IntField(default=0)
    saves = IntField(default=0)
    time_taken = IntField()
    distance = IntField()
    creator = ReferenceField(User, required=True)
    comment = ReferenceField(Comment, reverse_delete_rule='PULL')

    # Class method to retrieve a route by its ID
    @classmethod
    def get_by_id(cls, id):
        return cls.objects(id=id).first()


# Defines a UserEvent document for events created by users
class UserEvent(db.Document):
    # Required name of the event
    name = StringField(required=True, )
    # Required host of the event
    host = StringField(required=True)
    # Required venue of the event
    venue = StringField(required=True)
    # Date and time of the event, defaults to the current UTC time
    date = DateTimeField(default=datetime.datetime.utcnow())
    # Required reference to a Route document associated with the event
    route = ReferenceField(Route, required=True)
    # Number of users interested in the event, defaults to 0
    interested = IntField(default=0)

### code for further use ###

# class FriendList(Document):
#     number_of_friends = IntField(default=0)
#     friends = ListField(ReferenceField(User))

# class EventList(Document):
#     number_of_events = IntField(default=0)
#     events = ListField(ReferenceField('Event'))
#
# class RouteList(Document):
#     number_of_saved_routes = IntField(default=0)
#     routes = ListField(ReferenceField('Route'))
