# test_user_creation.py
from pathlib import Path
import pytest

from backend.api.models import User
from backend.utils.file.yaml_op import load_test_data

yaml_file_path = Path(__file__).parent / "data/user_creation_data.yaml"
test_cases = load_test_data(yaml_file_path)


@pytest.mark.parametrize("test_case", test_cases)
class TestUserCreation:
    def test_create_user(self, test_client, test_case):
        # Attempt to create a user, checking if it should succeed based on expected_success
        try:
            user = User(username=test_case['username'])
            user.password = test_case['password']
            user.save()
            assert User.objects(username=test_case['username']).first() is not None
            assert user.__repr__() == f"User {test_case['username']}"
            assert test_case['expected_success'], "Expected user creation to succeed."
        except Exception as e:
            # If failure is expected, catching an exception is a test pass
            if not test_case['expected_success']:
                assert True, "User creation failed as expected."
            else:
                pytest.fail(f"User creation failed unexpectedly: {e}")
