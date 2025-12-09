from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import User as CustomUser # Alias to avoid conflict with TestCase's User

class CompanyAboutAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company_user = get_user_model().objects.create_user(
            username='companyuser@example.com',
            email='companyuser@example.com',
            password='testpassword123',
            user_type=CustomUser.UserType.COMPANY
        )
        self.university_user = get_user_model().objects.create_user(
            username='universityuser@example.com',
            email='universityuser@example.com',
            password='testpassword123',
            user_type=CustomUser.UserType.UNIVERSITY
        )

    def test_company_user_can_access_company_about(self):
        self.client.login(email='companyuser@example.com', password='testpassword123')
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')

    def test_non_company_user_redirects_from_company_about(self):
        self.client.login(email='universityuser@example.com', password='testpassword123')
        # Step 1: Request company_about as a university user
        response = self.client.get(reverse('company_about'))

        # Expect an initial redirect (302) from company_about to screen1
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('screen1'), response['Location'])

        # Manually follow the first redirect to screen1
        response_screen1 = self.client.get(response['Location'])

        # Expect a second redirect (302) from screen1 to university_home for university users
        self.assertEqual(response_screen1.status_code, 302)
        self.assertIn(reverse('university_home'), response_screen1['Location'])

        # Manually follow the second redirect to university_home
        response_university_home = self.client.get(response_screen1['Location'])

        # Expect the final page (university_home) to be rendered successfully (200)
        self.assertEqual(response_university_home.status_code, 200)
        self.assertTemplateUsed(response_university_home, 'pages/university_home.html')
        # Optional: Assert some content to ensure it's the correct page
        # self.assertContains(response_university_home, "University Home Page") # Adjust text if needed

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 302) # Expect a redirect
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('company_about')}")


class DiscoverySearchTests(TestCase):
    """
    Tests for the global discovery search functionality.
    """
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser_search',
            email='testsearch@example.com',
            password='testpassword123',
            user_type=CustomUser.UserType.UNIVERSITY # Any user type should work for this view
        )

    def test_discovery_search_results_display(self):
        """
        Tests that the discovery search page shows Patents and Publications sections
        with dummy items when a query is submitted by an authenticated user.
        """
        self.client.login(email='testsearch@example.com', password='testpassword123')

        # Submit a query that should match some dummy data
        query_term = "secure" # This matches 'Method for Secure Data Transmission' patent
        response = self.client.get(reverse('discovery_search'), {'q': query_term})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="text-3xl font-bold mb-6 text-gray-800">Search Results for "secure"</h1>')
        self.assertContains(response, '<h2 class="text-2xl font-semibold mb-4 text-gray-700">Patents (1)</h2>')
        self.assertContains(response, '<h2 class="text-2xl font-semibold mb-4 text-gray-700">Publications (0)</h2>') # 'secure' only matches a patent in dummy data
        self.assertContains(response, 'No publications found matching your query.') # Explicitly check for no publications message

        # Check for dummy patent content
        self.assertContains(response, 'Method for Secure Data Transmission')
        self.assertContains(response, '<strong>Inventor:</strong> John Doe')
        self.assertContains(response, 'Patent No.: US1012345')
        self.assertContains(response, 'A novel method for encrypting and transmitting data over insecure networks using quantum entanglement.')

        # Submit a query that matches publications
        query_term_pub = "quantum" # Matches 'The Future of Quantum Computing' publication
        response = self.client.get(reverse('discovery_search'), {'q': query_term_pub})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="text-3xl font-bold mb-6 text-gray-800">Search Results for "quantum"</h1>')
        self.assertContains(response, '<h2 class="text-2xl font-semibold mb-4 text-gray-700">Patents (1)</h2>') # 'quantum' also matches 'quantum entanglement' in patent abstract
        self.assertContains(response, '<h2 class="text-2xl font-semibold mb-4 text-gray-700">Publications (1)</h2>')

        # Check for dummy publication content
        self.assertContains(response, 'The Future of Quantum Computing')
        self.assertContains(response, '<strong>Authors:</strong> A. Einstein, N. Bohr')
        self.assertContains(response, 'Journal: Physics Review (2023)')
        self.assertContains(response, 'An overview of recent advancements and challenges in the field of quantum computing.')
