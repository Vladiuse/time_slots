from dataclasses import dataclass

from clients.services import create_client_accounts, sync_clients

from containers.book_readers.unloading_reader.main import UploadBookReader
from containers.services.container_sync import ContainerSyncResult, sync_containers


@dataclass
class SyncResult:
    new_client_ids: list[int]
    new_client_account_ids: list[int]
    containers: ContainerSyncResult


def sync_from_text(text: str) -> SyncResult:
    uploading = UploadBookReader().read(text=text)

    source_names = list({container.client_name for container in uploading})
    new_clients = sync_clients(source_names)
    new_accounts = create_client_accounts(new_clients)

    container_result = sync_containers(uploading)

    return SyncResult(
        new_client_ids=[client.id for client in new_clients],
        new_client_account_ids=[account.id for account in new_accounts],
        containers=container_result,
    )
