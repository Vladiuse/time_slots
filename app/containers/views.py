import random
from datetime import timedelta

from bookings.models import Booking, Slot
from clients.models import Client
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from users.models import User

from .models import Container

WEEKDAY_SHORT = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
JOURNAL_FAKE_DAYS_BACK = 30


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
        .order_by("start_time")
    )
    containers = (
        Container.objects.select_related("client")
        .exclude(status=Container.Status.PICKED_UP)
        .order_by("client__name", "number")
    )
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
        for offset in range(7)
    ]
    content = {
        "containers": containers,
        "status_on_station": Container.Status.ON_STATION,
        "today": today,
        "slots": slots,
        "date_pills": date_pills,
    }
    return render(request, "containers/container_list.html", content)


@login_required
def containers_journal(request: HttpRequest) -> HttpResponse:
    containers = (
        Container.objects.select_related("client")
        .filter(status=Container.Status.PICKED_UP)
        .order_by("-number")
    )
    assert isinstance(request.user, User)  # noqa: S101
    if request.user.is_client:
        containers = containers.filter(client=request.user.client_account.client)

    today = timezone.localdate()
    containers_list = list(containers)
    for container in containers_list:
        days_back = random.randint(1, JOURNAL_FAKE_DAYS_BACK)  # noqa: S311
        container.shipped_date = today - timedelta(days=days_back)

    return render(request, "containers/journal_list.html", {"containers": containers_list})
