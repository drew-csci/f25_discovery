from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
import uuid

class User(AbstractUser):
    class UserType(models.TextChoices):
        UNIVERSITY = 'university', 'University'
        COMPANY = 'company', 'Company'
        INVESTOR = 'investor', 'Investor'

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.UNIVERSITY)
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # keep username for admin compatibility

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email

    def send_verification_email(self):
        """Sends an email to the user to verify their email address."""
        verification_url = settings.SITE_URL + reverse('email_verify', kwargs={'token': str(self.email_verification_token)})
        subject = 'Verify Your Email Address'
        message = render_to_string('accounts/email_verification_email.html', {
            'user': self,
            'verification_url': verification_url,
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]

        send_mail(subject, message, from_email, recipient_list, html_message=message)
