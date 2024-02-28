from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_login_data.yaml"
test_cases = load_data(yaml_file_path)


# Test the /api/login/ route
class TestUserLogin:
    # Simulate a server disconnect
    def mock_get_by_username(self, *args, **kwargs):
        raise ConnectionError("Simulated server disconnect")

    # Test by providing a username and password
    @pytest.mark.parametrize("test_case", test_cases)
    def test_user_login(self, test_client, test_case, monkeypatch):
        # Assert that the response status code matches the expected outcome for login
        expected_status = test_case["expected_status"]

        # If the expected status is 403, simulate server disconnect using monkeypatch
        if expected_status == 403:
            monkeypatch.setattr(User, "get_by_username", self.mock_get_by_username)

        # Use the correct password for login test
        login_password = test_case["password"]
        response = test_client.post('/api/login/', json={
            "username": test_case["username"],
            "password": login_password
        }, content_type=test_case["content_type"])

        assert response.status_code == expected_status

        # Further checks if login was successful
        if response.status_code == 200:
            assert response.json['success'] is True
            assert response.json['username'] == test_case["username"]
        # If status code is 403, validate the expected failure message
        if response.status_code == 403:
            # Expected failure message
            assert response.json['success'] is False
            assert response.json['msg'] == "Simulated server disconnect"
