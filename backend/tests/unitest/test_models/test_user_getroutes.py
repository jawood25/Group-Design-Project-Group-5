# test_user_getroutes.py
from pathlib import Path
import pytest

from backend.api.models import User, Route
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_user_getroute.yaml"
test_cases = load_data(yaml_file_path)


class TestUserGetRoutes:
    # Test for retrieving user-created routes

    @pytest.mark.parametrize("test_case", test_cases)
    def test_get_create_routes(self, test_client, test_case, n_routes):
        # Fetch the user object based on the test case
        user = User.objects(username=test_case['username']).first()

        # Retrieve the routes created by the user
        routes = user.get_create_routes()

        if test_case['expected_success']:
            # Verify that the newly added routes are included in the user's list of created routes
            assert routes == [r.to_json() for r in n_routes], \
                "The new routes should be included in the user's list of created routes."
        else:
            # In scenarios where data retrieval is expected to fail, ensure the validation is correct
            routes = []
            assert routes != [r.to_json() for r in n_routes], \
                "The new routes should not be incorrectly listed in the user's created routes when expected to fail."

    # Test for retrieving the IDs of the routes created by the user

    @pytest.mark.parametrize("test_case", test_cases)
    def test_get_create_routes_id(self, test_client, test_case, n_routes):
        # Fetch the user object based on the test case
        user = User.objects(username=test_case['username']).first()

        # Retrieve the IDs of the routes created by the user
        routes_id = user.get_create_routes_id()

        if test_case['expected_success']:
            # Check that the IDs of the newly added routes are correctly included in the user's list of route IDs
            assert routes_id == [str(r.id) for r in n_routes], \
                "The IDs of the new routes should be correctly included in the user's list of route IDs."
        else:
            # Ensure proper handling of cases where route ID retrieval is expected to fail
            routes_id = []
            assert routes_id != [str(r.id) for r in n_routes], \
                "The IDs of the new routes should not be incorrectly included in the user's list of route IDs when expected to fail."
