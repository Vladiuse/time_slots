from datetime import timedelta

from bookings.models import Booking, Slot
from clients.models import Client
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from users.models import User

from .models import Container

WEEKDAY_SHORT = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]


@login_required
def containers_list(request: HttpRequest) -> HttpResponse:
    slots = (
        Slot.objects.filter(date=timezone.localdate())
        .annotate(
            booking_count=Count(
                "bookings",
                filter=~Q(bookings__status=Booking.Status.CANCELLED),
            ),
        )
        .annotate(total_count=F("current_count") + F("booking_count"))
        .order_by("start_time")
    )
    containers = Container.objects.select_related("client").order_by("client__name", "number")
    assert isinstance(request.user, User) # noqa: S101
    if request.user.is_client:
        containers = containers.filter(client=request.user.client_account.client)
    today = timezone.localdate()
    date_pills = [
        {
            "date": today + timedelta(days=offset),
            "weekday": WEEKDAY_SHORT[(today + timedelta(days=offset)).weekday()],
            "is_today": offset == 0,
            "is_active": offset == 0,
        }
        for offset in range(-3, 4)
    ]
    content = {
        "containers": containers,
        "status_on_station": Container.Status.ON_STATION,
        "today": today,
        "slots": slots,
        "date_pills": date_pills,
    }
    return render(request, "containers/container_list.html", content)
