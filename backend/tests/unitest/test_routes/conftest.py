# test_routes/conftest.py
import pytest
from backend.api.models import User

# Add a user to the database before running the tests
@pytest.fixture(scope='class', autouse=True)
def add_user():
    user_info = {"username": "testuser", "password": "testpassword"}
    # user = User(username="testuser")
    # user.password = "testpassword"
    user = User(**user_info)
    added_user = User.get_by_username(username=user_info['username'])
    assert added_user is not None, "User should be added to the database"
    assert added_user.username == user_info['username'],\
        "Added user should have the correct username"
    yield
