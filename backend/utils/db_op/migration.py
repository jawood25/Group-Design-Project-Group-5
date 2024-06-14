from mongoengine import connect, get_db
from pymongo import UpdateOne
from backend.api.models import Comment
from backend.api.config import config

# Retrieve MongoDB configuration from the config file
DB_NAME = "test"
DB_HOST = config['development'].DBHOST
DB_USERNAME = config['development'].DBUSERNAME
DB_PASSWORD = config['development'].DBPASSWORD

# Connect to MongoDB using the provided information
connect(db=DB_NAME, username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)


def migrate_routes():
    db = get_db()  # Get the database instance
    route_collection = db['route']  # Assume your collection name is 'route'

    # Generate update operations
    updates = []
    for r in route_collection.find():
        if 'comment' in r and not isinstance(r['comment'], list):
            # Create and save a Comment object using ORM
            new_comment = Comment(body=r['comment'], author="test").save()

            # Add directly to the database and get ID, or any other logic
            comment_id = new_comment.id

            update = UpdateOne({'_id': r['_id']}, {'$set': {'comment': [str(comment_id)]}})
            updates.append(update)

    # Execute bulk update
    if updates:
        result = route_collection.bulk_write(updates)
        print(f"Modified {result.modified_count} documents.")


def migrate_comments():
    db = get_db()  # Get the database instance
    comment_collection = db['comment']  # Assume your collection name is 'route'

    # Generate update operations
    updates = []
    for c in comment_collection.find():
        if 'username' in c:
            update = UpdateOne({'_id': c['_id']},
                               {'$set': {'author': c['username']}, '$unset': {'username': ''}})
            updates.append(update)
        if 'author_username' in c:
            update = UpdateOne({'_id': c['_id']},
                               {'$set': {'author': c['author_username']},
                                '$unset': {'author_username': ''}})
            updates.append(update)

    # Execute bulk update
    if updates:
        result = comment_collection.bulk_write(updates)
        print(f"Modified {result.modified_count} documents.")


def migrate():
    migrate_routes()
    migrate_comments()
    print('Migration complete')


if __name__ == '__main__':
    migrate()
