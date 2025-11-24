from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from .models import InvestorProfile

User = get_user_model()

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

class InvestorProfileForm(forms.ModelForm):
    class Meta:
        model = InvestorProfile
        fields = ['fund_name', 'stages', 'ticket_size', 'therapeutic_areas', 'geography']
        # You might want to customize widgets here if needed
        # widgets = {
        #     'stages': forms.TextInput(attrs={'placeholder': 'e.g., Seed, Series A, Series B'}),
        #     'ticket_size': forms.TextInput(attrs={'placeholder': 'e.g., $100k - $1M'}),
        #     'therapeutic_areas': forms.TextInput(attrs={'placeholder': 'e.g., Oncology, Cardiology'}),
        #     'geography': forms.TextInput(attrs={'placeholder': 'e.g., North America, Europe'}),
        # }
