

from django.contrib import admin
from django.urls import path, include
from post.views import home, contact, about

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("post/", include("post.urls")),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
    path("user/", include("user.urls")),
]
