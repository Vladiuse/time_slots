from django.urls import path

from containers import views

app_name = "containers"

urlpatterns = [
    path("", views.containers_list, name="containers_list"),
]
