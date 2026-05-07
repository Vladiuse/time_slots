from datetime import timedelta

from django.utils import timezone

from bookings.services import create_slots_for_date


def create_slots() -> None:
    today = timezone.localdate()
    dates = [today + timedelta(days=i) for i in range(-7, 8)]
    for date in dates:
        create_slots_for_date(date)
    print(f"Created slots for {len(dates)} dates: {dates[0]} — {dates[-1]}")

def run() -> None:
    create_slots()
