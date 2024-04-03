from pathlib import Path

import pytest

from backend.api.models import Group, User
from backend.utils.file.yaml_op import load_data


@pytest.fixture(scope='function', autouse=True)
def add_user():
    user_info = [{"username": "Member One", "password": "testpassword"},
                 {"username": "Member Two", "password": "testpassword"},
                 {"username": "testuser", "password": "testpassword"}]
    for user in user_info:
        added_user = User(**user)
        added_user.save()
        assert added_user is not None, "User should be added to the database"
    yield


def create_test_user(username="testmember"):
    user_info = {"username": username, "password": "testpassword"}
    added_user = User(**user_info)
    added_user.save()
    return added_user


def create_test_group(test_case):
    users = []
    for member in test_case.get('members', []):
        user = User.objects(username=member).first()
        if user:
            users.append(user)
    g = Group(name=test_case['name'], manager="testuser", members=users)
    g.save()
    return g


@pytest.mark.parametrize("test_case", load_data(Path(__file__).parent / "data/test_group.yaml"))
def test_group_methods(test_client, test_case):
    method = test_case['method']
    try:
        group = create_test_group(test_case)
        if method == "__repr__":
            assert group.__repr__() == f"Group {test_case['name']}", "__repr__ method failed."
        elif method == "remove_member":
            member = User.objects(username=test_case['member_to_remove']).first()
            result = group.remove_member(member)
            assert result == test_case['expected_result'], "remove_member method failed."
        elif method == "delete_group":
            result = group.delete_group(test_case['manager'])
            assert result == test_case['expected_result'], "delete_group method failed."
        elif method == "get_by_name":
            group = Group.get_by_name(test_case['name'])
            assert group is not None, "get_by_name method failed."
        elif method == "toDICT":
            group_dict = group.toDICT()
            assert group_dict == test_case['expected_dict'], "toDICT method failed."
    except Exception as e:
        if not test_case['expected_success']:
            assert True, "Failed as expected."
        else:
            pytest.fail(f"Unexpected error occurred: {e}")
