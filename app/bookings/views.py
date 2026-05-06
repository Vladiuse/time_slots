from containers.models import Container
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View

from .models import Booking, Slot


class BookingCreateView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        slot_id = request.POST.get("slot_id")
        container_numbers = request.POST.getlist("container_numbers")

        slot = Slot.objects.get(pk=slot_id)
        containers = Container.objects.filter(number__in=container_numbers)

        bookings = [Booking(slot=slot, container=container) for container in containers]
        Booking.objects.bulk_create(bookings)

        containers.update(status=Container.Status.IN_BOOKING)

        return redirect("containers:containers_list")
