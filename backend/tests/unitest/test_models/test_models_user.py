import pytest
from pathlib import Path
from backend.api.models import User, Route
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/user_model_data.yaml"
test_cases = load_test_data(yaml_file_path)

user_create = test_cases['user_create']
user_password = test_cases['user_password']
user_routes = test_cases['user_routes']


class TestUser:

    def test_get_create_routes(user_and_route):
        user, route = user_and_route
        user.add_create_routes(route)
        assert len(user.get_create_routes()) == 1
        assert user.get_create_routes()[0]['name'] == "Test Route"

    def test_get_create_routes_id(user_and_route):
        user, route = user_and_route
        user.add_create_routes(route)
        assert len(user.get_create_routes_id()) == 1
        assert user.get_create_routes_id()[0] == str(route.id)

    def test_get_saved_routes(user_and_route):
        user, route = user_and_route
        user.add_saved_routes(route)
        assert len(user.get_saved_routes()) == 1
        assert user.get_saved_routes()[0]['name'] == "Test Route"

    def test_add_create_routes(user_and_route):
        user, _ = user_and_route
        new_route = Route(name="New Route", creator_username=user.username)
        new_route.save()
        user.add_create_routes(new_route)
        assert new_route in user.create_routes

    def test_add_saved_routes(user_and_route):
        user, _ = user_and_route
        new_route = Route(name="New Saved Route", creator_username=user.username)
        new_route.save()
        user.add_saved_routes(new_route)
        assert new_route in user.saved_routes

    def test_get_by_username(user_and_route):
        user, _ = user_and_route
        retrieved_user = User.get_by_username(user.username)
        assert retrieved_user is not None
        assert retrieved_user.username == user.username

        # Test for a non-existent user
        assert User.get_by_username("non_existent_user") is None
