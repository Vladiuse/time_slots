from datetime import date

from bookings.models import Slot

SLOT_LIMITS: tuple[int, ...] = (70, 70, 70, 65, 55, 70)


def create_slots_for_date(target_date: date) -> list[Slot]:
    slots = [
        Slot(date=target_date, index=index, container_limit=limit)
        for index, limit in enumerate(SLOT_LIMITS)
    ]
    return Slot.objects.bulk_create(slots, ignore_conflicts=True)
