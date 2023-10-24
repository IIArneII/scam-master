from config import Config, LogConfig
from loguru import logger
from fastapi import FastAPI
from starlette.exceptions import HTTPException


from scam_master.controllers.helpers.responses import INTERNAL_SERVER_ERROR
from scam_master.controllers.helpers import exception_handlers
from scam_master.controllers.transactions import transactions_api
from scam_master.container import Container
from scam_master.services.models.errors import NotFoundError, BadRequestError


def create_app(config: Config):
    _init_logger(config.log)

    container = Container()
    container.config.from_dict(config.model_dump())

    global_api = FastAPI(
        debug=config.app.DEBUG,
        docs_url=None,
        redoc_url=None,
    )
    global_api.container = container

    _init_routes(global_api, config)

    return global_api


def _init_logger(config: LogConfig):
    if config.TO_FILE:
        logger.add(f'{config.LOG_DIR}/logs.log', compression='zip', rotation=f'{config.ROTATION} MB', retention=config.RETENTION, level=config.LEVEL)


def _init_routes(global_api: FastAPI, config: Config):
    logger.info('Routes initialization...')

    api_v1 = FastAPI(
        debug=config.app.DEBUG,
        version=config.api.VERSION,
        title=f'{config.api.TITLE} V1',
        summary=config.api.SUMMARY,
        description=config.api.DESCRIPTION,
        docs_url='/openapi' if config.api.IS_VISIBLE else None,
        redoc_url=None,
        responses=INTERNAL_SERVER_ERROR,
    )

    api_v1.add_exception_handler(NotFoundError, exception_handlers.not_found_handler)
    api_v1.add_exception_handler(BadRequestError, exception_handlers.bad_request_handler)
    api_v1.add_exception_handler(HTTPException, exception_handlers.http_error_handler)
    api_v1.add_exception_handler(Exception, exception_handlers.internal_server_error_handler)

    api_v1.include_router(transactions_api)
    
    global_api.mount(f'{config.api.PREFIX}/v1', api_v1)
