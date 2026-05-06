from datetime import date, time

from bookings.models import Slot

SLOT_SCHEDULE: tuple[tuple[time, time, int], ...] = (
    (time(0, 0), time(4, 0), 70),
    (time(4, 0), time(8, 0), 70),
    (time(8, 0), time(12, 0), 70),
    (time(12, 0), time(16, 0), 65),
    (time(16, 0), time(20, 0), 55),
    (time(20, 0), time(0, 0), 70),
)


def create_slots_for_date(target_date: date) -> list[Slot]:
    slots = [
        Slot(date=target_date, start_time=start, end_time=end, container_limit=limit)
        for start, end, limit in SLOT_SCHEDULE
    ]
    return Slot.objects.bulk_create(slots, ignore_conflicts=True)
