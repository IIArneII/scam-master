from fastapi import APIRouter, BackgroundTasks, Depends
from scam_master.controllers.helpers.responses import NO_CONTENT, NOT_FOUND, BAD_REQUEST
from scam_master.controllers.helpers.services_providers import transactions_service
from scam_master.services.transactions import TransactionsService
from scam_master.services.models.transactions import Transaction, Confirm


transactions_api = APIRouter(
    prefix='/transactions',
    tags=['transactions']
)


@transactions_api.post('/init-transaction', operation_id='init', responses= NO_CONTENT | BAD_REQUEST)
async  def init_transaction(background_tasks: BackgroundTasks, model: Transaction, transactions_service: TransactionsService = Depends(transactions_service)):
    '''
    Initialize funds transfer from card to card.
    '''
    return background_tasks.add_task(transactions_service.init, model)


@transactions_api.post('/confirm-transaction', operation_id='confirm', responses= NO_CONTENT | BAD_REQUEST | NOT_FOUND)
async def confirm_transaction(background_tasks: BackgroundTasks, model: Confirm, transactions_service: TransactionsService = Depends(transactions_service)):
    '''
    Confirm the funds transfer with a confirmation code.
    '''
    return background_tasks.add_task(transactions_service.confirm, model)
