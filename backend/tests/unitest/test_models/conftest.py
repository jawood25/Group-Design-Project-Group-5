# test_models/conftest.py
import pytest
from backend.api.models import User, Route


# Create new routes for test user
@pytest.fixture(scope='class', autouse=True)
def n_routes():
    n_routes = []
    user = User.objects(username="testuser").first()
    assert user is not None, "User should be added to the database"
    for _ in range(1, 10):
        new_route = Route(creator_username=user.username)
        n_routes.append(new_route)
        user.create_routes.append(new_route)
        user.save()
    yield n_routes


@pytest.fixture(scope='class', autouse=True)
def add_user():
    user_info = {"username": "testuser", "password": "testpassword"}
    User(username="testuser", password="testpassword")
    added_user = User.objects(username=user_info['username']).first()
    assert added_user is not None, "User should be added to the database"
    assert added_user.username == user_info['username'], \
        "Added user should have the correct username"
    yield
