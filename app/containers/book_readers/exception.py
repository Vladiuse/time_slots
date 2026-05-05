from core.exceptions import AppError


class ContainerFileReadError(AppError):
    pass


class ContainerNotFound(ContainerFileReadError):
    pass


class FileLineFindDataError(ContainerFileReadError):
    pass
