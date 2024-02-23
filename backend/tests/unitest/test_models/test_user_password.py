# test_user.py
import pytest
from pathlib import Path
from backend.api.models import User, Route
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/user_password_data.yaml"
test_cases = load_test_data(yaml_file_path)


@pytest.mark.parametrize("test_case", test_cases)
class TestUserPassword:
    def test_check_password(self, test_client, test_case):
        # For valid user creation cases, test password verification
        user = User.objects(username=test_case['username']).first()
        with pytest.raises(AttributeError):
            _ = user.password
        assert user.check_password(test_case['password']) == test_case[
            'expected_success'], "Password verification should succeed."
