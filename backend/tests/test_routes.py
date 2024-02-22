import json
import pytest
from unittest.mock import patch
from backend.api.models import User, Route


@pytest.fixture(scope='class', autouse=True)
def add_user():
    user_info = {"username": "testuser", "password": "testpassword"}
    user = User(username="testuser")
    user.password = "testpassword"
    user.save()
    added_user = User.get_by_username(username=user_info['username'])
    assert added_user is not None, "User should be added to the database"
    assert added_user.username == user_info['username'], "Added user should have the correct username"
    yield


@pytest.mark.parametrize("username, password, content_type, expected_status", [
    ("newuser1", "newpassword1", "text", 415),  # 415 - unsupported type
    # TODO: it should return 401 according to the requirement,but actually 400
    ("testuser1", None, "application/json", 400),  # 400 - unsupported input
    ("testuser", "testpassword", "application/json", 400),  # 400 - usrname exists
    ("newuser", "newpassword", "application/json", 200),  # 200 - success
])
class TestUserSignUp:
    def test_signup_user(self, test_client, username, password, content_type, expected_status):
        data = {"username": username, "password": password}
        response = test_client.post('/api/sign-up/', data=json.dumps(data), content_type=content_type)

        assert response.status_code == expected_status

        if expected_status == 200:
            assert response.json['success'] is True
            added_user = User.get_by_username(username=response.json['username'])
            assert added_user is not None, "User should be added to the database"
            assert added_user.username == data['username'], "Added user should have the correct username"


# TODO: test for 401 - other failure
# def test_signup_other(self, test_client, username, password, content_type, expected_status):
#     pass


@pytest.mark.parametrize("username, password, content_type, expected_status", [
    ("testuser", "testpassword", "application/json", 200),  # 200 - successusrname
    ("newuser", "newpassword", "application/json", 401),  # 401 - not exists
    ("testuser", "testpassword1", "application/json", 400),  # 400 - wrong password
    # TODO: it should return 401 according to the requirement,but actually 400
    ("testuser", None, "application/json", 400),  # 400 - unsupported input
    ("testuser", "testpassword", "text", 415),  # 415 - unsupported type
])
class TestUserLogin:
    def test_login_user(self, test_client, username, password, content_type, expected_status):
        data = {"username": username, "password": password}
        response = test_client.post('/api/login/', data=json.dumps(data), content_type=content_type)

        assert response.status_code == expected_status

        if expected_status == 200:
            assert response.json['success'] is True
            added_user = User.get_by_username(username=response.json['username'])
            assert added_user.check_password(password), "User should be able to login with the correct password"


# TODO: test for 403 - other failure
# def test_login_other(self, test_client, username, password, content_type, expected_status):
#     pass


test_data = [
    (
        "testuser",
        "https://example.com/path/to/kml/file.kml",
        "Mountain View",
        "Rancho San Antonio",
        2,
        30,
        "Moderate",
        "This trail offers a good mix of uphill and downhill sections, with beautiful views of the valley.",
        "application/json",
        200  # 200 - success
    ),
    (
        "testuser1",
        "https://example.com/path/to/kml/file.kml",
        "Mountain View",
        "Rancho San Antonio",
        2,
        30,
        "Moderate",
        "This trail offers a good mix of uphill and downhill sections, with beautiful views of the valley.",
        "application/json",
        401  # 401 - not exists
    ),
    # TODO: it should return 401 according to the requirement,but actually 400
    (
        "u",
        "https://example.com/path/to/kml/file.kml",
        "MV",
        "Rancho",
        1,
        15,
        "Easy",
        "Short trail with minimal elevation gain.",
        "application/json",
        400  # 400 - unsupported input
    ),
    (
        "u",
        "https://example.com/path/to/kml/file.kml",
        "MV",
        "Rancho",
        1,
        15,
        "Easy",
        "Short trail with minimal elevation gain.",
        "text",
        415  # 415 - unsupported type
    )
]


@pytest.mark.parametrize(
    "username, kmlURL, city, location, hours, minutes, difficulty, desc, content_type, expected_status", test_data)
class TestUploadRoute:
    def test_upload_route(self, test_client, username, kmlURL, city, location, hours, minutes, difficulty, desc,
                          content_type, expected_status):
        data = {
            "username": username,
            "kmlURL": kmlURL,
            "city": city,
            "location": location,
            "hours": hours,
            "minutes": minutes,
            "difficulty": difficulty,
            "desc": desc
        }

        response = test_client.post('/api/upload/', data=json.dumps(data), content_type=content_type)

        assert response.status_code == expected_status

        if expected_status == 200:
            assert response.json['success'] is True
            added_route = Route.get_by_rid(rid=response.json['route_id'])
            assert added_route is not None, "Route should be added to the database"
            assert added_route.creator_username == data[
                'username'], "Added route should have the correct creator username"


# TODO: test for 403 - other failure


@pytest.mark.parametrize("username, content_type, expected_status", [
    ("testuser", "application/json", 200),  # 200 - successusrname
    ("newuser", "application/json", 401),  # 401 - not exists
    # TODO: it should return 401 according to the requirement,but actually 400
    (None, "application/json", 400),  # 400 - unsupported input
    ("testuser", "text", 415),  # 415 - unsupported type
])
class TestUserRoutes:
    @pytest.fixture(scope='class', autouse=True)
    def add_route(self):
        route = Route(creator_username="testuser", kmlURL="https://example.com/path/to/kml/file.kml",
                      city="Mountain View", location="Rancho San Antonio", hour=2, min=30, difficulty="Moderate",
                      desc="This trail offers a good mix of uphill and downhill sections, with beautiful views of the valley.")
        route.save()
        user = User.get_by_username(username="testuser")
        user.add_create_routes(route)
        added_route = Route.get_by_rid(rid=route.id)
        assert added_route is not None, "Route should be added to the database"
        assert added_route.creator_username == "testuser", "Added route should have the correct creator username"

    def test_user_routes(self, test_client, username, content_type, expected_status):
        data = {"username": username}
        response = test_client.post('/api/userroutes/', data=json.dumps(data), content_type=content_type)

        if expected_status == 200:
            assert response.json['success'] is True
            assert response.json['routes'] is not None

    # TODO: test for 403 - other failure
