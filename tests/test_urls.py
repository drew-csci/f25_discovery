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
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 302) # Expect a redirect
        self.assertRedirects(response, reverse('screen1'))

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 302) # Expect a redirect
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('company_about')}")
