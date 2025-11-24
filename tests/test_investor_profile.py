from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from accounts.models import InvestorProfile
from accounts.admin import InvestorProfileInline, UserAdmin

# Use get_user_model() to ensure we are using the custom user model
User = get_user_model()

class InvestorProfileAdminTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create admin user once for the class to avoid duplicate key errors
        cls.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='password123',
            is_email_verified=True
        )
        # Create an investor user for the class
        cls.investor_user_for_class = User.objects.create_user(
            email='investor_class@example.com',
            username='investor_class',
            password='password123',
            user_type=User.UserType.INVESTOR,
            is_email_verified=True
        )
        InvestorProfile.objects.create(user=cls.investor_user_for_class)

    @classmethod
    def tearDownClass(cls):
        # Clean up users created in setUpClass
        User.objects.filter(email__in=['admin@example.com', 'investor_class@example.com', 'newinvestor@example.com']).delete()
        InvestorProfile.objects.filter(user__email__in=['admin@example.com', 'investor_class@example.com', 'newinvestor@example.com']).delete()
        super().tearDownClass()

    def setUp(self):
        self.client = Client()
        self.admin_site = AdminSite()
        self.user_admin = UserAdmin(User, self.admin_site)

    def test_investor_profile_inline_in_admin(self):
        """Test that InvestorProfile is available as an inline in UserAdmin."""
        self.assertIn(InvestorProfileInline, self.user_admin.inlines)

    def test_create_investor_user_via_admin(self):
        """Test creating an investor user through the Django admin interface."""
        self.client.login(email='admin@example.com', password='password123')
        
        add_user_url = reverse('admin:accounts_user_add')
        
        user_data = {
            'email': 'newinvestor@example.com',
            'username': 'newinvestor',
            'first_name': 'New',
            'last_name': 'Investor',
            'user_type': User.UserType.INVESTOR,
            'password': 'newpassword123',
            'password2': 'newpassword123',
            'is_email_verified': True
        }
        
        response = self.client.post(add_user_url, user_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='newinvestor@example.com').exists())
        
        new_investor = User.objects.get(email='newinvestor@example.com')
        self.assertTrue(InvestorProfile.objects.filter(user=new_investor).exists())

class InvestorProfileUITest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an investor user
        self.investor_user = User.objects.create_user(
            email='investor@example.com',
            username='investor',
            password='password123',
            user_type=User.UserType.INVESTOR,
            is_email_verified=True
        )
        # Ensure InvestorProfile is created for the investor user
        self.investor_profile = InvestorProfile.objects.create(
            user=self.investor_user,
            fund_name='Test Fund',
            stages='Seed, Series A',
            ticket_size='$1M - $5M',
            therapeutic_areas='Oncology, Neurology',
            geography='North America'
        )

    def tearDown(self):
        # Clean up users created in setUp to prevent duplicate key errors on subsequent test runs
        # This is crucial for TestCase as setUp runs before each test.
        User.objects.filter(email='investor@example.com').delete()
        InvestorProfile.objects.filter(user__email='investor@example.com').delete()


    def test_fill_and_save_investor_profile_ui(self):
        """Test filling and saving investor profile data through the UI."""
        self.client.login(email='investor@example.com', password='password123')
        
        profile_url = reverse('investor_profile')
        
        updated_data = {
            'fund_name': 'Updated Test Fund',
            'stages': 'Series B, C',
            'ticket_size': '$5M - $10M',
            'therapeutic_areas': 'Cardiology',
            'geography': 'Europe'
        }
        
        response = self.client.post(profile_url, updated_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, profile_url)
        
        self.investor_user.refresh_from_db()
        updated_profile = InvestorProfile.objects.get(user=self.investor_user)
        
        self.assertEqual(updated_profile.fund_name, 'Updated Test Fund')
        self.assertEqual(updated_profile.stages, 'Series B, C')
        self.assertEqual(updated_profile.ticket_size, '$5M - $10M')
        self.assertEqual(updated_profile.therapeutic_areas, 'Cardiology')
        self.assertEqual(updated_profile.geography, 'Europe')

    def test_view_investor_profile_data_on_reload(self):
        """Test that data appears correctly on reload after saving."""
        self.client.login(email='investor@example.com', password='password123')
        profile_url = reverse('investor_profile')
        
        response_get = self.client.get(profile_url)
        self.assertEqual(response_get.status_code, 200)
        self.assertContains(response_get, 'Test Fund')
        self.assertContains(response_get, 'Seed, Series A')
        self.assertContains(response_get, '$1M - $5M')
        self.assertContains(response_get, 'Oncology, Neurology')
        self.assertContains(response_get, 'North America')

        updated_data = {
            'fund_name': 'Reload Test Fund',
            'stages': 'Series B',
            'ticket_size': '$10M+',
            'therapeutic_areas': 'Dermatology',
            'geography': 'Asia'
        }
        response_post = self.client.post(profile_url, updated_data)
        self.assertEqual(response_post.status_code, 302)

        response_reload = self.client.get(profile_url)
        self.assertEqual(response_reload.status_code, 200)
        self.assertContains(response_reload, 'Reload Test Fund')
        self.assertContains(response_reload, 'Series B')
        self.assertContains(response_reload, '$10M+')
        self.assertContains(response_reload, 'Dermatology')
        self.assertContains(response_reload, 'Asia')
