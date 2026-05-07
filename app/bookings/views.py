from itertools import groupby

from clients.models import Client
from containers.models import Container
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .models import Booking, Slot


class BookingCreateView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        slot_id = request.POST["slot_id"]
        container_numbers = request.POST.getlist("container_numbers")

        slot = Slot.objects.get(pk=slot_id)
        containers = Container.objects.filter(number__in=container_numbers)

        bookings = [Booking(slot=slot, container=container) for container in containers]
        Booking.objects.bulk_create(bookings)

        containers.update(status=Container.Status.IN_BOOKING)

        return redirect("containers:containers_list")


class BookingListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        client = Client.objects.get(source_name='ООО "КРАФТТРАНС"')
        bookings = (
            Booking.objects.filter(container__client=client)
            .select_related("slot", "container", "container__client")
            .order_by("-slot__date", "slot__start_time")
        )
        return render(request, "bookings/booking_list.html", {"bookings": bookings})


class SlotListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        client = Client.objects.get(source_name='ООО "КРАФТТРАНС"')
        slots = list(
            Slot.objects.prefetch_related(
                Prefetch(
                    "bookings",
                    queryset=Booking.objects.filter(
                        container__client=client,
                    ).select_related("container"),
                    to_attr="client_bookings",
                ),
            )
            .order_by("date", "start_time"),
        )
        slots_by_date = [
            (date, list(group))
            for date, group in groupby(slots, key=lambda slot: slot.date)
        ]
        return render(request, "bookings/slot_list.html", {"slots_by_date": slots_by_date})


class BookingDeleteView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:  # noqa: ARG002
        booking = Booking.objects.select_related("container").get(pk=pk)
        booking.container.status = Container.Status.ON_STATION
        booking.container.save(update_fields=["status"])
        booking.delete()
        return redirect("bookings:booking_list")
