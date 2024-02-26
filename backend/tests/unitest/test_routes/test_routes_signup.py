from pathlib import Path
import pytest

from backend.utils.file.yaml_op import load_data
yaml_file_path = Path(__file__).parent / "data/test_signup_data.yaml"
test_cases = load_data(yaml_file_path)

# Test the /api/sign-up/ route
class TestUserSignUp:
    # test by adding a user
    @pytest.mark.parametrize("test_case", test_cases)
    def test_user_sign_up(self, test_client, test_case):
        # Simulate a POST request to the sign-up endpoint
        response = test_client.post('/api/sign-up/', json={
            "username": test_case["username"],
            "password": test_case["password"]
        }, content_type=test_case["content_type"])

        # Assert that the response status code matches the expected outcome
        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            # Further checks if sign up was successful
            assert response.json['success'] is True
            assert response.json['username'] == test_case["username"]

    # TODO: test for 401 - other failure
    # def test_user_routes_other(self, test_client, test_case):
    #     pass
