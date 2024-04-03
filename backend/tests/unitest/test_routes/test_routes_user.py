from pathlib import Path

import pytest

from backend.utils.file.yaml_op import load_data


# Test the /api/sign-up/ route
class TestUserSignUp:
    # test by adding a user
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_signup_data.yaml"))
    def test_user_sign_up(self, test_client, test_case):
        # Simulate a POST request to the sign-up endpoint
        response = test_client.post('/api/sign-up/', json={
            "username": test_case["username"],
            "password": test_case["password"]
        }, content_type=test_case.get("content_type", "application/json"))

        # Assert that the response status code matches the expected outcome
        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert response.json['username'] == test_case["username"]
        if response.status_code in [401, 405]:
            assert response.json['success'] is False


class TestUserLogin:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_login_data.yaml"))
    def test_user_login(self, test_client, test_case):
        # Prepare request data, considering possible None values
        request_data = {
            "username": test_case.get("username"),
            "password": test_case.get("password")
        }
        # Filter out None values
        request_data = {k: v for k, v in request_data.items() if v is not None}

        response = test_client.post('/api/login/', json=request_data,
                                    content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"], f"Failed for case: {test_case}"

        if response.status_code == 200:
            assert response.json['success'] is True
            assert response.json.get('username') == test_case.get("username")
        elif response.status_code in [401, 403, 405]:
            assert response.json['success'] is False


class TestAddFriend:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_add_friend_data.yaml"))
    def test_add_friend(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/addingfriend/', json={
            "username": test_case["username"],
            "friend_username": test_case["friend_username"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert response.json['user'] == test_case["username"]
        elif response.status_code in [401, 402, 403]:
            assert response.json['success'] is False


class TestSaveRoute:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_save_route_data.yaml"))
    def test_save_route(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/savingroutes/', json={
            "username": test_case["username"],
            "route_id": test_case["route_id"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Route is saved" in response.json['msg']
        elif response.status_code in [401, 402, 403]:
            assert response.json['success'] is False


class TestSavedRoutes:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_saved_routes_data.yaml"))
    def test_saved_routes(self, test_client, test_case, monkeypatch):
        response = test_client.post('/api/savedroutes/', json={
            "username": test_case["username"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert type(response.json['routes']) is list
            assert "Routes retrieved successfully" in response.json['msg']
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False


class TestUnsavingRoute:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_unsave_route_data.yaml"))
    def test_unsaving_route(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/unsavingroutes/', json={
            "username": test_case["username"],
            "route_id": test_case["route_id"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Route is unsaved" in response.json['msg']
        elif response.status_code in [401, 403, 404]:
            assert response.json['success'] is False


class TestDeletingFriend:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_delete_friend_data.yaml"))
    def test_deleting_friend(self, test_client, test_case, monkeypatch):
        response = test_client.post('/api/deletingfriend/', json={
            "username": test_case["username"],
            "friend_username": test_case["friend_username"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert response.json['user'] == test_case["username"]
        elif response.status_code in [401, 402, 403]:
            assert response.json['success'] is False


class TestUsersFriends:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_users_friends_data.yaml"))
    def test_users_friends(self, test_client, test_case, monkeypatch):
        response = test_client.post('/api/usersfriends/', json={
            "username": test_case["username"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Friends retrieved successfully" in response.json['msg']
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False


class TestSearchUser:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_search_user_data.yaml"))
    def test_search_user(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/searchuser/', json=test_case["search_query"],
                                    content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Users retrieved successfully" in response.json['msg']
            # Further checks could be added to validate the contents of the response
        elif response.status_code == 500:
            assert response.json['success'] is False

# Test the /api/savedroutes/ route
class TestCreatedRoutes:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_userroutes_data.yaml"))
    def test_saved_routes(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/userroutes/', json={
            "username": test_case["username"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert isinstance(response.json['routes'], list)
            assert "Routes retrieved successfully" in response.json['msg']
        elif response.status_code in [401, 403]:
            assert not response.json['success']