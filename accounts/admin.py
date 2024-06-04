from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_active",
        "last_login",
    ]
    list_filter = ("email", "first_name", "is_superuser", "is_active")
    fieldsets = (
        (
            None,
            {"fields": ("email", "password")},
        ),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = (
        "date_joined",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
