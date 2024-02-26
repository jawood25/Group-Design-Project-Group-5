# test_user_routes.py
from pathlib import Path
import pytest

from backend.api.models import User, Route
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_user_addroute.yaml"
test_cases = load_data(yaml_file_path)


# TODO: add a failed test case

# Test user routes
@pytest.mark.parametrize("test_case", test_cases)
class TestUserRoutes:
    # adding a route to user
    @pytest.fixture(scope='function')
    def new_route(self, test_client, test_case):
        new_route = Route(creator_username=test_case['username'])
        new_route.save()
        return new_route

    # test by providing new route
    def test_add_create_routes(self, test_client, test_case, new_route):
        # Test adding routes only for cases where user creation is expected to succeed
        if test_case['expected_success']:
            user = User.objects(username=test_case['username']).first()
            user.add_create_routes(new_route)
            assert new_route in user.create_routes, \
                "New route should be added to the user's created routes."
