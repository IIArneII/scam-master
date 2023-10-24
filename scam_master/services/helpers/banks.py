from scam_master.banks.interface import BankRepositoryInterface
from scam_master.banks.tinkoff import TinkoffRepository
from scam_master.services.models.errors import UNKNOWN_BANK_ERR
from scam_master.services.models.transactions import Bank


def get_bank_repo(bank: Bank) -> BankRepositoryInterface:
    match bank:
        case Bank.tinkoff:
            return TinkoffRepository
        
    raise UNKNOWN_BANK_ERR