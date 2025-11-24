from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class UserType(models.TextChoices):
        UNIVERSITY = 'university', 'University'
        COMPANY = 'company', 'Company'
        INVESTOR = 'investor', 'Investor'

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.UNIVERSITY)
    email = models.EmailField(unique=True)

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

class TTOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='ttoprofile')
    institution_name = models.CharField(max_length=255, blank=True)
    office_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    therapeutic_focus_tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags, e.g., 'Oncology, Neurology'")
    trl_range_interest = models.CharField(max_length=100, blank=True, help_text="e.g., 'TRL 1-3, TRL 4-6'")

    def __str__(self):
        return f"{self.institution_name} TTO Profile ({self.user.email})"
