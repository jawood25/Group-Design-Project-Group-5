# unittest/conftest.py
import pytest
from mongoengine.connection import get_db

from backend.api import create_app


# provide a test client for the application
@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    testing_client = app.test_client()

    with app.app_context():
        yield testing_client


# Fixture to record data state before the test and clear only the data added during the test
@pytest.fixture(scope='class', autouse=True)
def setup_and_teardown_data():
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