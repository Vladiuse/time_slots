from bookings.models import Booking, Slot
from clients.models import Client, ClientAccount
from containers.models import Container
from users.models import User


def run() -> None:
    Booking.objects.all().delete()
    Slot.objects.all().delete()
    Container.objects.all().delete()
    ClientAccount.objects.all().delete()
    Client.objects.all().delete()
    User.objects.exclude(username__in=["vlad", "admin"]).delete()
