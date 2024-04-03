from pathlib import Path

import pytest

from backend.utils.file.yaml_op import load_data


class TestCreateComment:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_create_comment_data.yaml"))
    def test_adding_comment(self, test_client, test_case):
        response = test_client.post('/api/addingcomment/', json=test_case["req_data"],
                                    content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Comment is created" in response.json['msg']
        elif response.status_code in [401, 402, 403]:
            assert response.json['success'] is False


class TestCreatedComment:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_created_comment_data.yaml"))
    def test_fetch_comments(self, test_client, test_case):
        response = test_client.post('/api/routescomment/', json={
            "route_id": test_case["route_id"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert isinstance(response.json['comment'], list)
            assert "Comments retrieved successfully" in response.json['msg']
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False


class TestShareRoutes:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_share_route_data.yaml"))
    def test_share_route(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/shareroute/', json={
            "username": test_case["username"],
            "route_id": test_case["route_id"],
            "friend_username": test_case["friend_username"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Routes retrieved successfully" in response.json['msg']
            # Further validation can be done on the response's content if necessary
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False

class TestDeleteComment:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_delete_comment_data.yaml"))
    def test_delete_comment(self, test_client, test_case):
        # Construct the request payload dynamically, excluding 'null' values
        payload = {"comment_id": test_case["comment_id"]}
        if test_case.get("owner") is not None:
            payload["owner"] = test_case["owner"]
        if test_case.get("author") is not None:
            payload["author"] = test_case["author"]

        response = test_client.post('/api/deletecomment/', json=payload,
                                    content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Comment has been deleted" in response.json['msg']
        elif response.status_code in [401, 403, 402]:
            assert response.json['success'] is False
