from django.contrib import auth, messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render

from .models import User
from .validators import equals_passwords, range_password


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not equals_passwords(request, password, confirm_password):
            return redirect("/accounts/register")

        if range_password(request, password):
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
                print("Usuário autenticado!")
                auth.login(request, user)
                return redirect("/appone/home")
        else:
            messages.add_message(
                request, constants.ERROR, "E-mail ou senha inválido(a)"
            )

        return render(request, "login.html")
