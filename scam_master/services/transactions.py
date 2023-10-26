from loguru import logger

from scam_master.infrastructure.browser_manager import BrowserManager
from scam_master.infrastructure.kafka_service import KafkaService
from scam_master.services.models.transactions import Transaction, ConfirmTransaction, Message, Topic, Status
from scam_master.services.models.errors import BadRequestError, NotFoundError, BankError
from scam_master.services.helpers.banks import get_bank_transfer, get_bank_config
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
            get_bank_transfer(model.sender_bank)
            transfer = get_bank_transfer(model.bank_gateway)

            logger.info('Browser creation...')
            browser = await self._browser_manager.start(model, config.TIMEOUT)

            logger.info('Filling out the transfer form...')
            await transfer.fill_out_transfer_form(browser.page, config.URL, model.sender_card, model.recipient_card_number, model.amount)
            
            logger.info('Waiting for confirmation code to be entered...')

            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=Status.in_progress)
            )

        except BadRequestError as e:
            logger.info(e)
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=Status.failed)
            )
        
        except BankError:
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=Status.failed)
            )
            await self._browser_manager.stop(model.id)

        except Exception as e:
            logger.exception(e)
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=Status.failed)
            )
            await self._browser_manager.stop(model.id)


    async def confirm(self, model: ConfirmTransaction) -> None:
        try:
            browser = await self._browser_manager.get(model.id)
            if not browser:
                raise NotFoundError(f'Transaction {model.id} not found')

            transfer = get_bank_transfer(browser.transaction.sender_bank)

            logger.info('Confirmation of transfer...')
            await transfer.confirm_transfer(browser.page, model.confirmation_code)
            
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=Status.confirmed)
            )
            await self._browser_manager.stop(model.id)
        
        except NotFoundError as e:
            logger.info(e)
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=Status.failed)
            )
        
        except BankError:
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=Status.failed)
            )
            await self._browser_manager.stop(model.id)
        
        except Exception as e:
            logger.exception(e)
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=model.id, status=Status.failed)
            )
            await self._browser_manager.stop(model.id)
