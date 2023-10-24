class BankException(Exception):
    ...


UNKNOWN_TRANSFER_STATUS = BankException('Unknown transfer status')
