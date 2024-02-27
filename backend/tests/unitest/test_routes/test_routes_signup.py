from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_signup_data.yaml"
test_cases = load_data(yaml_file_path)


# Test the /api/sign-up/ route
class TestUserSignUp:
    # Simulate a server disconnect
    def mock_get_by_username(self, *args, **kwargs):
        raise ConnectionError("Simulated server disconnect")

    # test by adding a user
    @pytest.mark.parametrize("test_case", test_cases)
    def test_user_sign_up(self, test_client, test_case, monkeypatch):
        expected_status = test_case["expected_status"]

        # If the expected status is 403, simulate server disconnect using monkeypatch
        if expected_status == 401:
            monkeypatch.setattr(User, "get_by_username", self.mock_get_by_username)

        # Simulate a POST request to the sign-up endpoint
        response = test_client.post('/api/sign-up/', json={
            "username": test_case["username"],
            "password": test_case["password"]
        }, content_type=test_case["content_type"])

        # Assert that the response status code matches the expected outcome
        assert response.status_code == test_case["expected_status"], \
            f"Failed test case: {test_case}"
        if response.status_code == 200:
            # Further checks if sign up was successful
            assert response.json['success'] is True
            assert response.json['username'] == test_case["username"]
        # If status code is 401, validate the expected failure message
        if response.status_code == 401:
            # Expected failure message
            assert response.json['success'] is False
            assert response.json['msg'] == "Simulated server disconnect"
