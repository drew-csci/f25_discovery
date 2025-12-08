from django.test import TestCase
from django.urls import reverse
from django.core import mail
from accounts.models import User

class EmailSendingTestCase(TestCase):
    def setUp(self):
        # This method runs before each test. It sets up the necessary objects
        # for the test, in this case, a user to test the password reset with.
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_password_reset_email_sent(self):
        """
        Tests that a password reset email is sent to the correct user.
        """
        # Use the test client to simulate a POST request to the password reset URL,
        # mimicking a user submitting the form with their email.
        self.client.post(reverse('password_reset'), {'email': self.user.email})

        # During testing, Django doesn't actually send emails. Instead, it adds
        # them to a special outbox. We check that exactly one email was sent.
        self.assertEqual(len(mail.outbox), 1)

        # Get the email from the outbox.
        sent_email = mail.outbox[0]

        # Verify that the email was sent to the correct recipient.
        self.assertEqual(sent_email.to, [self.user.email])

        # Verify that the email has the expected subject.
        self.assertIn('Password reset', sent_email.subject)
