from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django import forms

def get_custom_user_model():
    return get_user_model()
from django.contrib.postgres.fields import ArrayField

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


class TTOProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='ttoprofile',
        limit_choices_to={'user_type': User.UserType.UNIVERSITY}
    )
    institution_name = models.CharField(max_length=255, blank=True)
    office_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    therapeutic_focus_tags = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Comma-separated list of therapeutic focus areas (e.g., 'Oncology', 'Cardiology')"
    )
    trl_range_interest_min = models.IntegerField(
        blank=True, null=True,
        help_text="Minimum Technology Readiness Level (TRL) of interest (1-9)"
    )
    trl_range_interest_max = models.IntegerField(
        blank=True, null=True,
        help_text="Maximum Technology Readiness Level (TRL) of interest (1-9)"
    )

    def __str__(self):
        return f"TTO Profile for {self.user.display_name}"

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.UNIVERSITY)
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email

class InvestorProfile(models.Model):
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

    def __str__(self):
        return f"Company Profile for {self.company_name}"

class UniversityProfile(models.Model):
    user = models.OneToOneField(get_custom_user_model(), on_delete=models.CASCADE, related_name='university_profile')
    university_name = models.CharField(max_length=255)

    def __str__(self):
        return f"University Profile for {self.university_name}"
