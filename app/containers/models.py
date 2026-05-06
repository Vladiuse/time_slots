from clients.models import Client
from django.core.validators import MaxValueValidator
from django.db import models


class Container(models.Model):
    class Status(models.TextChoices):
        ON_STATION = "on_station", "На станции"
        IN_BOOKING = "in_booking", "В заявке"
        PICKED_UP = "picked_up", "Забран"

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="containers")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ON_STATION)
    number = models.CharField(max_length=11)
    client_name = models.CharField(max_length=30)
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)
    nn = models.CharField(max_length=5, blank=True)
    send_number = models.CharField(max_length=10, blank=True)
    weight = models.CharField(max_length=5, blank=True)
    area = models.PositiveIntegerField(default=None, null=True, validators=[MaxValueValidator(99)])

    def __str__(self) -> str:
        return f"<Container:{self.number}>"
