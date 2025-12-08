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
