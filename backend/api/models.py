from datetime import datetime
from .exts import db  # Importing the database instance from an external module


# Defines a User document with various fields to store user information
class User(db.Document):
    # Unique username required for each user
    username = db.StringField(required=True, unique=True)
    # Password field, required for each user
    password = db.StringField(required=True)
    # Optional email field for the user
    email = db.StringField()
    # Optional name field for the user
    name = db.StringField()
    # Optional age field for the user
    age = db.IntField(default=0)
    # Optional phone field, must be unique if provided
    phone = db.IntField(default=0)
    # List of references to other User documents representing friends, auto-updates if a friend is deleted
    friends = db.ListField(db.ReferenceField('self', reverse_delete_rule='PULL'))

    ### code for further use ###

    # email = db.StringField(required=True,primary_key=True)
    # name = db.StringField(required=True)
    # age = db.IntField()
    # phone = db.IntField(unique=True)
    # friends = db.ListField(db.ReferenceField('self', reverse_delete_rule='PULL'))


# Defines a Comment document associated with users and their interactions
class Comment(db.Document):
    # Reference to a User document representing the comment's author, required
    author = db.ReferenceField(User, required=True)
    # Date and time when the comment was posted, defaults to the current UTC time
    date_posted = db.DateTimeField(default=datetime.utcnow)
    # Number of dislikes for the comment, defaults to 0
    dislikes = db.IntField(default=0)
    # Number of likes for the comment, defaults to 0
    likes = db.IntField(default=0)
    # The body of the comment, required
    body = db.StringField(required=True)


# Defines a Route document for storing information about specific routes
class Route(db.Document):
    # Required starting point of the route
    startPoint = db.StringField(required=True)
    # Optional description of the route
    description = db.StringField()
    # Number of dislikes for the route, defaults to 0
    dislike = db.IntField(default=0)
    # Number of likes for the route, defaults to 0
    like = db.IntField(default=0)
    # Number of saves for the route, indicating how many users have saved it, defaults to 0
    saves = db.IntField(default=0)
    # Optional field for the time taken to complete the route
    time_taken = db.IntField()
    # Optional field for the distance of the route
    distance = db.IntField()
    # Reference to the User document of the route's creator, required
    creator = db.ReferenceField(User, required=True)
    # Optional reference to a Comment document, auto-updates if the comment is deleted
    comment = db.ReferenceField(Comment, reverse_delete_rule='PULL')


# Defines a UserEvent document for events created by users
class UserEvent(db.Document):
    # Required name of the event
    name = db.StringField(required=True, )
    # Required host of the event
    host = db.StringField(required=True)
    # Required venue of the event
    venue = db.StringField(required=True)
    # Date and time of the event, defaults to the current UTC time
    date = db.DateTimeField(default=datetime.utcnow)
    # Required reference to a Route document associated with the event
    route = db.ReferenceField(Route, required=True)
    # Number of users interested in the event, defaults to 0
    interested = db.IntField(default=0)


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
