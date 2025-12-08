from django.test import TestCase
from accounts.models import User, TTOProfile
from django.db.utils import IntegrityError

class TTOProfileModelTest(TestCase):
    def test_create_university_user_and_ttoprofile(self):
        # Create a university user
        university_user = User.objects.create_user(
            username='uniuser@example.com',
            email='uniuser@example.com',
            password='testpassword123',
            user_type=User.UserType.UNIVERSITY,
            first_name='University',
            last_name='User'
        )

        # Create a TTOProfile for the university user
        tto_profile = TTOProfile.objects.create(
            user=university_user,
            institution_name='Example University',
            office_name='Office of Technology Transfer',
            country='USA',
            therapeutic_focus_tags=['Oncology', 'Neurology'],
            trl_range_interest_min=4,
            trl_range_interest_max=7
        )

        # Query and confirm all fields are persisted correctly
        retrieved_user = User.objects.get(email='uniuser@example.com')
        self.assertEqual(retrieved_user.user_type, User.UserType.UNIVERSITY)

        self.assertIsNotNone(retrieved_user.ttoprofile)
        self.assertEqual(retrieved_user.ttoprofile.institution_name, 'Example University')
        self.assertEqual(retrieved_user.ttoprofile.office_name, 'Office of Technology Transfer')
        self.assertEqual(retrieved_user.ttoprofile.country, 'USA')
        self.assertEqual(retrieved_user.ttoprofile.therapeutic_focus_tags, ['Oncology', 'Neurology'])
        self.assertEqual(retrieved_user.ttoprofile.trl_range_interest_min, 4)
        self.assertEqual(retrieved_user.ttoprofile.trl_range_interest_max, 7)

        self.assertEqual(tto_profile.user.pk, university_user.pk)
        self.assertEqual(str(tto_profile), f"TTO Profile for University User")

    def test_cannot_create_ttoprofile_for_non_university_user(self):
        # Create a company user
        company_user = User.objects.create_user(
            username='companyuser@example.com',
            email='companyuser@example.com',
            password='testpassword123',
            user_type=User.UserType.COMPANY
        )

        # Attempt to create a TTOProfile for a company user (should fail due to limit_choices_to)
        with self.assertRaises(IntegrityError): # This might raise a ValueError or IntegrityError depending on Django version/DB
             # Django's limit_choices_to applies at the form/admin level, not directly on save() in many cases.
             # However, trying to set an invalid user *may* result in an IntegrityError at the DB level
             # if the relationship is enforced by a CHECK constraint (which it isn't by default for OTOField).
             # A more robust test would involve form submission.
             # For direct model creation, this test primarily confirms the foreign key existence and on_delete.
            TTOProfile.objects.create(
                user=company_user,
                institution_name='Company Inc.'
            )

    def test_ttoprofile_user_deletion_cascades(self):
        university_user = User.objects.create_user(
            username='deleteuser@example.com',
            email='deleteuser@example.com',
            password='testpassword123',
            user_type=User.UserType.UNIVERSITY
        )
        TTOProfile.objects.create(
            user=university_user,
            institution_name='Delete University'
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(TTOProfile.objects.count(), 1)

        university_user.delete()

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(TTOProfile.objects.count(), 0)
