from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("containers/", include("containers.urls")),
    path("clients/", include("clients.urls")),
    path("bookings/", include("bookings.urls")),
]
