from scam_master.services.models.base import BaseModel

from pydantic import Field
from typing import Annotated
from enum import Enum


class Bank(str, Enum):
    tinkoff = 'tinkoff'


class Transaction(BaseModel):
    transaction_id: str
    sender_card_number: Annotated[str, Field(pattern='^\d{16}$', examples=['1111111111111111'])]
    validity: Annotated[str, Field(pattern='^(0[1-9]|1[0-2])([0-9]{2})$', examples=['0101'])]
    cvc: Annotated[str, Field(pattern='^\d{3}$', examples=['111'])]
    recipient_card_number: Annotated[str, Field(pattern='^\d{16}$', examples=['1111111111111111'])]
    bank_gateway: Annotated[Bank, Field(description='The bank through which the funds will be transferred')]
    sender_bank: Annotated[Bank, Field(description='Sender\'s card bank')]
    amount: Annotated[int, Field(ge=1, examples=[1], description='Amount in kopecks (RUB * 10^2)')]


class Confirm(BaseModel):
    transaction_id: str
    confirmation_code: str
