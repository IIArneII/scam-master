from fastapi import HTTPException, status


CREDENTIALS_ERR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

FORBIDDEN_ERR = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Forbidden',
    )

GRANT_TYPE_PASS_ERR = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='If the value is "password" for the "grant_type" field, the username and password must be passed',
    )

GRANT_TYPE_REFRESH_ERR = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='If the value is "refresh_token" for the "grant_type" field, the refresh_token must be passed',
    )
