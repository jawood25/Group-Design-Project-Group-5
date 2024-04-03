from pathlib import Path

import pytest

from backend.utils.file.yaml_op import load_data


class TestCreateEvent:
    @pytest.mark.parametrize("test_case", load_data(Path(__file__).parent /"data/test_create_event_data.yaml"))
    def test_create_event(self, test_client, test_case):
        response = test_client.post('/api/uploadevent/', json=test_case["req_data"],
                                    content_type=test_case.get("content_type", "application/json"))

        assert response.status_code == test_case["expected_status"]
        if response.status_code == 200:
            assert response.json['success'] is True
            assert "Route is created" in response.json['msg']  # Consider updating message to "Event is created"
            # Further assertions can be added to verify the contents of the response
        elif response.status_code in [401, 403]:
            assert response.json['success'] is False
