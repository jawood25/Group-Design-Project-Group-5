from pathlib import Path
import pytest

from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_uploadroutes_data.yaml"
test_cases = load_data(yaml_file_path)


# Test the /api/upload/ route
class TestUploadRoute:

    # test by adding a route
    @pytest.mark.parametrize("test_case", test_cases)
    def test_upload_route(self, test_client, test_case):
        response = test_client.post('/api/upload/', json={
            "username": test_case["username"],
            "kmlURL": test_case["kmlURL"],
            "city": test_case["city"],
            "location": test_case["location"],
            "hours": test_case["hours"],
            "minutes": test_case["minutes"],
            "difficulty": test_case["difficulty"],
            "desc": test_case["desc"]
        }, content_type=test_case["content_type"])

        assert response.status_code == test_case["expected_status"], f"Failed test case: {test_case}"

        if response.status_code == 200:
            assert response.json['success'] is True
            assert 'route_id' in response.json, "Route ID not found in response."
            assert 'msg' in response.json, "Message not found in response."

    # TODO: test for 403 - other failure
    # def test_user_routes_other(self, test_client, test_case):
    #     pass
