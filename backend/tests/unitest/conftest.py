# unittest/conftest.py
import pytest

from backend.api import create_app


# provide a test client for the application
@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    testing_client = app.test_client()

    with app.app_context():
        yield testing_client
