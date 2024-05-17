from django.contrib import admin
from django.contrib.auth import admin as admin_auth_django

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin_auth_django.UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = UserProfile
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {"fields": ("first_name", "last_name", "email", "password")},
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
