from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Create and save a User with the given email, first name, last name and password.
        """
        if not first_name:
            raise ValueError(_("The field first name is required."))
        if not last_name:
            raise ValueError(_("The field last name is requited."))

        if not email:
            raise ValueError(_("An email address is required."))

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(first_name, last_name, email, password, **extra_fields)

    def create_superuser(
        self, first_name, last_name, email, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(first_name, last_name, email, password, **extra_fields)
