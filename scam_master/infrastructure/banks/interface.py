from abc import ABC, abstractmethod
from pyppeteer.page import Page as PyppPage
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger

from scam_master.services.models.errors import UNKNOWN_TRANSFER_STATUS
from scam_master.services.models.transactions import Card


class IBankTransfer(ABC):
    @staticmethod
    @abstractmethod
    async def fill_out_transfer_form(page: PyppPage | WebDriver, url: str, sender_card: Card, recipient_card_number: str, amount: int) -> None:
        '''
        Fills out the transfer form and presses the button.
        Used for gateway bank.
        '''
        logger.warning('Not implemented')
        raise UNKNOWN_TRANSFER_STATUS
    
    @staticmethod
    @abstractmethod
    async def check_confirm_transfer(page: PyppPage | WebDriver) -> None:
        '''
        Checks whether the 3D security page is open to enter a confirmation code.
        Used for sender's bank.
        '''
        logger.warning('Not implemented')
        raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    @abstractmethod
    async def confirm_transfer(page: PyppPage | WebDriver, sms_code: str) -> None:
        '''
        Fills out the 3D security form, enters the confirmation code.
        Used for sender's bank.
        '''
        logger.warning('Not implemented')
        raise UNKNOWN_TRANSFER_STATUS
    
    @staticmethod
    @abstractmethod
    async def check_transfer_status(page: PyppPage | WebDriver) -> None:
        '''
        Checks the status of the transfer.
        Used for gateway bank.
        '''
        logger.warning('Not implemented')
        raise UNKNOWN_TRANSFER_STATUS
