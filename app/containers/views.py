from datetime import date

from bookings.models import Booking, Slot
from clients.models import Client
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Container


def containers_list(request: HttpRequest) -> HttpResponse:
    client = Client.objects.get(source_name='ООО "КРАФТТРАНС"')
    slots = Slot.objects.filter(date=timezone.localdate()).order_by("start_time")
    containers = Container.objects.filter(client=client).exclude(status=Container.Status.PICKED_UP)
    content = {
        "containers": containers,
        "status_on_station": Container.Status.ON_STATION,
        "today": timezone.localdate(),
        "slots": slots,
    }
    return render(request, "containers/container_list.html", content)
