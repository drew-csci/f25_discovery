from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, View
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import UserRegistrationForm, EmailAuthenticationForm, InvestorProfileForm
from .models import User, InvestorProfile

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login') # Redirect to login after registration

    def form_valid(self, form):
        user = form.save()
        user_type = form.cleaned_data.get('user_type')

        if user_type == User.UserType.INVESTOR:
            # Create an InvestorProfile for the new investor user
            InvestorProfile.objects.create(user=user)
            messages.success(self.request, f"Investor account created successfully. Please log in.")
        elif user_type == User.UserType.COMPANY:
            # Handle company profile creation if needed
            pass
        elif user_type == User.UserType.UNIVERSITY:
            # Handle university profile creation if needed
            pass

        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirect investors to their profile page after login
        if self.request.user.user_type == User.UserType.INVESTOR:
            return reverse_lazy('investor_profile')
        # Default redirect for other user types
        return reverse_lazy('screen1') # Or wherever you want to redirect

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('login') # Redirect to login page after logout

class InvestorProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/investor_profile.html'
    form_class = InvestorProfileForm
    model = InvestorProfile

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = user.investor_profile
            form = self.form_class(instance=profile)
        except InvestorProfile.DoesNotExist:
            form = self.form_class()
            profile = None

        context = {
            'profile': profile,
            'form': form,
            'user': user,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = user.investor_profile
            form = self.form_class(request.POST, instance=profile)
        except InvestorProfile.DoesNotExist:
            form = self.form_class(request.POST)

        if form.is_valid():
            investor_profile = form.save(commit=False)
            investor_profile.user = user
            investor_profile.save()
            messages.success(request, "Investor profile updated successfully.")
            return HttpResponseRedirect(reverse_lazy('investor_profile'))
        else:
            messages.error(request, "Please correct the errors below.")
            context = {
                'profile': profile if 'profile' in locals() else None,
                'form': form,
                'user': user,
            }
            return render(request, self.template_name, context)
