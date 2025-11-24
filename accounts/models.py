from django.db import models
from django.contrib.auth.models import AbstractUser
# Import get_user_model here, but defer its direct use until needed.
from django.contrib.auth import get_user_model
from django import forms

# Define a placeholder or a function to get the user model when it's safe to do so.
# This helps prevent issues where get_user_model() is called before the app is ready.
def get_custom_user_model():
    return get_user_model()

class User(AbstractUser):
    class UserType(models.TextChoices):
        UNIVERSITY = 'university', 'University'
        COMPANY = 'company', 'Company'
        INVESTOR = 'investor', 'Investor'

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.UNIVERSITY,
    )
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

class InvestorProfile(models.Model):
    # Use the custom user model obtained via the helper function
    user = models.OneToOneField(get_custom_user_model(), on_delete=models.CASCADE, related_name='investor_profile')
    fund_name = models.CharField(max_length=255)
    stages = models.CharField(max_length=255, help_text="e.g., Seed, Series A, Series B")
    ticket_size = models.CharField(max_length=255, help_text="e.g., $100k - $1M")
    therapeutic_areas = models.CharField(max_length=255, help_text="e.g., Oncology, Cardiology")
    geography = models.CharField(max_length=255, help_text="e.g., North America, Europe")

    def __str__(self):
        return f"Investor Profile for {self.user.display_name}"

class CompanyProfile(models.Model):
    user = models.OneToOneField(get_custom_user_model(), on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    # Add other company-specific fields as needed

    def __str__(self):
        return f"Company Profile for {self.company_name}"

class UniversityProfile(models.Model):
    user = models.OneToOneField(get_custom_user_model(), on_delete=models.CASCADE, related_name='university_profile')
    university_name = models.CharField(max_length=255)
    # Add other university-specific fields as needed

    def __str__(self):
        return f"University Profile for {self.university_name}"
