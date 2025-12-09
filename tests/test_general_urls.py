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

    def test_discovery_search_results_display(self):
        """
        Tests that the discovery search page shows Patents and Publications sections
        with dummy items when a query is submitted by an authenticated user.
        """
        from accounts.models import User
        # Create and log in a user, as discovery_search requires authentication
        user = User.objects.create_user(
            username='testuser_search',
            email='testsearch@example.com',
            password='testpassword123',
            user_type=User.UserType.UNIVERSITY # Any user type should work for this view
        )
        self.client.login(email='testsearch@example.com', password='testpassword123')

        # Submit a query that should match some dummy data
        query_term = "secure" # This matches 'Method for Secure Data Transmission' patent
        response = self.client.get(reverse('discovery_search'), {'q': query_term})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Search Results for "secure"</h1>')
        self.assertContains(response, '<h2>Patents (1)</h2>')
        self.assertContains(response, '<h2>Publications (0)</h2>') # 'secure' only matches a patent in dummy data

        # Check for dummy patent content
        self.assertContains(response, 'Method for Secure Data Transmission')
        self.assertContains(response, 'Inventor: John Doe')
        self.assertContains(response, 'Patent No.: US1012345')
        self.assertContains(response, 'A novel method for encrypting and transmitting data over insecure networks using quantum entanglement.')

        # Submit a query that matches publications
        query_term_pub = "quantum" # Matches 'The Future of Quantum Computing' publication
        response = self.client.get(reverse('discovery_search'), {'q': query_term_pub})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Search Results for "quantum"</h1>')
        self.assertContains(response, '<h2>Patents (1)</h2>') # 'quantum' also matches 'quantum entanglement' in patent abstract
        self.assertContains(response, '<h2>Publications (1)</h2>')

        # Check for dummy publication content
        self.assertContains(response, 'The Future of Quantum Computing')
        self.assertContains(response, 'Authors: A. Einstein, N. Bohr')
        self.assertContains(response, 'Journal: Physics Review (2023)')
        self.assertContains(response, 'An overview of recent advancements and challenges in the field of quantum computing.')
