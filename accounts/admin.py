from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, TTOProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Meta'), {'fields': ('user_type', 'username')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'user_type')}),
    )
    list_display = ('email', 'user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(TTOProfile)
class TTOProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution_name', 'country', 'therapeutic_focus_tags')
    search_fields = ('institution_name', 'user__email', 'therapeutic_focus_tags')
    raw_id_fields = ('user',)
