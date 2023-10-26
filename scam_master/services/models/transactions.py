from scam_master.services.models.base import BaseModel

from pydantic import Field
from typing import Annotated
from enum import Enum


class Bank(str, Enum):
    tinkoff = 'tinkoff'


class Topic(str, Enum):
    transactions_status_changed = 'transactions.status.changed'


class Status(str, Enum):
    in_progress = 'in_progress'
    confirmed = 'confirmed'
    failed = 'failed'


class Message(BaseModel):
    id: Annotated[str, Field(alias='ID')]
    status: Status


class Card(BaseModel):
    card_number: Annotated[str, Field(pattern='^\d{16}$', examples=['1111111111111111'])]
    expiration_date: Annotated[str, Field(pattern='^(0[1-9]|1[0-2])([0-9]{2})$', examples=['0101'])]
    cvc: Annotated[str, Field(pattern='^\d{3}$', examples=['111'])]


class Transaction(BaseModel):
    id: Annotated[str, Field(alias='ID')]
    sender_card: Card
    recipient_card_number: Annotated[str, Field(pattern='^\d{16}$', examples=['1111111111111111'])]
    bank_gateway: Annotated[Bank, Field(description='The bank through which the funds will be transferred')]
    sender_bank: Annotated[Bank, Field(description='Sender\'s card bank')]
    amount: Annotated[int, Field(ge=1000, examples=[1000], description='Amount in kopecks (RUB * 10^2)')]


class ConfirmTransaction(BaseModel):
    id: Annotated[str, Field(alias='ID')]
    confirmation_code: str
