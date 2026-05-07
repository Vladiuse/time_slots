import json
import random

from containers.models import Container

from bookings.models import Booking, Slot

with open("_data/leave.json", "r", encoding="utf-8") as file:
    leave_containers = json.load(file)


def create_slots(containers: list[Container]) -> None:
    to_create = []
    slots = list(Slot.objects.all())
    for container in containers:
        slot = random.choice(slots)
        to_create.append(Booking(slot=slot, container=container))
        container.status = Container.Status.IN_BOOKING
        container.save()
    Booking.objects.bulk_create(to_create, ignore_conflicts=True)
    print(f"Created bookings for containers: {len(containers)}")


def create_bookings() -> None:
    containers = Container.objects.exclude(number__in=leave_containers)[:100]
    create_slots(containers)
    containers = Container.objects.filter(number__in=leave_containers)
    create_slots(containers)


def run() -> None:
    create_bookings()
