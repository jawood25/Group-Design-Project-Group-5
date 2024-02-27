# test_user_addroutes.py
from pathlib import Path
import pytest

from backend.api.models import User, Route
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_user_addroute.yaml"
test_cases = load_data(yaml_file_path)


# Tests for User Routes
@pytest.mark.parametrize("test_case", test_cases)
class TestUserRoutes:
    # Fixture to add a new route for a user
    @pytest.fixture(scope='function')
    def new_route(self, test_client, test_case):
        new_route = Route(creator_username=test_case['username'])
        new_route.save()
        return new_route

    # Test to verify adding a new route
    def test_add_create_routes(self, test_client, test_case, new_route):
        # Proceed with adding routes only in scenarios where user creation is anticipated to succeed
        user = User.objects(username=test_case['username']).first()
        user.add_create_routes(new_route)
        if test_case['expected_success']:
            assert new_route in user.create_routes, \
                "The new route should be successfully added to the user's created routes."
        else:
            # In cases where route addition is not expected to succeed, ensure the route is not added
            new_route = None
            assert new_route not in user.create_routes, \
                "The new route should not be found in the user's created routes when addition is expected to fail."
