from .exts import db

class User(db.Document):
    # unique
    email = db.StringField()
    name = db.StringField()

    age = db.IntField()
    phone = db.IntField()

    friends = db.ListField(db.ReferenceField('self', reverse_delete_rule='PULL'))

class Comment(db.Document):
    pass

class Route(db.Document):
    startPoint = db.StringField(required=True)
    description = db.StringField()

    dislike = db.IntField(default=0)
    like = db.IntField(default=0)
    saves = db.IntField(default=0)
    time_taken = db.IntField()
    distance = db.IntField()

    creator = db.ReferenceField(User)
    # comments = db.ListField(EmbeddedDocumentField('Comment'))
    comment = db.ReferenceField(Comment, reverse_delete_rule='PULL')

class UserEvent(db.Document):
    pass