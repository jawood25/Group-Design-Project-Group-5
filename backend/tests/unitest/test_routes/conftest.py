# test_routes/conftest.py
import pytest
from werkzeug.security import generate_password_hash, check_password_hash

from backend.api.models import Route, Comment, User, Event, Group


def mock_save(object=None):
    return True


def mock_get_by_rid(route_id):
    if route_id == "nonexistent":
        return None
    elif route_id == "disconnected":
        # Simulating server disconnect scenario
        raise ConnectionError("Simulated server disconnect")
    route = Route()
    route.id = route_id
    route.get_comments = lambda: []
    route.delete_route = lambda: None  # Mock the deletion method
    return route


def mock_get_by_username(username):
    if username == "nonexistent":
        return None
    elif username == "disconnected":
        # Simulating server disconnect scenario
        raise ConnectionError("Simulated server disconnect")

    # Assuming we have a function to check if two users are friends
    def mock_are_friends(user, friend):
        return user.username == "alreadyfriends" and friend.username == "friend1"

    def mock_delete_friend(friend):
        # This function returns True if the friend can be deleted,
        # and False if the friend cannot be found in the user's friend list.
        return friend.username != "undeletablefriend"

    user = User()
    user.username = username
    user.password_hash = generate_password_hash("testpassword")
    user.check_password = lambda password: check_password_hash(user.password_hash, password)
    user.add_friend = lambda friend: not mock_are_friends(user, friend)
    user.delete_friend = lambda friend: mock_delete_friend(friend)
    user.get_friends = lambda: []
    user.add_saved_routes = lambda route: True
    user.remove_saved_route = lambda route: True
    user.get_saved_routes = lambda: []
    user.get_created_routes = lambda: []
    user.toDICT = lambda: {"username": username, "shared_routes": ["route1", "route2"]}  # Example return structure
    return user


# Mock function to simulate User search
def mock_search_user(args):
    # Simulate a search that returns no results for specific queries
    if args.get("username") == "disconnected" or args.get("email") == "disconnected":
        raise ConnectionError("Simulated server disconnect")
    # Return a list of mock users for other queries
    return []


def mock_get_by_cid(comment_id):
    if comment_id == "nonexistent":
        return None
    if comment_id == "disconnected":
        raise ConnectionError("Simulated server disconnect")
    comment = Comment()
    comment.id = comment_id
    comment.author = "commentAuthor"  # Adjust as necessary based on your test cases

    # Mocked method to simulate the deletion logic as per the provided source code.
    def mock_delete_comment(owner, author):
        # Simulate checking ownership and authorship
        if bool(owner) == bool(author):
            return False

        # For simplicity, simulate the comment is always associated with a route
        # and adjust the route's creator and comment's author as per your testing needs
        route_creator_username = "validOwner"
        if route_creator_username != owner and comment.author != author:
            return False

        # Simulate successful deletion
        return True

    comment.delete_comment = mock_delete_comment
    return comment


def mock_get_by_name(groupname):
    if groupname == "nonexistent":
        return None
    if groupname == "disconnected":
        raise ConnectionError("Simulated server disconnect")

    def mock_to_dict():
        return {"name": "mockgroup", "members": ["user1", "user2"]}

    group = Group()
    group.name = groupname
    # Assuming delete_group returns False if the user is not authorized
    group.delete_group = lambda manager: manager == "authorizedmanager"
    group.toDICT = mock_to_dict
    group.remove_member = lambda x: False if x is None else x.username != "nonmember"
    return group


# Mock function to simulate route update behavior
def mock_update_route(route_id, data):
    if route_id == "nonexistent":
        return False
    if route_id == "disconnected":
        raise ConnectionError("Simulated server disconnect")
    return True


def mock_search_routes(args):
    if args.get("city") == "disconnected":
        raise ConnectionError("Simulated server disconnect")
    return []


def mock_add_comment(route, comment):
    return True


@pytest.fixture
def mock_all_routes_success(monkeypatch):
    def mock_return():
        return [
            {"id": "route1", "name": "Route 1", "description": "This is route 1"},
            {"id": "route2", "name": "Route 2", "description": "This is route 2"},
        ]

    monkeypatch.setattr(Route, "all_routes", mock_return)


@pytest.fixture
def mock_all_routes_failure(monkeypatch):
    def mock_return():
        raise Exception("Simulated database failure")

    monkeypatch.setattr(Route, "all_routes", mock_return)


@pytest.fixture(autouse=True)
def setup_user(monkeypatch):
    monkeypatch.setattr(User, "get_by_username", mock_get_by_username)
    monkeypatch.setattr(User, "save", mock_save)
    monkeypatch.setattr(User, "search_user", mock_search_user)


@pytest.fixture(autouse=True)
def setup_route(monkeypatch):
    monkeypatch.setattr(Route, "get_by_rid", mock_get_by_rid)
    monkeypatch.setattr(Route, "add_comment", mock_add_comment)
    monkeypatch.setattr(Route, "update_route", mock_update_route)
    monkeypatch.setattr(Route, "search_routes", mock_search_routes)


@pytest.fixture(autouse=True)
def setup_comment(monkeypatch):
    monkeypatch.setattr(Comment, "get_by_cid", mock_get_by_cid)
    monkeypatch.setattr(Comment, "save", mock_save)


@pytest.fixture(autouse=True)
def setup_event(monkeypatch):
    monkeypatch.setattr(Event, "save", mock_save)


@pytest.fixture(autouse=True)
def setup_group(monkeypatch):
    monkeypatch.setattr(Group, "get_by_name", mock_get_by_name)
    monkeypatch.setattr(Group, "save", mock_save)
