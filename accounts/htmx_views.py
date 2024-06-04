from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from accounts.models import User


def check_email(request):
    email = request.GET.get("email")
    user = User.objects.filter(email=email)
    if user.exists():
        messages.add_message(request, constants.ERROR, _("E-mail already registered"))
    context = {"user": user}
    return render(request, "partials/htmx_components/check_email.html", context)
