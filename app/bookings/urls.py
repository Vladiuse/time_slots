from django.urls import path

from .views import BookingCreateView, BookingDeleteView, BookingListView

app_name = "bookings"

urlpatterns = [
    path("create/", BookingCreateView.as_view(), name="booking_create"),
    path("<int:pk>/delete/", BookingDeleteView.as_view(), name="booking_delete"),
    path("", BookingListView.as_view(), name="booking_list"),
]
