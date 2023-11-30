from scam_master.services.models.base import BaseModel

from pydantic import Field
from typing import Annotated
from enum import Enum


class Bank(str, Enum):
    tinkoff = 'tinkoff'
    otp = 'otp'
    sber = 'sber'
    rsh = 'rsh'


class Driver(str, Enum):
    pyppeteer = 'pyppeteer'
    selenium = 'selenium'


class Topic(str, Enum):
    transactions_status_changed = 'transactions.status.changed'


class KafkaStatus(str, Enum):
    in_progress = 'in_progress'
    confirmed = 'confirmed'
    failed = 'failed'


class TransactionStatus(str, Enum):
    browser_creation = 'browser_creation'
    filling_out_form = 'filling_out_form'
    confirmation_check = 'confirmation_check'
    waiting_for_code = 'waiting_for_code'
    entering_code = 'entering_code'
    transfer_check = 'transfer_check'


class Message(BaseModel):
    id: str
    status: KafkaStatus


class Card(BaseModel):
    card_number: Annotated[str, Field(pattern='^\d{16}$', examples=['1111111111111111'])]
    expiration_date: Annotated[str, Field(pattern='^(0[1-9]|1[0-2])([0-9]{2})$', examples=['0101'])]
    cvc: Annotated[str, Field(pattern='^\d{3}$', examples=['111'])]


class Transaction(BaseModel):
    id: str
    sender_card: Card
    recipient_card_number: Annotated[str, Field(pattern='^\d{16}$', examples=['1111111111111111'])]
    bank_gateway: Annotated[Bank, Field(description='The bank through which the funds will be transferred')]
    sender_bank: Annotated[Bank, Field(description='Sender\'s card bank')]
    amount: Annotated[int, Field(ge=1000, examples=[1000], description='Amount in kopecks (RUB * 10^2)')]


class ConfirmTransaction(BaseModel):
    id: Annotated[str, Field(alias='ID')]
    confirmation_code: str
