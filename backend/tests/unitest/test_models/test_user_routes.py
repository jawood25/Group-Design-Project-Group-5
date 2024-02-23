# test_user_routes.py
from pathlib import Path
import pytest

from backend.api.models import User, Route
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/user_route_data.yaml"
test_cases = load_test_data(yaml_file_path)


# TODO: add a failed test case


@pytest.mark.parametrize("test_case", test_cases)
class TestUserRoutes:

    @pytest.fixture(scope='function')
    def new_route(self, test_client, test_case):
        new_route = Route(creator_username=test_case['username'])
        new_route.save()
        return new_route

    def test_add_create_routes(self, test_client, test_case, new_route):
        # Test adding routes only for cases where user creation is expected to succeed
        if test_case['expected_success']:
            user = User.objects(username=test_case['username']).first()
            user.add_create_routes(new_route)
            assert new_route in user.create_routes,\
                "New route should be added to the user's created routes."
