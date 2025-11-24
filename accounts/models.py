from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ChoiceField, RadioSelect
# Import get_user_model here to ensure it's available when needed
from django.contrib.auth import get_user_model
from django import forms # Import forms module

# Get the custom user model
User = get_user_model()

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_profile')
    fund_name = models.CharField(max_length=255)
    stages = models.CharField(max_length=255, help_text="e.g., Seed, Series A, Series B")
    ticket_size = models.CharField(max_length=255, help_text="e.g., $100k - $1M")
    therapeutic_areas = models.CharField(max_length=255, help_text="e.g., Oncology, Cardiology")
    geography = models.CharField(max_length=255, help_text="e.g., North America, Europe")

    def __str__(self):
        return f"Investor Profile for {self.user.display_name}"

# Assuming CompanyProfile and UniversityProfile are also needed,
# and that they should be defined in this file as well.
class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    # Add other company-specific fields as needed

    def __str__(self):
        return f"Company Profile for {self.company_name}"

class UniversityProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='university_profile')
    university_name = models.CharField(max_length=255)
    # Add other university-specific fields as needed

    def __str__(self):
        return f"University Profile for {self.university_name}"

# Forms (assuming these are still relevant and need to be kept)
# Note: These forms are defined here for completeness, but the issue was likely with
# how Django's internal auth forms were trying to access the user model.
# The fix in settings.py and ensuring accounts is loaded correctly should resolve it.
class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.UserType.choices, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('user_type', 'first_name', 'last_name', 'email')

class EmailAuthenticationForm(AuthenticationForm):
    # Field is still named "username" internally; label it clearly as Email.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({'placeholder': 'you@example.com', 'autofocus': True})

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Use email directly for lookup, as it's the username field
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("This email is not associated with any account.")
        return email
