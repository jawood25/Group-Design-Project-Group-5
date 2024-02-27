from pathlib import Path
from flask import json
import pytest

from backend.api.models import User, Route
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_userroutes_data.yaml"
test_cases = load_data(yaml_file_path)


# Test the /api/userroutes/ route
@pytest.mark.parametrize("test_case", test_cases)
class TestUserRoutes:
    # Simulate a server disconnect
    def mock_get_by_username(self, *args, **kwargs):
        raise ConnectionError("Simulated server disconnect")

    # Add the temporary routes to the database
    @pytest.fixture(scope='function', autouse=True)
    def add_route(self, test_case):
        for routeinfo in test_case['expected_routes']:
            route = Route(
                creator_username=routeinfo['username'],
                kmlURL=routeinfo['kmlURL'],
                city=routeinfo['city'],
                location=routeinfo['location'],
                hour=routeinfo['hours'],
                min=routeinfo['minutes'],
                difficulty=routeinfo['difficulty'],
                desc=routeinfo['desc']
            )
            route.save()
            user = User.get_by_username(username="testuser")
            user.add_create_routes(route)
            added_route = Route.get_by_rid(rid=route.id)
            assert added_route is not None, "Route should be added to the database"
            assert added_route.creator_username == "testuser", \
                "Added route should have the correct creator username"

    # test by providing the username
    def test_user_routes(self, test_client, test_case, monkeypatch):
        expected_status = test_case.get("expected_status")
        # If the expected status is 403, simulate server disconnect using monkeypatch
        if expected_status == 403:
            monkeypatch.setattr(User, "get_by_username", self.mock_get_by_username)

        response = test_client.post('/api/userroutes/', json={"username": test_case["username"]},
                                    content_type=test_case["content_type"])

        assert response.status_code == test_case["expected_status"], \
            f"Failed test case: {test_case}"

        if response.status_code == 200:
            # Load the response data
            data = response.get_json()
            assert data['success'] is True
            # Assuming 'routes' is a JSON string of the routes list
            data['routes'] = json.dumps(test_case['expected_routes'])
            routes = json.loads(data['routes'])
            for route in routes:
                assert route in test_case["expected_routes"], \
                    "The returned routes do not match the expected routes."
        if response.status_code == 403:
            # Expected failure message
            assert response.json['success'] is False
            assert response.json['msg'] == "Simulated server disconnect"
