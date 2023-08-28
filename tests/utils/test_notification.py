import pytest
from app.utils.notification import Notification


class TestNotification:
    @pytest.fixture
    def notification(self):
        return Notification()

    def test_create_html_table(self, notification):
        data = [
            {"header1": "value1", "header2": "value2"},
            {"header1": "value3", "header2": "value4"}
        ]

        expected_html = (
            "<table class='styled-table'>\n"
            "<thead>\n<tr>\n<th>header1</th>\n<th>header2</th>\n</tr>\n</thead>\n"
            "<tbody>\n<tr>\n<td>value1</td>\n<td>value2</td>\n</tr>\n"
            "<tr>\n<td>value3</td>\n<td>value4</td>\n</tr>\n</tbody>\n</table>"
        )

        assert notification.create_html_table(data) == expected_html
