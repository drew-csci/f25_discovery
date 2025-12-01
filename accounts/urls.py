from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .forms import EmailAuthenticationForm, CustomPasswordResetForm
from .views import RegisterView, CustomLoginView, LogoutView, InvestorProfileView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Password reset URLs
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html',
             form_class=CustomPasswordResetForm,
             email_template_name='accounts/password_reset_email.html', # Ensure this template exists
             subject_template_name='accounts/password_reset_subject.txt' # Ensure this template exists
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             # success_url='/accounts/reset/complete/' # Define success_url if needed
         ),
         name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # Investor Profile URL
    path('profile/investor/', InvestorProfileView.as_view(), name='investor_profile'),
]
