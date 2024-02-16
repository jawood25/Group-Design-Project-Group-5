import datetime
from mongoengine import StringField,IntField,ListField,ReferenceField, DateTimeField
from .exts import db  # Importing the database instance from an external module

# Defines a User document with various fields to store user information
class User(db.Document):
    # Unique username required for each user
    username = StringField(required=True, unique=True)
    # Password field, required for each user
    password = StringField(required=True)
    # Optional email field for the user
    email = StringField()
    # Optional name field for the user
    name = StringField()
    # Optional age field for the user
    age = IntField(default=0)
    # Optional phone field, must be unique if provided
    phone = IntField(default=0)
    # List of references to other User documents representing friends,
    # auto-updates if a friend is deleted
    friends = ListField(ReferenceField('self', reverse_delete_rule='PULL'))

    ### code for further use ###

    # email = StringField(required=True,primary_key=True)
    # name = StringField(required=True)
    # age = IntField()
    # phone = IntField(unique=True)
    # friends = ListField(ReferenceField('self', reverse_delete_rule='PULL'))


# Defines a Comment document associated with users and their interactions
class Comment(db.Document):
    # Reference to a User document representing the comment's author, required
    author = ReferenceField(User, required=True)
    # Date and time when the comment was posted, defaults to the current UTC time
    date_posted = DateTimeField(default=datetime.datetime.utcnow())
    # Number of dislikes for the comment, defaults to 0
    dislikes = IntField(default=0)
    # Number of likes for the comment, defaults to 0
    likes = IntField(default=0)
    # The body of the comment, required
    body = StringField(required=True)


# Defines a Route document for storing information about specific routes
class Route(db.Document):
    # Required starting point of the route
    startPoint = StringField(required=True)
    # Optional description of the route
    description = StringField()
    # Number of dislikes for the route, defaults to 0
    dislike = IntField(default=0)
    # Number of likes for the route, defaults to 0
    like = IntField(default=0)
    # Number of saves for the route, indicating how many users have saved it, defaults to 0
    saves = IntField(default=0)
    # Optional field for the time taken to complete the route
    time_taken = IntField()
    # Optional field for the distance of the route
    distance = IntField()
    # Reference to the User document of the route's creator, required
    creator = ReferenceField(User, required=True)
    # Optional reference to a Comment document, auto-updates if the comment is deleted
    comment = ReferenceField(Comment, reverse_delete_rule='PULL')


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
