# test_models/conftest.py
import pytest
from backend.api.models import User


@pytest.fixture(scope='class', autouse=True)
def add_user():
    user_info = {"username": "testuser", "password": "testpassword"}
    user = User(username="testuser")
    user.password = "testpassword"
    user.save()
    added_user = User.objects(username=user_info['username']).first()
    assert added_user is not None, "User should be added to the database"
    assert added_user.username == user_info['username'],\
        "Added user should have the correct username"
    yield
