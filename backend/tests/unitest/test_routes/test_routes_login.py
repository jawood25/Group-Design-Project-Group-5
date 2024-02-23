import pytest
from pathlib import Path
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/login_test_data.yaml"
test_cases = load_test_data(yaml_file_path)


class TestUserLogin:
    @pytest.mark.parametrize("test_case", test_cases)
    def test_user_login(self, test_client, test_case):
        # Use the correct password for login test
        login_password = test_case.get("wrong_password", test_case["password"])
        response = test_client.post('/api/login/', json={
            "username": test_case["username"],
            "password": login_password
        }, content_type=test_case["content_type"])

        # Assert that the response status code matches the expected outcome for login
        expected_status = test_case.get("expected_status")
        if "wrong_password" in test_case:
            expected_status = 400  # Expect login failure if wrong password is used

        assert response.status_code == expected_status

        if response.status_code == 200:
            # Further checks if login was successful
            assert response.json['success'] is True
            assert response.json['username'] == test_case["username"]

    # TODO: test for 403 - other failure
    # def test_user_routes_other(self, test_client, test_case):
    #     pass
