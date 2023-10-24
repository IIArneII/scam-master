class ServiceError(Exception):
    ...

class NotFoundError(ServiceError):
    ...

class BadRequestError(ServiceError):
    ...

class ForbiddenError(ServiceError):
    ...


NOT_FOUND_ERR = NotFoundError('Not found')
FORBIDDEN_ERR = NotFoundError('Forbidden')
BAD_REQUEST_ERR = BadRequestError('Bad request')

UNKNOWN_BANK_ERR = BadRequestError('Unknown bank')
TRANSACTION_ALREADY_EXISTS = ServiceError('Transaction already exists')
