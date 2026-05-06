from containers.models import Container
from django.db import models


class Slot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_blocked = models.BooleanField(default=False)
    container_limit = models.PositiveIntegerField(default=50)

    class Meta:
        unique_together = ("date", "start_time")
        ordering = ("date", "start_time")

    def __str__(self) -> str:
        return f"{self.date} {self.start_time:%H:%M}—{self.end_time:%H:%M}"


class Booking(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        CANCELLED = "cancelled", "Отменена"
        NOT_COMPLETED = "not_completed", "Не выполнена"

    slot = models.ForeignKey(Slot, on_delete=models.PROTECT, related_name="bookings")
    container = models.ForeignKey(Container, on_delete=models.PROTECT, related_name="bookings")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.container.number} → {self.slot} ({self.status})"
