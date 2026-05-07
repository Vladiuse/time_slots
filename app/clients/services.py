from faker import Faker

from clients.models import Client

fake = Faker("ru_RU")


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
