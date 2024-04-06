from pathlib import Path

import pytest

from backend.api.models import User, Route, SharedRoute, SharedEvent
from backend.utils.file.yaml_op import load_data


def create_test_user(test_case):
    user = User(username=test_case.get('username', "testuser"), password="TestPassword")
    user.save()
    return user


def gen_routes(user, expected_num):
    routes = []
    for i in range(expected_num):
        new_route = Route(creator_username=user.username)
        new_route.save()
        routes.append(new_route)
    return routes


def create_test_routes(user, expected_routes):
    routes = gen_routes(user, expected_routes)
    for route in routes:
        user.create_routes.append(route)
    user.save()


def save_test_routes(user, expected_routes):
    routes = gen_routes(user, expected_routes)
    for route in routes:
        user.saved_routes.append(route)
    user.save()


def add_shared_routes(user, expected_shared_routes):
    for route in expected_shared_routes:
        user.add_shared_route(route['route'], route['shared_by'])
    user.save()


def add_shared_events(user, expected_shared_events):
    for event in expected_shared_events:
        user.add_shared_event(event['event'], event['shared_by'])
    user.save()


def gen_shared_routes(user, expected_num):
    for i in range(expected_num):
        user.add_shared_route("SharedRouteID", user.username)
    user.save()
    if expected_num == 1:
        return SharedRoute(route="SharedRouteID", shared_by=user.username)


def gen_shared_events(user, expected_num):
    for i in range(expected_num):
        user.add_shared_event("SharedEventID", user.username)
    user.save()
    if expected_num == 1:
        return SharedEvent(event="SharedEventID", shared_by=user.username)


def create_friend(user, test_case):
    for friend in test_case['expected_friends']:
        new_friend = User(username=friend['username'], password="FriendPassword", name=friend['name'])
        new_friend.save()
        user.add_friend(new_friend)


@pytest.mark.parametrize("test_case", load_data(Path(__file__).parent / "data/test_user.yaml"))
def test_user_methods(test_client, test_case):
    user = create_test_user(test_case)
    method = test_case['method']
    try:
        if test_case['method'] == "__repr__":
            assert user.__repr__() == test_case['expected_repr'], "__repr__ method output mismatch."
        if method == "password":
            user = User(username="testUser", password="initialPass")
            user.password = test_case['new_password']
            assert user.check_password(test_case['check_password']) == test_case[
                'expected_result'], "Password method failed."
            with pytest.raises(AttributeError) as excinfo:
                _ = user.password
            assert str(
                excinfo.value) == "not a readable attribute", "Password property read did not raise expected AttributeError."
        elif method == "add_create_routes":
            new_route = Route(creator_username=user.username)
            new_route.save()
            user.add_create_routes(new_route)
            assert new_route in user.create_routes, "Route not added correctly."
        elif method == "remove_created_route":
            new_route = Route(creator_username=user.username)
            new_route.save()
            user.add_create_routes(new_route)
            user.remove_created_route(new_route)
            user.save()
            assert new_route not in user.create_routes, "Route not removed correctly."
        elif method == "get_created_routes":
            create_test_routes(user=user, expected_routes=test_case['expected_routes_num'])
            if test_case.get('include_invalid_shared_route', False):
                user.create_routes.append(object())  # Add invalid shared route
            assert len(user.get_created_routes()) == test_case[
                'expected_routes_num'], "Failed to retrieve created routes correctly."
        elif method == "get_created_routes_id":
            create_test_routes(user=user, expected_routes=test_case['expected_routes_num'])
            if test_case.get('include_invalid_shared_route', False):
                user.create_routes.append(object())  # Add invalid shared route
            assert len(user.get_created_routes_id()) == test_case[
                'expected_routes_num'], "Failed to retrieve created routes correctly."
        elif method == "add_saved_routes":
            route_to_save = Route(creator_username=user.username)
            route_to_save.save()
            if not test_case.get('expected_success', True):
                user.add_saved_routes(route_to_save)
            success = user.add_saved_routes(route_to_save)
            assert success == test_case['expected_success'], "Route not saved correctly."
        elif method == "remove_saved_route":
            new_route = Route(creator_username=user.username)
            new_route.save()
            user.add_saved_routes(new_route)
            user.remove_saved_route(new_route)
            user.save()
            assert new_route not in user.saved_routes, "Route not removed correctly."
        elif method == "get_saved_routes":
            save_test_routes(user=user, expected_routes=test_case['expected_routes_num'])
            if test_case.get('include_invalid_shared_route', False):
                user.saved_routes.append(object())  # Add invalid shared route
            assert len(user.get_saved_routes()) == test_case[
                'expected_routes_num'], "Failed to retrieve saved routes correctly."
        elif method == "get_saved_routes_id":
            save_test_routes(user=user, expected_routes=test_case['expected_routes_num'])
            if test_case.get('include_invalid_shared_route', False):
                user.saved_routes.append(object())  # Add invalid shared route
            assert len(user.get_saved_routes_id()) == test_case[
                'expected_routes_num'], "Failed to retrieve saved routes correctly."
        elif method == "add_shared_route":
            if not test_case.get('expected_success', True):
                gen_shared_routes(user=user, expected_num=1)
            success = user.add_shared_route(route="SharedRouteID", shared_by=user.username)
            assert success == test_case['expected_success'], "Shared route not added correctly."
        elif method == "get_shared_routes":
            add_shared_routes(user=user, expected_shared_routes=test_case['expected_shared_routes'])
            if test_case.get('include_invalid_shared_route', False):
                user.shared_routes.append(object())  # Add invalid shared route
            assert len(user.get_shared_routes()) == len(
                test_case['expected_shared_routes']), "Failed to retrieve shared routes correctly."
        elif method == "add_friend":
            new_friend = User(username="NewFriend", password="FriendPassword")
            new_friend.save()
            user.add_friend(new_friend)
            assert new_friend in user.friends, "Friend not added correctly."
        elif method == "delete_friend":
            new_friend = User(username="NewFriend", password="FriendPassword")
            new_friend.save()
            user.add_friend(new_friend)
            user.delete_friend(new_friend)
            user.save()
            assert new_friend not in user.friends, "Friend not removed correctly."
        elif method == "get_friends":
            create_friend(user, test_case)
            assert len(user.get_friends()) == len(
                test_case['expected_friends']), "Failed to retrieve friends correctly."
        elif method == "add_shared_event":
            gen_shared_events(user=user, expected_num=1)
            assert any(sr.event == "SharedEventID" for sr in user.shared_events), "Shared route not added correctly."
        elif method == "get_shared_events":
            add_shared_events(user=user, expected_shared_events=test_case['expected_shared_events'])
            if test_case.get('include_invalid_shared_event', False):
                user.shared_events.append(object())
            assert len(user.get_shared_events()) == len(
                test_case['expected_shared_events']), "Failed to retrieve shared events correctly."
        elif method == "search_user":
            found_users = User.search_user(test_case['search_params'])
            assert len(found_users) == test_case['expected_count'], "User search returned incorrect number of users."
        elif method == "get_by_username":
            found_user = User.get_by_username(test_case['username'])
            assert found_user is not None and found_user.username == test_case[
                'username'], "Failed to retrieve user by username."
        elif method == "toDICT":
            user_dict = user.toDICT()
            expected_dict = test_case['expected_dict']
            assert user_dict == expected_dict, "User dictionary does not match expected."

    except Exception as e:
        pytest.fail(f"Unexpected error occurred: {e}")
