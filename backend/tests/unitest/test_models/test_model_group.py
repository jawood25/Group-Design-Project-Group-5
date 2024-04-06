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


def create_test_group(test_case, i=0):
    users = []
    for member in test_case.get('members', []):
        user = User.objects(username=member).first()
        if user:
            users.append(user)
    if i == 0:
        g = Group(name=test_case['name'], manager="testuser", members=users)
    else:
        g = Group(name=f"{test_case['name']}{i}", manager="testuser", members=users)
    g.save()
    return g

def create_groups(test_case):
    for i in range(test_case['expected_groups_num'] - 1):
        create_test_group(test_case,i+1)


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
        elif method == "all_groups":
            create_groups(test_case)
            all_groups = Group.all_groups()
            assert isinstance(all_groups, list) and len(all_groups) > 0, "Failed to retrieve all routes."
        elif method == "toDICT":
            group_dict = group.toDICT()
            assert group_dict == test_case['expected_dict'], "toDICT method failed."
    except Exception as e:
        if not test_case['expected_success']:
            assert True, "Failed as expected."
        else:
            pytest.fail(f"Unexpected error occurred: {e}")
