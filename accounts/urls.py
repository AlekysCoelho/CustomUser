from django.urls import path

from . import htmx_views, views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
]

htmx_urlpatterns = [
    path("check_email/", htmx_views.check_email, name="check_email"),
]

urlpatterns += htmx_urlpatterns
