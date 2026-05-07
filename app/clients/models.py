from django.db import models
from users.models import User


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    source_name = models.CharField(max_length=255, unique=True)
    is_blocked = models.BooleanField(default=False)
    contact_full_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=512, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self) -> str:
        return self.name


class ClientAccount(models.Model):
    class Role(models.TextChoices):
        MASTER = "master", "Мастер-аккаунт"
        EMPLOYEE = "employee", "Сотрудник"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_account")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="accounts")
    role = models.CharField(max_length=16, choices=Role.choices)

    def __str__(self) -> str:
        return f"{self.client} / {self.user} ({self.role})"
