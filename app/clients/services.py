from faker import Faker
from users.models import User

from clients.models import Client, ClientAccount
from clients.utils import client_name_to_username

fake = Faker("ru_RU")


def create_client_accounts(clients: list[Client]) -> list[ClientAccount]:
    accounts = []
    for client in clients:
        username = client_name_to_username(client.name)
        user = User.objects.create(username=username)
        account = ClientAccount.objects.create(
            user=user,
            client=client,
            role=ClientAccount.Role.MASTER,
        )
        accounts.append(account)
    return accounts


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
