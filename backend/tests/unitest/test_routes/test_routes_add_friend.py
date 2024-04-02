from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_add_friend_data.yaml"
test_cases = load_data(yaml_file_path)

# Assuming we have a function to check if two users are friends
def mock_are_friends(user, friend):
    # This function should return True if user and friend are already friends,
    # otherwise False. For simplicity, let's say "alreadyfriends" and "friend1"
    # are already friends.
    return user.username == "alreadyfriends" and friend.username == "friend1"

class TestAddFriend:
    @staticmethod
    def mock_get_by_username(username):
        # Here, "nonexistent" simulates a user that doesn't exist in the database.
        if username == "nonexistent":
            return None
        user = User()
        user.username = username
        user.add_friend = lambda friend: not mock_are_friends(user, friend)  # Simplified logic
        return user

    @pytest.mark.parametrize("test_case", test_cases)
    def test_add_friend(self, test_client, test_case, monkeypatch):
        monkeypatch.setattr(User, "get_by_username", self.mock_get_by_username)

        response = test_client.post('/api/addingfriend/', json={
            "username": test_case["username"],
            "friend_username": test_case["friend_username"]
        }, content_type=test_case["content_type"])

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert response.json['user'] == test_case["username"]
