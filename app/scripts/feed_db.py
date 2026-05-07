from bookings.scripts.bookings.create_booking import create_bookings, update_statuses
from bookings.scripts.bookings.create_slots import create_slots
from containers.scripts.containers.create_containers import load_3_db


def run() -> None:
    load_3_db()
    create_slots()
    create_bookings()
    update_statuses()