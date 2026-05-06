from containers.models import Container
from django.db import models


class Slot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_blocked = models.BooleanField(default=False)
    current_count = models.PositiveIntegerField(default=0)
    container_limit = models.PositiveIntegerField(default=50)

    class Meta:
        unique_together = ("date", "start_time")
        ordering = ("date", "start_time")

    def __str__(self) -> str:
        return f"{self.date} {self.time_range}"

    @property
    def time_range(self) -> str:
        return f"{self.start_time:%H:%M} — {self.end_time:%H:%M}"

    @property
    def occupancy_percent(self) -> int:
        if self.container_limit == 0:
            return 0
        return round(self.current_count / self.container_limit * 100)

    @property
    def is_full(self) -> bool:
        return self.current_count >= self.container_limit

    @property
    def color_class(self) -> str:
        if self.is_blocked or self.occupancy_percent >= 100:  # noqa: PLR2004
            return "dark"
        if self.occupancy_percent >= 80:  # noqa: PLR2004
            return "danger"
        if self.occupancy_percent >= 50:  # noqa: PLR2004
            return "warning"
        return "success"


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
