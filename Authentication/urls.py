from django.urls import path
from .views import (
    register_user_view,
    login_user_view,
    logout_user_view,
    contact_us_view,
)

app_name = "Authentication"

urlpatterns = [
    path("register_user/", register_user_view, name="register_user"),
    path("login/", login_user_view, name="login_user"),
    path("logout/", logout_user_view, name="logout_user"),
    path("contact_us/", contact_us_view, name="contact_us"),
]
