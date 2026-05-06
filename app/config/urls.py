from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("containers/", include("containers.urls")),
    path("bookings/", include("bookings.urls")),
]
