from abc import ABC, abstractmethod
from scam_master.services.models.transactions import Card
from pyppeteer import page


class BankRepositoryInterface(ABC):
    @staticmethod
    @abstractmethod
    async def fill_out_transfer_form(browser_page: page.Page, sender_card: Card, recipient_card_number: str, amount_kopeikami: int) -> None:
        pass
    
    @staticmethod
    @abstractmethod
    async def confirm_transfer(browser_page: page.Page, sms_code: str) -> None:
        pass