from urllib import request

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.messages import constants
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .tokens import account_activate_token
from .validators import ValidatorPassword

User = get_user_model()


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        validate_password = ValidatorPassword(request, password, confirm_password)

        if validate_password.verified():
            try:
                User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )
                return redirect("/accounts/login")
            except:
                return redirect("/accounts/register")
        else:
            return redirect("/accounts/register")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email=email)

        if user.exists():
            user = auth.authenticate(request, email=email, password=password)
            if user:
                auth.login(request, user)
                return redirect("/appone/home")
        else:
            messages.add_message(request, constants.ERROR, "Invalid email or password.")

        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/accounts/login")


def password_reset(request):
    """Recover password."""

    if request.method == "GET":
        return render(request, "password_reset.html")
    elif request.method == "POST":
        user = User.objects.filter(email="reus__black@outlook.com")
        email = request.POST.get("email")

        if not user.exists():

            messages.add_message(request, constants.ERROR, "Email not registered.")
            return redirect("/accounts/password_reset")
        else:
            user = user.first()
            try:

                html_content = render_to_string(
                    "confirm_password_reset.html",
                    {
                        "user": user.first_name,
                        "domain": get_current_site(request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activate_token.make_token(user),
                        "protocol": "https" if request.is_secure() else "http",
                    },
                )
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    "Change password",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                encode = urlsafe_base64_encode(force_bytes(user.pk))
                return redirect("verification_sent", user_id=encode)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return redirect("/accounts/password_reset")


def verification_sent(request, user_id):
    decode_id = force_str(urlsafe_base64_decode(user_id))
    user = get_user_model().objects.get(id=decode_id)
    context = {"user": user}
    return render(request, "verification_sent.html", context)


def change_password(request, uidb64, token):
    if request.method == "GET":
        context = {"uid": uidb64, "token": token}
        return render(request, "change_password.html", context)
    if request.method == "POST":
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
            user.set_password("")
            user.save(update_fields=["password"])
        except User.DoesNotExist:
            user = None

        if user is not None and account_activate_token.check_token(user, token):
            if request.method == "POST":

                password = request.POST.get("new_password")
                confirm_password = request.POST.get("confirm_password")

                validate_password = ValidatorPassword(
                    request, password, confirm_password
                )

                if validate_password.verified():
                    try:
                        user.set_password(password)
                        user.save(update_fields=["password"])
                        user = get_object_or_404(User, pk=uid)

                        messages.add_message(
                            request,
                            constants.SUCCESS,
                            "Your password has been changed successfully.",
                        )
                        return redirect("/accounts/login")
                    except:
                        return redirect(f"/accounts/change_password/{uidb64}/{token}")
                else:
                    return redirect(f"/accounts/change_password/{uidb64}/{token}")
        else:
            messages.add_message(request, constants.ERROR, "Links is expired.")
            return render(request, "password_reset_failed.html")
