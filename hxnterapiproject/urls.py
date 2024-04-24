from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from hxnterapiapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", Users, "user")

urlpatterns = [
    path("", include(router.urls)),
    path("login", Users.as_view({"post": "login_user"}), name="login"),
    path("register", Users.as_view({"post": "register_account"}), name="register"),
]
