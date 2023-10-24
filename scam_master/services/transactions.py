from scam_master.infrastructure.browser_manager import BrowserManager, Browser
from scam_master.services.helpers.banks import get_bank_transfer, get_bank_config
from scam_master.services.helpers.try_except import try_except
from scam_master.services.models.errors import NOT_FOUND_ERR
from scam_master.services.models.transactions import Transaction, Confirm
from config import BanksConfig


class TransactionsService:
    def __init__(self, browser_manager: BrowserManager, banks_config: dict) -> None:
        self._browser_manager: BrowserManager = browser_manager
        self._banks_config: BanksConfig = BanksConfig(banks_config)
    
    @try_except
    async def init(self, model: Transaction) -> None:
        try:
            config = get_bank_config(self._banks_config, model.bank_gateway)

            browser = await self._browser_manager.start(model, config.TIMEOUT)
            
            transfer = get_bank_transfer(model.bank_gateway)
            await transfer.fill_out_transfer_form(browser.page, config.URL, model.sender_card, model.recipient_card_number, model.amount)
            
            # kafka.send_message
        except Exception:
            await self._browser_manager.stop(model.transaction_id)
            raise

    @try_except
    async def confirm(self, model: Confirm) -> None:
        br: Browser = None
        try:
            br = await self._browser_manager.get(model.transaction_id)
            
            transfer = get_bank_transfer(br.transaction.sender_bank)
            await transfer.confirm_transfer(br.page, model.confirmation_code)
            
            # kafka.send_message
        except Exception:
            await self._browser_manager.stop(model.transaction_id)
            raise
