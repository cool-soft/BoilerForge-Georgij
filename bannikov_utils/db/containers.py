from dependency_injector import containers, providers
from bannikov_utils.db.repository import DBRepository
from bannikov_utils.db.resources import DBConnect


class DBContainer(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)

    resource = providers.Resource(
        DBConnect,
        path=config.path,
        base=config.base,
    )

    db_repository = providers.Singleton(
        DBRepository,
        session_factory=resource,
    )