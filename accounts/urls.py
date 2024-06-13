from django.urls import path

from . import htmx_views, views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout, name="logout"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path(
        "verification_sent/<str:user_id>",
        views.verification_sent,
        name="verification_sent",
    ),
    path(
        "change_password/<uidb64>/<token>",
        views.change_password,
        name="change_password",
    ),
]

htmx_urlpatterns = [
    path("check_email/", htmx_views.check_email, name="check_email"),
]

urlpatterns += htmx_urlpatterns
