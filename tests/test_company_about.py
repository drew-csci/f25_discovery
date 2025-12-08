from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanyAboutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company_user = User.objects.create_user(
            username='companyuser',
            email='company@example.com',
            password='password123',
            user_type=User.UserType.COMPANY,
            first_name='Company',
            last_name='User'
        )
        self.university_user = User.objects.create_user(
            username='universityuser',
            email='university@example.com',
            password='password123',
            user_type=User.UserType.UNIVERSITY,
            first_name='University',
            last_name='User'
        )
        self.investor_user = User.objects.create_user(
            username='investoruser',
            email='investor@example.com',
            password='password123',
            user_type=User.UserType.INVESTOR,
            first_name='Investor',
            last_name='User'
        )
        self.company_about_url = reverse('company_about')
        self.screen1_url = reverse('screen1')

    def test_company_about_access_control(self):
        # Test access for a university user
        self.client.login(username='universityuser', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertRedirects(response, self.screen1_url, status_code=302, target_status_code=200)

        # Test access for an investor user
        self.client.logout() # Logout university user
        self.client.login(username='investoruser', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertRedirects(response, self.screen1_url, status_code=302, target_status_code=200)

        # Test access for a company user (should be allowed)
        self.client.logout() # Logout investor user
        self.client.login(username='companyuser', password='password123')
        response = self.client.get(self.company_about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')

    def test_company_about_unauthenticated_access(self):
        # Test access for an unauthenticated user
        response = self.client.get(self.company_about_url)
        # Unauthenticated users should be redirected to the login page
        login_url = reverse('login') + f'?next={self.company_about_url}'
        self.assertRedirects(response, login_url, status_code=302, target_status_code=200)
