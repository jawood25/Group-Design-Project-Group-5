from pathlib import Path

import pytest

from backend.utils.file.yaml_op import load_data


# Test the /api/upload/ route
class TestUploadRoute:
    @pytest.mark.parametrize("test_case", load_data(
        Path(__file__).parent / "data/test_uploadroutes_data.yaml"
    ))
    def test_upload_route(self, test_client, test_case):
        # Prepare and send the request to the API
        response = test_client.post('/api/upload/', json={
            "username": test_case["username"],
            "coordinates": test_case["coordinates"],
            "mapCenter": test_case["map_center"],
            "city": test_case["city"],
            "mobility": test_case["mobility"],
            "location": test_case["location"],
            "difficulty": test_case["difficulty"],
            "comment": test_case["comment"]
        }, content_type=test_case.get("content_type", "application/json"))

        # Assert the response status code
        assert response.status_code == test_case["expected_status"]

        # Handle assertions for successful upload
        if response.status_code == 200:
            assert response.json['success'] is True
            assert 'route_id' in response.json, "Expected 'route_id' in response."
            assert 'msg' in response.json, "Expected 'msg' in response."

        # Handle assertions for simulated server disconnect or other failures
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False


class TestEditRoute:
    @pytest.mark.parametrize("test_case", load_data(
        Path(__file__).parent / "data/test_edit_route_data.yaml")["post"]
                             )
    def test_edit_route(self, test_client, test_case):

        response = test_client.post('/api/editroute/', json=test_case["req_data"],
                                    content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Route is updated" in response.json['msg']
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False

    @pytest.mark.parametrize("test_case", load_data(
        Path(__file__).parent / "data/test_edit_route_data.yaml")["delete"]
                             )
    def test_delete_route(self, test_client, test_case):

        response = test_client.delete('/api/editroute/',
                                      json=test_case["req_data"],
                                      content_type=test_case.get("content_type",
                                                                 "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Route has been deleted" in response.json['msg']
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False


class TestAllRoutes:
    def test_fetch_all_routes_success(self, test_client, mock_all_routes_success):
        sample_routes = [
            {"id": "route1", "name": "Route 1", "description": "This is route 1"},
            {"id": "route2", "name": "Route 2", "description": "This is route 2"},
        ]
        response = test_client.post('/api/allUR/')
        assert response.status_code == 200
        assert response.json['success'] is True
        assert response.json['routes'] == sample_routes
        assert "Routes retrieved successfully" in response.json['msg']

    def test_fetch_all_routes_failure(self, test_client, mock_all_routes_failure):
        response = test_client.post('/api/allUR/')
        assert response.status_code == 500
        assert response.json['success'] is False
        assert "Simulated database failure" in response.json['msg']


class TestSearchRoute:
    @pytest.mark.parametrize("test_case", load_data(
        Path(__file__).parent / "data/test_search_route_data.yaml"
    ))
    def test_search_route(self, test_client, test_case):
        response = test_client.post('/api/searchroute/', json=test_case["search_criteria"],
                                    content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert isinstance(response.json['routes'], list)
            assert "Routes retrieved successfully" in response.json['msg']
        elif response.status_code == 500:
            assert response.json['success'] is False
