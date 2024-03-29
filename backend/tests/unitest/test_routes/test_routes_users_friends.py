from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_users_friends_data.yaml"
test_cases = load_data(yaml_file_path)

# Mock function to simulate fetching friends from the database
def mock_get_friends():
    # Return a list of friend usernames for simplicity
    return ["friend1", "friend2", "friend3"]

class TestUsersFriends:
    @staticmethod
    def mock_get_by_username(username):
        # "nonexistent" simulates a user that doesn't exist in the database.
        if username == "nonexistent":
            return None
        user = User()
        user.username = username
        user.get_friends = mock_get_friends
        return user

    @pytest.mark.parametrize("test_case", test_cases)
    def test_users_friends(self, test_client, test_case, monkeypatch):
        monkeypatch.setattr(User, "get_by_username", self.mock_get_by_username)

        response = test_client.post('/api/usersfriends/', json={
            "username": test_case["username"]
        }, content_type=test_case["content_type"])

        assert response.status_code == test_case["expected_status"]

        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Friends retrieved successfully" in response.json['msg']

