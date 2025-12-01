from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import UserRegistrationForm, EmailAuthenticationForm, InvestorProfileForm
from .models import User, InvestorProfile
from django.views.generic import FormView
from .forms import UserRegistrationForm, EmailAuthenticationForm
from accounts.models import User

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        user_type = form.cleaned_data.get('user_type')

        if user_type == User.UserType.INVESTOR:
            if not hasattr(user, 'investor_profile'):
                InvestorProfile.objects.create(user=user)
            messages.success(self.request, f"Investor account created successfully. Please log in.")
        elif user_type == User.UserType.COMPANY:
            pass
        elif user_type == User.UserType.UNIVERSITY:
            pass

        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = False # Temporarily set to False for debugging

    def get_success_url(self):
        if self.request.user.user_type == User.UserType.INVESTOR:
            return reverse_lazy('investor_profile')
        if self.request.user.is_authenticated and self.request.user.user_type == User.UserType.COMPANY:
            return reverse_lazy('company_home')
        return reverse_lazy('screen1')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('login')

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
        profile = None
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
                'profile': profile,
                'form': form,
                'user': user,
            }
            return render(request, self.template_name, context)
