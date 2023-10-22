from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton, Configuration

from config import Config
from scam_master.services.transactions import TransactionsService


class Container(DeclarativeContainer):
    config: Config = Configuration()

    wiring_config = WiringConfiguration(modules=[
        '.controllers.helpers.services_providers',
    ])

    transactions_service: TransactionsService = Factory(TransactionsService)
