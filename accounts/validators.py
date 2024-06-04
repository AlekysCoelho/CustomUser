from django.contrib import messages
from django.contrib.messages import constants
from django.utils.translation import gettext_lazy as _


def equals_passwords(request, password1, password2):

    if password1 and password2 and password1 != password2:
        messages.add_message(
            request, constants.WARNING, "The two password fields didn’t match."
        )
        return False
    return True


def range_password(request, password):
    if len(password) <= 8 or len(password) >= 32:
        print(f"TAMANO SENHA == {len(password)}")
        messages.add_message(
            request,
            constants.WARNING,
            "The password length must be between 8 and 32 characters.",
        )
        return False
    return True
