from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    class UserType(models.TextChoices):
        UNIVERSITY = 'university', 'University'
        COMPANY = 'company', 'Company'
        INVESTOR = 'investor', 'Investor'



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
