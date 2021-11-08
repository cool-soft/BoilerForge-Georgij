from dependency_injector import containers, providers

from bannikov_utils.data_services.data_services import DataServices


class DataServicesContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    db_repository = providers.Dependency()
    data_services = providers.Factory(
        DataServices,
        db_repository=db_repository,
    )