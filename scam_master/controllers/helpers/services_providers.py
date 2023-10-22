from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from scam_master.container import Container
from scam_master.services.transactions import TransactionsService


@inject
def transactions_service(transactions_service: TransactionsService  = Depends(Provide[Container.transactions_service])) -> TransactionsService:
    return transactions_service
