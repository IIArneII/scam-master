from scam_master.banks.interface import BankRepositoryInterface
from scam_master.services.browsermanager import Browser, start_browser, get_browser
from scam_master.services.helpers.banks import get_bank_repo
from scam_master.services.helpers.try_except import try_except
from scam_master.services.models.transactions import Transaction, Confirm


class TransactionsService:
    transactions: dict[str, Transaction] = {}
    
    def __init__(self) -> None:
        ...
    
    @try_except
    async def init(self, model: Transaction) -> None:
        br: Browser = None
        try:
            br: Browser = await start_browser(model)
            repo: BankRepositoryInterface = get_bank_repo(model.bank_gateway)
            
            await repo.fill_out_transfer_form(br.page, model.sender_card, model.recipient_card_number, model.amount)
            
            # kafka.send_message
        except Exception:
            if br:
                await br.browser.close()
            raise
        
    @try_except
    async def confirm(self, model: Confirm) -> None:
        br: Browser = None
        try:
            br = await get_browser(model.transaction_id)
            repo: BankRepositoryInterface = get_bank_repo(br.transaction.bank_gateway)
            
            await repo.confirm_transfer(br.page, model.confirmation_code)
            
            # kafka.send_message
        except Exception:
            if br:
                await br.browser.close()
            raise
