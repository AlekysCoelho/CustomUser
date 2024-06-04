from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), max_length=100, unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_("Designates wheter this user can log into this admin site."),
    )
    # is_staff = models.BooleanField(
    #     _("staff status"),
    #     default=False,
    #     help_text=_("Designates whether the user can log into this admin site."),
    # )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    # is_verified = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}"

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin
