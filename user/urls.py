from django.urls import path
from user.views import login, logout, register, profile

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
]
