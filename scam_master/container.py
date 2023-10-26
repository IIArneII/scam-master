from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Factory, Configuration
from typing import Type

from config import Config
from scam_master.infrastructure.browser_manager import BrowserManager
from scam_master.services.transactions import TransactionsService
from scam_master.infrastructure.kafka_service import KafkaService


class Container(DeclarativeContainer):
    config: Config = Configuration()

    wiring_config = WiringConfiguration(modules=[
        '.controllers.helpers.services_providers',
    ])

    browser_manager: Type[BrowserManager] = Singleton(BrowserManager, browser_config=config.browser)
    kafka_service: Type[KafkaService] = Singleton(KafkaService, kafka_config=config.kafka)

    transactions_service: Type[TransactionsService] = Factory(
        TransactionsService,
        browser_manager=browser_manager,
        kafka_service=kafka_service,
        banks_config=config.banks)
