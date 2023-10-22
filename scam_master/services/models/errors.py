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

WRONG_PASS_ERR = BadRequestError('Wrong password')
CREDENTIALS_ERR = BadRequestError('Could not validate credentials')
