# pylint: disable=no-member
import math
from pathlib import Path

import pytest

from backend.api.models import Route, Comment, User
from backend.utils.file.yaml_op import load_data


# Auxiliary function to create a route
def create_test_route(test_case):
    route = Route(**test_case['route_data'])
    route.save()
    return route


def create_routes(test_case):
    for _ in range(test_case['expected_routes_count'] - 1):
        create_test_route(test_case)


def create_test_user(test_case):
    user = User(username=test_case.get('username', "testuser"), password="TestPassword")
    user.save()
    return user


@pytest.mark.parametrize("test_case", load_data(Path(__file__).parent / "data/test_route.yaml"))
def test_route_methods(test_client, test_case):
    route = create_test_route(test_case)
    method = test_case['method']
    try:
        if method == "__repr__ and update_distance_and_time":
            assert repr(route) == f"Route {route.id}", "__repr__ method output mismatch."
            assert math.isclose(route.distance, test_case['expected_distance'], rel_tol=1e-3), \
                "Distance calculation mismatch."
            assert route.min == test_case['expected_time'], "Time calculation mismatch."
        elif method == "add_comment":
            comment = Comment(body="Nice route!", author="testuser")
            comment.save()
            route.add_comment(comment)
            assert comment in route.comment, "Comment not added correctly."
        elif method == "get_comments":
            new_comment = Comment(body="Nice route!", author="testuser").save()
            if test_case.get('include_invalid_shared_route', False):
                route.comment.append(object())  # Add invalid shared route
            route.comment.append(new_comment)
            comments = route.get_comments()
            assert isinstance(comments, list) and len(comments) > 0, "Comments retrieval failed."
        elif method == "search_routes":
            found_routes = Route.search_routes(test_case['search_params'])
            assert len(found_routes) == test_case[
                'expected_count'], "Routes search returned incorrect number of routes."
        elif method == "update_route":
            if test_case.get('expected_success', True):
                success, message = Route.update_route(route.id, test_case['update_data'])
                assert success is test_case.get('expected_success', True) \
                       and message == "Route updated successfully", "Route update failed."
            else:
                success, message = Route.update_route(None, test_case['update_data'])
                assert success is test_case['expected_success'], "Unexpected route update success."
        elif method == "delete_route":
            owner = create_test_user(test_case)
            owner.add_shared_route(str(route.id), "testuser")
            owner.add_create_routes(route)
            owner.add_saved_routes(route)
            new_comment = Comment(body="Nice route!", author="testuser").save()
            route.add_comment(new_comment)
            route.delete_route()
            assert Route.objects(id=route.id).first() is None, "Route not deleted correctly."
        elif method == "all_routes":
            create_routes(test_case)
            all_routes = Route.all_routes()
            assert isinstance(all_routes, list) and len(all_routes) > 0,\
                "Failed to retrieve all routes."
        elif method == "get_by_rid":
            found_route = Route.get_by_rid(route.id)
            assert found_route is not None, "Failed to retrieve route by ID."
        elif method == "toDICT":
            route_dict = route.toDICT()
            expected_dict = test_case['expected_dict']
            expected_dict['id'] = str(route.id)
            assert route_dict == expected_dict, "Route dictionary does not match expected."

    except Exception as e:
        pytest.fail(f"Unexpected error occurred: {e}")
