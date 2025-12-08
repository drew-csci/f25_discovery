from django.test import TestCase
from django.urls import reverse

class GeneralURLTests(TestCase):
    """
    Tests for general application URLs to ensure they are accessible.
    """
    def test_login_page_status_code(self):
        """
        Tests that the login page can be accessed successfully.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_welcome_page_status_code(self):
        """
        Tests that the welcome page can be accessed successfully.
        """
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
