# test_routes/conftest.py
import pytest
import logging
from backend.api import create_app
from mongoengine.connection import get_db


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
def clear_data():
    yield
    db = get_db()
    for collection in db.list_collection_names():
        db.drop_collection(collection)
