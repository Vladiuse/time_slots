from bookings.models import Booking, Slot
from clients.models import Client
from django.db.models import Count, F, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Container


def containers_list(request: HttpRequest) -> HttpResponse:
    client = Client.objects.get(source_name='ООО "КРАФТТРАНС"')
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
    containers = Container.objects.select_related("client").filter(client=client)
    content = {
        "containers": containers,
        "status_on_station": Container.Status.ON_STATION,
        "today": timezone.localdate(),
        "slots": slots,
    }
    return render(request, "containers/container_list.html", content)
