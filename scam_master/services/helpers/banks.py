from typing import Type

from scam_master.infrastructure.banks.interface import IBankTransfer
from scam_master.infrastructure.banks.tinkoff import TinkoffTransfer
from scam_master.infrastructure.banks.otp import OtpTransfer
from scam_master.infrastructure.banks.sber import SberTransfer
from scam_master.infrastructure.banks.rsh import RshTransfer
from scam_master.services.models.errors import UNKNOWN_BANK_ERR
from scam_master.services.models.transactions import Bank, Driver
from config import BanksConfig, BankConfig


def get_bank_transfer(bank: Bank) -> Type[IBankTransfer]:
    if bank == Bank.tinkoff:
        return TinkoffTransfer
    if bank == Bank.otp:
        return OtpTransfer
    if bank == Bank.sber:
        return SberTransfer
    if bank == Bank.rsh:
        return RshTransfer
            
    raise UNKNOWN_BANK_ERR


def get_bank_driver(bank: Bank) -> Driver:
    if bank == Bank.tinkoff:
        return Driver.pyppeteer
    if bank == Bank.otp:
        return Driver.selenium
    if bank == Bank.rsh:
        return Driver.selenium
    
    raise UNKNOWN_BANK_ERR


def get_bank_config(banks_config: BanksConfig, bank: Bank) -> BankConfig:
    if bank == Bank.tinkoff:
        return banks_config.tinkoff
    if bank == Bank.otp:
        return banks_config.otp
    if bank == Bank.rsh:
        return banks_config.rsh
        
    raise UNKNOWN_BANK_ERR
