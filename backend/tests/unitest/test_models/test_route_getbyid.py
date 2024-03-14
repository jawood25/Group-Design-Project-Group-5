# test_route_getbyid.py
from pathlib import Path
import pytest

from backend.api.models import Route
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_route_getbyid.yaml"
test_cases = load_data(yaml_file_path)


# Test get_by_id in route
@pytest.mark.parametrize("test_case", test_cases)
class TestRouteGetID:
    # test by providing new route info
    def test_get_by_rid(self, test_client, test_case):
        new_route1 = Route(creator_username=test_case['username'])
        new_route2 = Route(creator_username=test_case['username'])
        if test_case['expected_success']:
            route = Route.get_by_rid(new_route1.id)
            assert route is not None, "Route should exist in the database."
            assert route.id == new_route1.id, "Route should have the correct id."
        else:
            route = Route.get_by_rid(new_route2.id)
            assert route.id != new_route1.id, "Route should have the correct id."
