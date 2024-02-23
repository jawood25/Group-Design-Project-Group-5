# test_user_getname.py
from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/user_getname_data.yaml"
test_cases = load_test_data(yaml_file_path)


@pytest.mark.parametrize("test_case", test_cases)
class TestUserGetName:
    def test_get_by_username(self, test_client, test_case):
        # Test adding routes only for cases where user creation is expected to succeed
        user = User.get_by_username(test_case['username'])
        if test_case['expected_success']:
            assert user is not None, "User should exist in the database."
            assert user.username == test_case['username'], "User should have the correct username."
        else:
            assert user is None, "User should not exist in the database."
