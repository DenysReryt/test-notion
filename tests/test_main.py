"""
This module contains integration tests for the main.py script
"""
import unittest
from unittest.mock import patch
from main import app


class MainIntegrationTest(unittest.TestCase):
    """Integration tests for main.py"""

    @patch('main.subprocess.Popen')  # Mock the subprocess.Popen method
    def test_run_script(self, mock_popen):
        """Test the run_script() function in main.py"""
        # Send a request to the Flask app
        with app.test_client() as client:
            response = client.get('/')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_popen.call_count, 1)
        self.assertEqual(mock_popen.call_args[0][0], ['python', 'app.py'])

        # Verify the response from the Flask app
        self.assertEqual(response.data.decode('utf-8'), 'Script started')


if __name__ == '__main__':
    unittest.main()
