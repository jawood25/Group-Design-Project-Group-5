from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_uploadroutes_data.yaml"
test_cases = load_data(yaml_file_path)


# Test the /api/upload/ route
class TestUploadRoute:
    # Simulate a server disconnect
    def mock_get_by_username(self, *args, **kwargs):
        raise ConnectionError("Simulated server disconnect")

    # test by adding a route
    @pytest.mark.parametrize("test_case", test_cases)
    def test_upload_route(self, test_client, test_case, monkeypatch):
        expected_status = test_case["expected_status"]
        # If the expected status is 403, simulate server disconnect using monkeypatch
        if expected_status == 403:
            monkeypatch.setattr(User, "get_by_username", self.mock_get_by_username)

        response = test_client.post('/api/upload/', json={
            "username": test_case["username"],
            "coordinates": test_case["coordinates"],
            "city": test_case["city"],
            "location": test_case["location"],
            "hours": test_case["hours"],
            "minutes": test_case["minutes"],
            "difficulty": test_case["difficulty"],
            "comment": test_case["comment"]
        }, content_type=test_case["content_type"])

        assert response.status_code == test_case["expected_status"], \
            f"Failed test case: {test_case}"

        if response.status_code == 200:
            assert response.json['success'] is True
            assert 'route_id' in response.json, "Route ID not found in response."
            assert 'msg' in response.json, "Message not found in response."
        if response.status_code == 403:
            # Expected failure message
            assert response.json['success'] is False
            assert response.json['msg'] == "Simulated server disconnect"
