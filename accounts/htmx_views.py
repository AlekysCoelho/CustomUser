from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages import constants
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def check_email(request):
    email = request.GET.get("email")
    user = get_user_model().objects.filter(email=email)
    if user.exists():
        messages.add_message(request, constants.ERROR, _("Email already registered"))
    context = {"user": user}
    return render(request, "partials/htmx_components/check_email.html", context)
