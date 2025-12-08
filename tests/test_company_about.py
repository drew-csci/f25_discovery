from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanyAboutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company_user = User.objects.create_user(
            username='companyuser',
            email='company@example.com',
            password='password123',
            user_type=User.UserType.COMPANY,
            first_name='Test',
            last_name='Company'
        )
        self.university_user = User.objects.create_user(
            username='universityuser',
            email='university@example.com',
            password='password123',
            user_type=User.UserType.UNIVERSITY,
            first_name='Test',
            last_name='University'
        )
        self.company_about_url = reverse('company_about')
        self.screen1_url = reverse('screen1')
        self.login_url = reverse('login')

    def test_company_user_access_company_about(self):
        """
        Ensure a logged-in company user can access the company about page.
        """
        self.client.login(username='companyuser', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')
        self.assertContains(response, self.company_user.display_name)
        self.assertContains(response, 'Our Mission')
        self.assertContains(response, 'Problems We Solve')
        self.assertContains(response, 'Contact Us')

    def test_non_company_user_redirected_from_company_about(self):
        """
        Ensure a logged-in non-company user (e.g., university user) is redirected.
        """
        self.client.login(username='universityuser', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertRedirects(response, self.screen1_url, status_code=302, target_status_code=200)

    def test_unauthenticated_user_redirected_to_login(self):
        """
        Ensure an unauthenticated user is redirected to the login page.
        """
        response = self.client.get(self.company_about_url)
        expected_redirect_url = f"{self.login_url}?next={self.company_about_url}"
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
