from loguru import logger

from scam_master.infrastructure.browser_manager import BrowserManager
from scam_master.infrastructure.kafka_service import KafkaService
from scam_master.services.models.transactions import Transaction, ConfirmTransaction, Message, Topic, KafkaStatus, TransactionStatus
from scam_master.services.models.errors import BadRequestError, NotFoundError, BankError
from scam_master.services.helpers.banks import get_bank_transfer, get_bank_config, get_bank_driver
from config import BanksConfig


class TransactionsService:
    def __init__(self, browser_manager: BrowserManager, kafka_service: KafkaService, banks_config: dict) -> None:
        self._browser_manager: BrowserManager = browser_manager
        self._kafka_service: KafkaService = kafka_service
        self._banks_config: BanksConfig = BanksConfig(banks_config)
    
    
    async def init(self, model: Transaction) -> None:
        try:
            if await self._browser_manager.get(model.id):
                raise BadRequestError(f'Transaction {model.id} already exists')

            config = get_bank_config(self._banks_config, model.bank_gateway)
            sender = get_bank_transfer(model.sender_bank)
            gateway = get_bank_transfer(model.bank_gateway)
            driver = get_bank_driver(model.bank_gateway)

            browser = await self._browser_manager.start(model, driver, config.TIMEOUT)

            browser.set_status(TransactionStatus.filling_out_form)
            await gateway.fill_out_transfer_form(browser.page, config.URL, model.sender_card, model.recipient_card_number, model.amount)

            browser.set_status(TransactionStatus.confirmation_check)
            await sender.check_confirm_transfer(browser.page)

            browser.set_status(TransactionStatus.waiting_for_code)

            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=KafkaStatus.in_progress)
            )

        except BadRequestError as e:
            logger.info(e)
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=KafkaStatus.failed)
            )
        
        except BankError:
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=KafkaStatus.failed)
            )
            await self._browser_manager.stop(model.id)

        except Exception as e:
            logger.exception(e)
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=KafkaStatus.failed)
            )
            await self._browser_manager.stop(model.id)


    async def confirm(self, model: ConfirmTransaction) -> None:
        try:
            browser = await self._browser_manager.get(model.id)
            if not browser:
                raise NotFoundError(f'Transaction not found | id={model.id}')

            sender = get_bank_transfer(browser.transaction.sender_bank)
            gateway = get_bank_transfer(browser.transaction.bank_gateway)

            browser.set_status(TransactionStatus.entering_code)
            await sender.confirm_transfer(browser.page, model.confirmation_code)

            browser.set_status(TransactionStatus.transfer_check)
            await gateway.check_transfer_status(browser.page)
            
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=KafkaStatus.confirmed)
            )
            await self._browser_manager.stop(model.id)
        
        except NotFoundError as e:
            logger.info(e)
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=KafkaStatus.failed)
            )
        
        except BankError:
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=KafkaStatus.failed)
            )
            await self._browser_manager.stop(model.id)
        
        except Exception as e:
            logger.exception(e)
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=KafkaStatus.failed)
            )
            await self._browser_manager.stop(model.id)
