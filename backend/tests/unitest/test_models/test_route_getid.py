#
from pathlib import Path
import pytest

from backend.api.models import Route
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/route_getid_data.yaml"
test_cases = load_test_data(yaml_file_path)


@pytest.mark.parametrize("test_case", test_cases)
class TestRouteGetID:
    def test_get_by_rid(self, test_client, test_case):
        new_route1 = Route(creator_username=test_case['username'])
        new_route1.save()
        new_route2 = Route(creator_username=test_case['username'])
        new_route2.save()
        if test_case['expected_success']:
            route = Route.get_by_rid(new_route1.id)
            assert route is not None, "Route should exist in the database."
            assert route.id == new_route1.id, "Route should have the correct id."
        else:
            route = Route.get_by_rid(new_route2.id)
            assert route.id != new_route1.id, "Route should have the correct id."
