"""
This module contains unit tests for the functions in app.py
"""
import unittest
from unittest.mock import patch
from app import read_db, update_page, calculate_next_due_date


class TestApp(unittest.TestCase):
    """Test class for app.py functions"""

    def test_read_db(self):
        """Test the read_db function"""
        headers = {
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
            "Authorization": "Bearer TOKEN"
        }
        db_id = "DATABASE_ID"
        expected_data = {"results": [{"id": 1}, {"id": 2}, {"id": 3}]}
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = expected_data
            data = read_db(db_id, headers)
            mock_post.assert_called_with(
                url=f"https://api.notion.com/v1/databases/{db_id}/query",
                headers=headers,
                timeout=None
            )
        self.assertEqual(data, expected_data)

    def test_update_page(self):
        """Test the update_page function"""
        headers = {
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
            "Authorization": "Bearer TOKEN"
        }
        page_id = 1
        properties = {"Status": "DONE"}
        expected_response = {"status": "success"}
        with patch("requests.patch") as mock_patch:
            mock_patch.return_value.json.return_value = expected_response
            response = update_page(headers, page_id, properties)
            mock_patch.assert_called_with(
                url=f"https://api.notion.com/v1/pages/{page_id}",
                headers=headers,
                data='{"properties": {"Status": "DONE"}}',
                timeout=None
            )
        self.assertEqual(response, expected_response)

    def test_calculate_next_due_date(self):
        """Test the calculate_next_due_date function"""
        due_date = "2023-06-27"
        periodicity = "Daily"
        expected_next_due_date = "2023-06-28"
        expected_next_set_date = "2023-06-27"
        next_due_date, next_set_date = calculate_next_due_date(
            due_date, periodicity)
        self.assertEqual(str(next_due_date.date()), expected_next_due_date)
        self.assertEqual(str(next_set_date.date()), expected_next_set_date)


if __name__ == "__main__":
    unittest.main()
