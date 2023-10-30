from fastapi import status
from fastapi import APIRouter, BackgroundTasks, Depends
from scam_master.controllers.helpers.responses import NO_CONTENT
from scam_master.controllers.helpers.services_providers import transactions_service
from scam_master.services.transactions import TransactionsService
from scam_master.services.models.transactions import Transaction, ConfirmTransaction


transactions_api = APIRouter(
    prefix='/transactions',
    tags=['transactions']
)


@transactions_api.post('/init-transaction', operation_id='init', status_code=status.HTTP_204_NO_CONTENT, responses= NO_CONTENT)
async  def init_transaction(background_tasks: BackgroundTasks, model: Transaction, transactions_service: TransactionsService = Depends(transactions_service)):
    '''
    Initialize funds transfer from card to card.
    '''
    return background_tasks.add_task(transactions_service.init, model)


@transactions_api.post('/confirm-transaction', operation_id='confirm', status_code=status.HTTP_204_NO_CONTENT, responses= NO_CONTENT)
async def confirm_transaction(background_tasks: BackgroundTasks, model: ConfirmTransaction, transactions_service: TransactionsService = Depends(transactions_service)):
    '''
    Confirm the funds transfer with a confirmation code.
    '''
    return background_tasks.add_task(transactions_service.confirm, model)
