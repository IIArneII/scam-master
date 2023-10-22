from scam_master.services.models.errors import BadRequestError, NOT_FOUND_ERR
from scam_master.services.helpers.try_except import try_except
from scam_master.services.models.transactions import Transaction, Confirm


class TransactionsService:
    def __init__(self) -> None:
        ...
    
    @try_except
    def init(self, model: Transaction) -> None:
        ...
    
    @try_except
    def confirm(self, model: Confirm) -> None:
        ...
