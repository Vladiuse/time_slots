from dataclasses import dataclass

from clients.models import Client
from clients.services import sync_clients
from containers.book_readers.unloading_reader.main import UploadBookReader
from containers.services.container_sync import ContainerSyncResult, sync_containers


@dataclass
class SyncResult:
    new_clients: list[Client]
    containers: ContainerSyncResult


def sync_from_text(text: str) -> SyncResult:
    uploading = UploadBookReader().read(text=text)

    source_names = list({c.client_name for c in uploading})
    new_clients = sync_clients(source_names)

    container_result = sync_containers(uploading)

    return SyncResult(new_clients=new_clients, containers=container_result)
