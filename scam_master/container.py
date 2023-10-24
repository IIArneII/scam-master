from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Factory, Configuration

from config import Config
from scam_master.infrastructure.browser_manager import BrowserManager
from scam_master.services.transactions import TransactionsService


class Container(DeclarativeContainer):
    config: Config = Configuration()

    wiring_config = WiringConfiguration(modules=[
        '.controllers.helpers.services_providers',
    ])

    browser_manager: BrowserManager = Singleton(BrowserManager)

    transactions_service: TransactionsService = Factory(TransactionsService, browser_manager=browser_manager, banks_config=config.banks)
