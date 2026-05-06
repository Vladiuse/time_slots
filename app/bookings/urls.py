from django.urls import path

from .views import BookingCreateView, BookingListView

app_name = "bookings"

urlpatterns = [
    path("create/", BookingCreateView.as_view(), name="booking_create"),
    path("", BookingListView.as_view(), name="booking_list"),
]
