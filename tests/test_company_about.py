from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import User


class CompanyAboutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company_user = get_user_model().objects.create_user(
            username='testcompany',
            email='company@example.com',
            password='password123',
            user_type=User.UserType.COMPANY
        )
        self.university_user = get_user_model().objects.create_user(
            username='testuniversity',
            email='university@example.com',
            password='password123',
            user_type=User.UserType.UNIVERSITY
        )
        self.company_about_url = reverse('company_about')
        self.login_url = reverse('login')
        self.screen1_url = reverse('screen1')

    def test_company_about_page_access_for_company_user(self):
        """
        Tests that a logged-in company user can access the company about page.
        """
        self.client.login(username='testcompany', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')

    def test_company_about_page_redirects_for_university_user(self):
        """
        Tests that a logged-in university user is redirected from the company about page.
        """
        self.client.login(username='testuniversity', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.screen1_url)

    def test_company_about_page_redirects_for_anonymous_user(self):
        """
        Tests that an anonymous user is redirected to the login page.
        """
        response = self.client.get(self.company_about_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.company_about_url}')

    def test_company_about_page_content(self):
        """
        Tests that the company about page displays the correct content.
        """
        self.client.login(username='testcompany', password='password123')
        response = self.client.get(self.company_about_url)
        
        self.assertContains(response, self.company_user.display_name)
        self.assertContains(response, "To foster innovation by connecting with the brightest academic minds.")
        self.assertContains(response, "We bridge the gap between academic research and industry application, helping to bring groundbreaking ideas to market.")
        self.assertContains(response, self.company_user.email)
