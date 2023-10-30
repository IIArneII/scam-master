class ServiceError(Exception):
    ...

class NotFoundError(ServiceError):
    ...

class BadRequestError(ServiceError):
    ...

class BankError(Exception):
    ...


UNKNOWN_TRANSFER_STATUS = BankError('Unknown transfer status')
UNKNOWN_BANK_ERR = BadRequestError('Unknown bank')
TRANSACTION_ALREADY_EXISTS = BadRequestError('Transaction already exists')
TRANSACTION_NOT_FOUND = NotFoundError('Transaction not found')
