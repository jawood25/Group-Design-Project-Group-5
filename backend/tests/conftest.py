# units/conftest.py
import pytest
import logging
from backend.api import create_app
from mongoengine.connection import get_db
from backend.api.models import User


@pytest.fixture(scope='session', autouse=True)
def disable_logging():
    logging.getLogger('api').setLevel(logging.CRITICAL)
    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)


@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    testing_client = app.test_client()

    with app.app_context():
        yield testing_client


@pytest.fixture(scope='class', autouse=True)
def add_user():
    user_info = {"username": "testuser", "password": "testpassword"}
    user = User(username="testuser")
    user.password = "testpassword"
    user.save()
    added_user = User.get_by_username(username=user_info['username'])
    assert added_user is not None, "User should be added to the database"
    assert added_user.username == user_info['username'], "Added user should have the correct username"
    yield


@pytest.fixture(scope='class', autouse=True)
def clear_data():
    yield
    db = get_db()
    for collection in db.list_collection_names():
        db.drop_collection(collection)
