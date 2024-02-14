from datetime import datetime
from .exts import db

class User(db.Document):
    username = db.StringField(required=True,unique=True)
    #email = db.StringField(required=True,primary_key=True)
    #name = db.StringField(required=True)
    password = db.StringField(required=True)

    #age = db.IntField()
    #phone = db.IntField(unique=True)

    #friends = db.ListField(db.ReferenceField('self', reverse_delete_rule='PULL'))

class Comment(db.Document):
    author = db.ReferenceField(User, required=True)

    date_posted = db.DateTimeField(default=datetime.utcnow)

    dislikes = db.IntField(default=0)
    likes = db.IntField(default=0)

    body = db.StringField(required=True)

class Route(db.Document):
    startPoint = db.StringField(required=True)
    description = db.StringField()

    dislike = db.IntField(default=0)
    like = db.IntField(default=0)
    saves = db.IntField(default=0)
    time_taken = db.IntField()
    distance = db.IntField()

    creator = db.ReferenceField(User, required=True)
    comment = db.ReferenceField(Comment, reverse_delete_rule='PULL')

class UserEvent(db.Document):
    name = db.StringField(required=True,)
    host = db.StringField(required=True)
    venue = db.StringField(required=True)

    date = db.DateTimeField(default=datetime.utcnow)

    route = db.ReferenceField(Route,required=True)

    interested = db.IntField(default=0)

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

