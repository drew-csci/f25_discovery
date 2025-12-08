from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from django.contrib.auth import get_user_model

# Assuming a Project model exists and is used by the company_home view.
# If this model is not defined, these tests might need adjustment or a mock.
# For simplicity, we'll assume the view passes a 'projects' context and
# the template displays project titles if available.

class CompanyHomeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company_user = get_user_model().objects.create_user(
            username='companyuser',
            email='company@example.com',
            password='password123',
            user_type=User.UserType.COMPANY
        )
        self.university_user = get_user_model().objects.create_user(
            username='universityuser',
            email='university@example.com',
            password='password123',
            user_type=User.UserType.UNIVERSITY
        )
        self.investor_user = get_user_model().objects.create_user(
            username='investoruser',
            email='investor@example.com',
            password='password123',
            user_type=User.UserType.UNIVERSITY # Use a valid UserType for non-company user
        )
        self.company_home_url = reverse('company_home')

    def test_company_home_access_control(self):
        """
        Confirms that only authenticated company users can view /company/home/,
        while other user types or unauthenticated visitors are redirected appropriately.
        """
        # Unauthenticated user should be redirected to login
        response = self.client.get(self.company_home_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

        # University user should be redirected (e.g., to screen1 or login if login_required redirect)
        self.client.login(email='university@example.com', password='password123')
        response = self.client.get(self.company_home_url)
        self.assertEqual(response.status_code, 302)
        # Assuming the default login_required redirect for non-company users goes to screen1
        self.assertIn(reverse('screen1'), response.url)
        self.client.logout()

        # Investor user should be redirected
        self.client.login(email='investor@example.com', password='password123')
        response = self.client.get(self.company_home_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('screen1'), response.url)
        self.client.logout()

        # Authenticated company user should access the page successfully
        self.client.login(email='company@example.com', password='password123')
        response = self.client.get(self.company_home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_home.html')
        self.client.logout()

    def test_company_home_template_rendering(self):
        """
        Confirms the correct template is used and the page displays expected elements.
        """
        self.client.login(email='company@example.com', password='password123')
        response = self.client.get(self.company_home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_home.html')
        self.assertContains(response, 'Welcome, companyuser!') # Example welcome message
        self.assertContains(response, '<input type="search"', html=True) # Search bar
        self.assertContains(response, 'id="project-list"') # Assuming a div for project list
        self.client.logout()

    def test_company_home_empty_result_handling(self):
        """
        Confirms that when no projects match, a clear 'No projects found' message is shown.
        This test assumes the view passes an empty list of projects, and the template handles it.
        """
        self.client.login(email='company@example.com', password='password123')
        # Simulate a scenario where no projects are returned by the view (e.g., via a query parameter)
        # For a more robust test, one would mock the queryset or create no projects.
        # For now, we'll assume the template has a conditional for this.
        response = self.client.get(self.company_home_url) # Without any specific query, it might show projects
        self.assertEqual(response.status_code, 200)
        # If the view logic correctly handles empty search results, this message should appear.
        # This might require a change to the company_home view to pass an explicit empty projects list
        # or a specific context variable to trigger this state if search is not yet implemented.
        self.assertNotContains(response, 'No projects found matching your criteria.') # Should NOT be present if projects exist

        # To properly test empty results with a search, the view would need to implement search.
        # Assuming a search parameter like 'q' can lead to no results:
        response_empty_search = self.client.get(self.company_home_url + '?q=nonexistentproject')
        self.assertEqual(response_empty_search.status_code, 200)
        self.assertContains(response_empty_search, 'No projects found matching your criteria.') # Should be present for empty search
        self.client.logout()

    # Note: Search and filter features will require actual Project models and view logic
    # to be fully tested. The 'empty result handling' partially covers this.
    # For a complete test, you would:
    # 1. Create several Project instances with varying attributes.
    # 2. Make requests to company_home_url with search queries and filter parameters.
    # 3. Assert that the response contains the expected project titles/details and
    #    does not contain those that should be filtered out.
