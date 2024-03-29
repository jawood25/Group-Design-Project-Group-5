from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_delete_friend_data.yaml"
test_cases = load_data(yaml_file_path)


# Assuming a function to check if the deletion was successful
def mock_delete_friend(friend):
    # This function returns True if the friend can be deleted,
    # and False if the friend cannot be found in the user's friend list.
    return friend.username != "undeletablefriend"


class TestDeletingFriend:
    @staticmethod
    def mock_get_by_username(username):
        # "nonexistent" simulates a user that doesn't exist in the database.
        if username == "nonexistent":
            return None
        user = User()
        user.username = username
        user.delete_friend = lambda friend: mock_delete_friend(friend)
        return user

    @pytest.mark.parametrize("test_case", test_cases)
    def test_deleting_friend(self, test_client, test_case, monkeypatch):
        monkeypatch.setattr(User, "get_by_username", self.mock_get_by_username)

        response = test_client.post('/api/deletingfriend/', json={
            "username": test_case["username"],
            "friend_username": test_case["friend_username"]
        }, content_type=test_case["content_type"])

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert response.json['user'] == test_case["username"]
