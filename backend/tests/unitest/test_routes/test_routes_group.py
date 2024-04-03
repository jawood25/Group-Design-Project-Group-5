from pathlib import Path

import pytest

from backend.utils.file.yaml_op import load_data


class TestCreateGroup:

    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_create_group_data.yaml"))
    def test_create_group(self, test_client, test_case, monkeypatch):
        # Simulate a POST request to create a group
        response = test_client.post('/api/creategroup/', json={
            "name": test_case["name"],
            "manager": test_case["manager"],
            "members": test_case["members"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Group is created" in response.json['msg']
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False


class TestDeleteGroup:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_delete_group_data.yaml"))
    def test_delete_group(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/deletegroup/', json={
            "groupname": test_case["groupname"],
            "manager": test_case["manager"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Group deleted" in response.json['msg']
        elif response.status_code in [401, 402, 500]:
            assert response.json['success'] is False


# Mock function for converting group information to a dictionary

class TestGetGroup:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_get_group_data.yaml"))
    def test_get_group(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/getgroup/', json={
            "groupname": test_case["groupname"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Groups retrieved successfully" in response.json['msg']
            # Optionally, check for the content of the group information
        elif response.status_code in [401, 500]:
            assert response.json['success'] is False


class TestLeaveGroup:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_leave_group_data.yaml"))
    def test_leave_group(self, test_client, test_case, monkeypatch):

        response = test_client.post('/api/leavinggroup/', json={
            "groupname": test_case["groupname"],
            "username": test_case["username"]
        }, content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "member leave" in response.json['msg']
        elif response.status_code in [401, 402, 500]:
            assert response.json['success'] is False
