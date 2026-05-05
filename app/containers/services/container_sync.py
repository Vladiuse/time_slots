import logging
from collections.abc import Collection
from dataclasses import dataclass
from datetime import datetime, time

from clients.models import Client
from django.utils.timezone import make_aware

from containers.book_readers.unloading_reader.dto import UploadingContainer
from containers.models import Container

logger = logging.getLogger(__name__)


@dataclass
class ContainerSyncResult:
    created: list[Container]
    picked_up_numbers: Collection[str]
    skipped_no_client: list[UploadingContainer]


def sync_containers(uploading: list[UploadingContainer]) -> ContainerSyncResult:
    file_numbers: set[str] = {dto.container_number for dto in uploading}

    db_containers = Container.objects.all()
    existing_numbers: set[str] = {container.number for container in db_containers}
    on_station_numbers: set[str] = {
        container.number
        for container in db_containers
        if container.status == Container.Status.ON_STATION
    }

    picked_up_numbers = on_station_numbers - file_numbers
    if picked_up_numbers:
        Container.objects.filter(number__in=picked_up_numbers).update(status=Container.Status.PICKED_UP)
    clients_by_source: dict[str, Client] = {
        client.source_name: client for client in Client.objects.all()
    }

    to_create: list[Container] = []
    skipped: list[UploadingContainer] = []
    for dto in uploading:
        if dto.container_number in existing_numbers:
            continue
        client = clients_by_source.get(dto.client_name)
        if client is None:
            logger.warning(
                "Клиент %s не найден, контейнер %s пропущен",
                dto.client_name,
                dto.container_number,
            )
            skipped.append(dto)
            continue
        to_create.append(_dto_to_container(dto=dto, client=client))

    created = Container.objects.bulk_create(to_create)

    return ContainerSyncResult(created=created, picked_up_numbers=picked_up_numbers, skipped_no_client=skipped)


def _dto_to_container(dto: UploadingContainer, client: Client) -> Container:
    start_date = make_aware(datetime.combine(dto.start_date, time.min))
    return Container(
        client=client,
        number=dto.container_number,
        client_name=dto.client_name,
        start_date=start_date,
        nn=dto.nn,
        send_number=dto.send_number,
        weight=dto.weight,
        area=dto.area,
    )
