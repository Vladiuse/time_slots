import json
import random

from containers.models import Container

from bookings.models import Booking, Slot
from django.db.models import Q
from django.utils import timezone

PAST_COMPLETED_RATE = 0.9
FUTURE_CANCELLED_RATE = 0.2

with open("_data/leave.json", "r", encoding="utf-8") as file:
    leave_containers = json.load(file)


def add_booking_to_slots(containers: list[Container]) -> None:
    to_create = []
    slots = list(Slot.objects.all())
    for container in containers:
        slot = random.choice(slots)
        to_create.append(Booking(slot=slot, container=container))
        container.status = Container.Status.IN_BOOKING
        container.save()
    Booking.objects.bulk_create(to_create, ignore_conflicts=True)
    print(f"Created bookings for containers: {len(containers)}")


def update_statuses() -> None:
    today = timezone.localdate()

    now = timezone.localtime()
    past_bookings = list(
        Booking.objects.filter(status=Booking.Status.ACTIVE).filter(
            Q(slot__date__lt=today) |
            Q(slot__date=today, slot__end_time__lt=now.time()),
        )
    )
    past_bookings = list(
        Booking.objects.filter(
            Q(slot__date__lt=today) |
            Q(slot__date=today, slot__end_time__lt=now.time()),
        ).select_related("container"),
    )
    for booking in past_bookings:
        is_completed = random.random() < PAST_COMPLETED_RATE  # noqa: S311
        if is_completed:
            booking.status = Booking.Status.COMPLETED
            booking.container.status = Container.Status.PICKED_UP
        else:
            booking.status = Booking.Status.CANCELLED
            booking.container.status = Container.Status.ON_STATION
    Booking.objects.bulk_update(past_bookings, ["status"])
    Container.objects.bulk_update([b.container for b in past_bookings], ["status"])
    print(f"Updated {len(past_bookings)} past bookings")

    future_bookings = list(Booking.objects.filter(slot__date__gt=today, status=Booking.Status.ACTIVE))
    cancelled = [b for b in future_bookings if random.random() < FUTURE_CANCELLED_RATE]  # noqa: S311
    for booking in cancelled:
        booking.status = Booking.Status.CANCELLED
    Booking.objects.bulk_update(cancelled, ["status"])
    print(f"Cancelled {len(cancelled)} future bookings")


def create_bookings() -> None:
    containers = Container.objects.exclude(number__in=leave_containers)[:100]
    add_booking_to_slots(containers)
    containers = Container.objects.filter(number__in=leave_containers)
    add_booking_to_slots(containers)


def run() -> None:
    create_bookings()
    update_statuses()
