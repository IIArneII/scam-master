from abc import ABC, abstractmethod
from scam_master.services.models.transactions import Card
from pyppeteer.page import Page as PyppPage


class IBankTransfer(ABC):
    @staticmethod
    @abstractmethod
    async def fill_out_transfer_form(page: PyppPage, url: str, sender_card: Card, recipient_card_number: str, amount: int) -> None:
        ...
    
    @staticmethod
    @abstractmethod
    async def confirm_transfer(page: PyppPage, sms_code: str) -> None:
        ...
