# pylint: disable=no-member
from pathlib import Path

import pytest

from backend.api.models import Event, User, Route
from backend.utils.file.yaml_op import load_data


def create_test_user_and_route():
    user_info = {"username": "hostUser", "password": "testpassword"}
    added_user = User(**user_info)
    added_user.save()

    route = Route(creator_username=added_user.username)
    route.save()
    return added_user, route


@pytest.mark.parametrize("test_case", load_data(Path(__file__).parent / "data/test_event.yaml"))
def test_event_methods(test_client, test_case):
    method = test_case['method']
    try:
        if method == "__init__":
            event = Event(**test_case['params'])
            for key, value in test_case['params'].items():
                if key == "id":
                    continue
                if key == "date":
                    assert getattr(event, key).strftime('%Y-%m-%dT%H:%M:%S') == value, \
                        f"{key} does not match."
                else:
                    assert getattr(event, key) == value, f"{key} does not match."
        elif method == "__repr__":
            event = Event(name=test_case['name'])
            assert repr(event) == f"Event {test_case['name']}", "__repr__ method failed."
        elif method == "get_by_eid":
            event = Event(**test_case['params'])
            event.save()
            found_event = Event.get_by_eid(event.id)
            assert found_event is not None, "Failed to retrieve event by ID."
        elif method == "toDICT":
            user, route = create_test_user_and_route()
            event = Event(name=test_case['expected_dict']['name'],
                          venue=test_case['expected_dict']['venue'],
                          interested=test_case['expected_dict']['interested'],
                          date=test_case['expected_dict']['date'],
                          hostname=test_case['expected_dict']['host'], route_id=route.id,
                          information=test_case['expected_dict']['information'])
            event_dict = event.toDICT()
            test_case['expected_dict'].pop('rid')
            test_case['expected_dict']['route'] = route.toDICT()
            assert event_dict == test_case['expected_dict'], "toDICT method failed."
    except Exception as e:
        if not test_case['expected_success']:
            assert True, "Failed as expected."
        else:
            pytest.fail(f"Unexpected error occurred: {e}")
