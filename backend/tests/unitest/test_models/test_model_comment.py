# pylint: disable=no-member
import datetime
from pathlib import Path

import pytest

from backend.api.models import Route, Comment
from backend.utils.file.yaml_op import load_data


def create_test_route(test_comment):
    test_route = Route(creator_username="testuser")
    test_route.comment = [test_comment]
    test_route.save()
    return test_route


def create_test_comment(author, body, likes=0, dislikes=0):
    if author is None:
        author = "commentAuthor"
    comment = Comment(author=author, body=body, likes=likes,
                      dislikes=dislikes, date_posted=datetime.datetime.now())
    comment.save()
    return comment


@pytest.mark.parametrize("test_case", load_data(Path(__file__).parent / "data/test_comment.yaml"))
def test_comment_methods(test_client, test_case):
    method = test_case['method']
    try:
        if method == "__init__":
            comment = create_test_comment(**test_case['params'])
            for key, value in test_case['params'].items():
                assert getattr(comment, key) == value, f"{key} does not match."
        elif method == "__repr__":
            comment = create_test_comment(test_case['author'], test_case['body'])
            assert repr(comment) == f"{test_case['author']}'s comment"
        elif method == "delete_comment":
            owner = test_case['owner']
            author = test_case['author']
            comment = create_test_comment("commentAuthor", "Sample comment body")
            if not test_case.get('no_route', False):
                create_test_route(comment)
            # Assuming `get_route()` and other interactions need mock or setup
            result = comment.delete_comment(owner, author)
            assert result == test_case['expected_result']
        elif method == "get_route":
            test_comment = create_test_comment("testuser", "Sample comment")
            test_route = create_test_route(test_comment)
            retrieved_route = test_comment.get_route()
            assert retrieved_route == test_route, \
                "get_route method failed to retrieve the correct route."
        elif method == "get_by_cid":
            # Assuming we have a setup phase where a comment is created and we have its id
            comment = create_test_comment("testuser", "Sample comment")
            cid = comment.id
            retrievde_comment = Comment.get_by_cid(cid)
            assert retrievde_comment is not None  # Adjust according to your logic
        elif method == "toDICT":
            comment = create_test_comment("testuser", "Sample comment", 5, 2)
            comment_dict = comment.toDICT()
            assert comment_dict['author'] == "testuser"
            assert comment_dict['likes'] == 5
            assert comment_dict['dislikes'] == 2
            # More assertions based on the structure
    except Exception as e:
        # Handling exceptions based on test case expectations
        if test_case['expected_success'] is False:
            assert True, "Failed as expected."
        else:
            pytest.fail(f"Unexpected error occurred: {e}")
