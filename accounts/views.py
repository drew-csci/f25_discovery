from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, View
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegistrationForm, EmailAuthenticationForm
from .models import User

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    # success_url = reverse_lazy('screen1') # This will be changed to a pending verification page

    def form_valid(self, form):
        user = form.save()
        user.send_verification_email()
        # Instead of logging in immediately, redirect to a page indicating verification is needed.
        messages.success(self.request, 'A verification email has been sent. Please check your inbox.')
        return redirect('email_verification_pending') # Redirect to the pending verification page

    def get_initial(self):
        initial = super().get_initial()
        user_type = self.request.GET.get('type') or self.request.session.get('selected_user_type')
        if user_type:
            initial['user_type'] = user_type
        return initial

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        # Check if the user's email is verified before redirecting
        if self.request.user.is_authenticated and not self.request.user.is_email_verified:
            messages.warning(self.request, 'Please verify your email address to continue.')
            return reverse_lazy('email_verification_pending') # Redirect to a pending verification page
        return reverse_lazy('screen1')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.request.GET.get('type')
        if user_type:
            self.request.session['selected_user_type'] = user_type
        context['selected_user_type'] = user_type
        return context

class EmailVerifyView(View):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            if not user.is_email_verified:
                user.is_email_verified = True
                user.email_verification_token = None  # Clear the token after verification
                user.save()
                messages.success(request, 'Your email address has been successfully verified. You can now log in.')
                return redirect('login')
            else:
                messages.info(request, 'Your email address has already been verified.')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid verification link or token expired.')
            return redirect('login') # Or a page indicating the error

# A placeholder view for when email verification is pending
class EmailVerificationPendingView(View):
    def get(self, request):
        # If the user is already logged in and verified, redirect them to screen1
        if request.user.is_authenticated and request.user.is_email_verified:
            return redirect('screen1')
        # If the user is logged in but not verified, show them the pending page
        elif request.user.is_authenticated and not request.user.is_email_verified:
            return render(request, 'accounts/email_verification_pending.html')
        # If the user is not logged in, redirect them to login
        else:
            return redirect('login')

class ResendVerificationEmailView(View):
    def post(self, request):
        email = request.POST.get('email') # Assuming the form in email_verification_pending.html will have an email field
        if not email:
            messages.error(request, "Email address is required to resend verification.")
            return redirect('email_verification_pending')

        try:
            user = User.objects.get(email__iexact=email, is_email_verified=False)
            user.send_verification_email()
            messages.success(request, f"A new verification email has been sent to {email}. Please check your inbox.")
        except User.DoesNotExist:
            messages.error(request, "No unverified account found with that email address.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('email_verification_pending')
