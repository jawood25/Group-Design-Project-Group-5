# test_user_getroutes.py
from pathlib import Path
import pytest

from backend.api.models import User, Route
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/user_getroute_data.yaml"
test_cases = load_test_data(yaml_file_path)


# TODO: add a failed test case

@pytest.fixture(scope='class', params=test_cases)
def new_routes(request):
    new_routes = []
    user = User.objects(username=request.param['username']).first()
    if not user:
        # Handle case where user does not exist; possibly create one or skip tests
        pytest.skip("User does not exist")
    for i in range(1, 10):
        new_route = Route(creator_username=user.username)
        new_route.save()
        new_routes.append(new_route)
        user.create_routes.append(new_route)
    user.save()
    return new_routes


@pytest.mark.usefixtures("new_routes")
@pytest.mark.parametrize("test_case", test_cases)
class TestUserGetRoutes:
    def test_get_create_routes(self, test_client, test_case, new_routes):
        # Test adding routes only for cases where user creation is expected to succeed
        if test_case['expected_success']:
            user = User.objects(username=test_case['username']).first()
            routes = user.get_create_routes()
            assert routes == [r.to_json() for r in new_routes], \
                "New routes should be added to the user's created routes."

    def test_get_create_routes_id(self, test_client, test_case, new_routes):
        # Test adding routes only for cases where user creation is expected to succeed
        if test_case['expected_success']:
            user = User.objects(username=test_case['username']).first()
            routes_id = user.get_create_routes_id()
            assert routes_id == [str(r.id) for r in new_routes],\
                "New routes id should be added to the user's created routes."
