from typing import Type

from scam_master.infrastructure.banks.interface import IBankTransfer
from scam_master.infrastructure.banks.tinkoff import TinkoffTransfer
from scam_master.infrastructure.banks.psbank import PsbankTransfer
from scam_master.services.models.errors import UNKNOWN_BANK_ERR
from scam_master.services.models.transactions import Bank
from config import BanksConfig, BankConfig


def get_bank_transfer(bank: Bank) -> Type[IBankTransfer]:
    match bank:
        case Bank.tinkoff:
            return TinkoffTransfer
        case Bank.psbank:
            return PsbankTransfer

    raise UNKNOWN_BANK_ERR


def get_bank_config(banks_config: BanksConfig, bank: Bank) -> BankConfig:
    match bank:
        case Bank.tinkoff:
            return banks_config.tinkoff
        case Bank.psbank:
            return banks_config.psbank
        
    raise UNKNOWN_BANK_ERR
