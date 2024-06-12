import re

from django.contrib import messages
from django.contrib.messages import constants
from django.utils.translation import gettext_lazy as _


class ValidatorPassword:
    def __init__(self, request, password1, password2):
        self.password1 = password1
        self.password2 = password2
        self.request = request
        self.is_valid = True

    def password_empty(self):
        if not self.password1 or not self.password2:
            messages.add_message(
                self.request, constants.ERROR, _("The password field is empty.")
            )
            self.is_valid = False

    def range_password(self):
        if not (8 <= len(self.password1) <= 32):
            messages.add_message(
                self.request,
                constants.ERROR,
                _("The password length must be between 8 and 32 characters."),
            )
            self.is_valid = False

    def number_validator(self):
        if not re.search(r"\d", self.password1):
            messages.add_message(
                self.request,
                constants.ERROR,
                _("The password must contain at least 1 digit, 0-9."),
            )
            self.is_valid = False

    def uppercase_validate(self):
        if not re.search(r"[A-Z]", self.password1):
            messages.add_message(
                self.request,
                constants.ERROR,
                _("The password must contain at least 1 uppercase letter, A-Z."),
            )
            self.is_valid = False

    def symbol_validate(self):
        if not re.search(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', self.password1):
            messages.add_message(
                self.request,
                constants.ERROR,
                _(
                    "The password must contain at least 1 special character: ()[]{}|\`~!@#$%^&*_-+=;:'\",<>./ "
                ),
            )
            self.is_valid = False

    def equals_passwords(self):
        if self.password1 != self.password2:
            messages.add_message(
                self.request,
                constants.ERROR,
                _("The two password fields didn’t match."),
            )
            self.is_valid = False

    def verified(self):
        self.password_empty()
        if not self.is_valid:
            return False
        self.range_password()
        if not self.is_valid:
            return False
        self.number_validator()
        if not self.is_valid:
            return False
        self.uppercase_validate()
        if not self.is_valid:
            return False
        self.symbol_validate()
        if not self.is_valid:
            return False
        self.equals_passwords()
        return self.is_valid
