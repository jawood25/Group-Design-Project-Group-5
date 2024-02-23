import pytest
from pathlib import Path
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/signup_test_data.yaml"
test_cases = load_test_data(yaml_file_path)


class TestUserSignUp:
    @pytest.mark.parametrize("test_cases", test_cases)
    def test_user_sign_up(self, test_client, test_cases):
        # Simulate a POST request to the sign-up endpoint
        response = test_client.post('/api/sign-up/', json={
            "username": test_cases["username"],
            "password": test_cases["password"]
        }, content_type=test_cases["content_type"])

        # Assert that the response status code matches the expected outcome
        assert response.status_code == test_cases["expected_status"]

        if response.status_code == 200:
            # Further checks if sign up was successful
            assert response.json['success'] is True
            assert response.json['username'] == test_cases["username"]

# TODO: test for 401 - other failure
# def test_user_routes_other(self, test_client, test_case):
#     pass
