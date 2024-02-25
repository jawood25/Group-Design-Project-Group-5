# test_user_creation.py
from pathlib import Path
import pytest

from backend.api.models import Route
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/route_creation_data.yaml"
test_cases = load_test_data(yaml_file_path)


@pytest.mark.parametrize("test_case", test_cases)
class TestRouteCreation:
    def test_create_route(self, test_client, test_case):
        try:
            route = Route(creator_username=test_case['username'])
            route.save()
            assert Route.objects(creator_username=test_case['username']).first() is not None
            assert route.__repr__() == f"Route {route.id}"
            assert test_case['expected_success'], "Expected user creation to succeed."
        except Exception as e:
            # If failure is expected, catching an exception is a test pass
            if not test_case['expected_success']:
                assert True, "User creation failed as expected."
            else:
                pytest.fail(f"User creation failed unexpectedly: {e}")
