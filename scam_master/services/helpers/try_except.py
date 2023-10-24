import asyncio
from loguru import logger
import traceback

from scam_master.services.models.errors import ServiceError


def _get_line(e: Exception):
    traceback_info = traceback.extract_tb(e.__traceback__)
    last_frame = traceback_info[-1]
    return last_frame.lineno


def try_except(func):
    if asyncio.iscoroutinefunction(func):
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ServiceError as e:
                logger.patch(lambda record: record.update(name=func.__module__, function=func.__name__, line=_get_line(e))).info(e)
                raise
            except Exception as e:
                logger.patch(lambda record: record.update(name=func.__module__, function=func.__name__, line=_get_line(e))).exception(e)
                raise
        return async_wrapper
    else:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ServiceError as e:
                logger.patch(lambda record: record.update(name=func.__module__, function=func.__name__, line=_get_line(e))).info(e)
                raise
            except Exception as e:
                logger.patch(lambda record: record.update(name=func.__module__, function=func.__name__, line=_get_line(e))).exception(e)
                raise
        return wrapper
