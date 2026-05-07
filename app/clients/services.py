from django.contrib.auth.hashers import make_password
from faker import Faker
from users.models import User

from clients.models import Client, ClientAccount
from clients.utils import client_name_to_username

fake = Faker("ru_RU")

DEFAULT_PASSWORD = "20003000Ab%"  # noqa: S105


def create_client_accounts(clients: list[Client]) -> list[ClientAccount]:
    password_hash = make_password(DEFAULT_PASSWORD)
    users = [
        User(username=client_name_to_username(client.name), password=password_hash)
        for client in clients
    ]
    created_users = User.objects.bulk_create(users)

    accounts = [
        ClientAccount(
            user=user,
            client=client,
            role=ClientAccount.Role.MASTER,
        )
        for user, client in zip(created_users, clients, strict=True)
    ]
    return ClientAccount.objects.bulk_create(accounts)


def sync_clients(source_names: list[str]) -> list[Client]:
    existing = set(Client.objects.values_list("source_name", flat=True))
    new_names = [name for name in source_names if name not in existing]
    new_clients = [
        Client(
            source_name=name,
            name=name,
            contact_full_name=fake.name(),
            address=fake.address(),
            phone=fake.phone_number(),
            email=fake.email(),
        )
        for name in new_names
    ]
    return Client.objects.bulk_create(new_clients)
