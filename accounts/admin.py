from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User, InvestorProfile, CompanyProfile, UniversityProfile

class InvestorProfileInline(admin.StackedInline):
    model = InvestorProfile
    can_delete = False
    verbose_name_plural = 'Investor Profile'

class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    can_delete = False
    verbose_name_plural = 'Company Profile'

class UniversityProfileInline(admin.StackedInline):
    model = UniversityProfile
    can_delete = False
    verbose_name_plural = 'University Profile'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (InvestorProfileInline, CompanyProfileInline, UniversityProfileInline)
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_type')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.username:
            obj.username = obj.email
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)

admin.site.register(InvestorProfile)
admin.site.register(CompanyProfile)
admin.site.register(UniversityProfile)
