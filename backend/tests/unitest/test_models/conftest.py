# # test_models/conftest.py
import pytest
from mongoengine.connection import get_db


# Fixture to record data state before the test and clear only the data added during the test
@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown_data():
    # Connect to MongoDB using the provided information
    # connect(db=DB_NAME, username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)
    # client = MongoClient(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD)
    # db = client[DB_NAME]
    db = get_db()

    # Record the state of the data before the test starts
    pre_test_data = {}
    for collection in db.list_collection_names():
        pre_test_data[collection] = set(db[collection].find().distinct('_id'))

    yield

    # After the test, delete only the data that was added during the test
    for collection in db.list_collection_names():
        current_data = set(db[collection].find().distinct('_id'))
        added_data = current_data - pre_test_data.get(collection, set())
        for data_id in added_data:
            db[collection].delete_one({'_id': data_id})

    # client.close()
