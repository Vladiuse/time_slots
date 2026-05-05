from typing import TYPE_CHECKING

from .container_separator import UploadingBookContainerSeparator
from .converter import UnloadingBookTextConverter
from .dto import UploadingContainer

if TYPE_CHECKING:
    from containers.book_readers.dto import ContainerExistLines


class UploadBookReader:
    def read(self, text: str) -> list[UploadingContainer]:
        separate_result: ContainerExistLines = UploadingBookContainerSeparator().separate(lines=text.split("\n"))
        containers: list[UploadingContainer] = UnloadingBookTextConverter().convert(
            lines_with_containers=separate_result.lines_with_container,
        )
        return containers
