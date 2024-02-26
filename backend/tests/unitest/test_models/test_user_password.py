# test_user_password.py
from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_data

yaml_file_path = Path(__file__).parent / "data/test_user_password.yaml"
test_cases = load_data(yaml_file_path)


# Test user password
@pytest.mark.parametrize("test_case", test_cases)
class TestUserPassword:
    # test by setting password
    def test_check_password(self, test_client, test_case):
        # For valid user creation cases, test password verification
        user = User.objects(username=test_case['username']).first()
        with pytest.raises(AttributeError):
            _ = user.password
        assert user.check_password(test_case['password']) == test_case[
            'expected_success'], "Password verification should succeed."
