from clients.models import Client


def sync_clients(source_names: list[str]) -> list[Client]:
    existing = set(Client.objects.values_list("source_name", flat=True))
    new_names = [name for name in source_names if name not in existing]
    new_clients = [Client(source_name=name, name=name) for name in new_names]
    return Client.objects.bulk_create(new_clients)
