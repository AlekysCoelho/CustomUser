from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.messages import constants
from django.shortcuts import redirect, render

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


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        email = request.POST.get("email")
        senha = request.POST.get("password")

        user = User.objects.filter(email=email)

        if user.exists():
            user = auth.authenticate(request, email=email, password=senha)
            if user:
                auth.login(request, user)
                return redirect("/appone/home")
        else:
            messages.add_message(
                request, constants.ERROR, "E-mail ou senha inválido(a)"
            )

        return render(request, "login.html")
