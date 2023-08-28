import pytest
import datetime
from app.utils.utils import Utils


class TestUtils:
    @pytest.fixture
    def utils(self):
        return Utils()

    def test_get_time_now(self, utils):
        current_time = utils.get_time_now()
        assert current_time is not None
        assert isinstance(current_time, datetime.datetime)

    def test_format_datetime(self, utils):
        example_date = datetime.datetime(2023, 8, 8, 15, 30, 0)
        formatted_date = utils.format_datetime(example_date)
        expected_format = "2023-08-08 15:30:00"
        assert formatted_date == expected_format
