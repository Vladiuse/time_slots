from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def is_client(self) -> bool:
        return hasattr(self, "client_account")
