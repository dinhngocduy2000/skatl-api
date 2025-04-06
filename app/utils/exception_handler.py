from common.logger import get_logger
import asyncio
import functools
import inspect
import traceback
from contextvars import ContextVar
from fastapi import HTTPException

logger = get_logger(__name__)

exception_logged = ContextVar("exception_logged", default=False)


class ExceptionLoggingContext:
    def __enter__(self):
        exception_logged.set(False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class DatabaseException(HTTPException):
    def __init__(self, detail: Exception):
        self.status_code = 400
        self.detail = detail


class ServiceException(HTTPException):
    def __init__(self, detail: Exception):
        self.status_code = 400
        self.detail = detail


def handle_exceptions():
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if not exception_logged.get():
                    log_exception_details(e)
                    exception_logged.set(True)

                if isinstance(e, DatabaseException):
                    raise
                if isinstance(e, ServiceException):
                    raise
                if isinstance(e, HTTPException):
                    raise
                raise HTTPException(status_code=500, detail=str(e)) from e

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not exception_logged.get():
                    log_exception_details(e)
                    exception_logged.set(True)
                if isinstance(e, HTTPException):
                    raise
                raise HTTPException(status_code=500, detail=str(e)) from e

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


def log_exception_details(e):
    tb = traceback.extract_tb(e.__traceback__)
    repo_frame = next(
        (frame for frame in tb if "/app/repositories/" in frame.filename), None
    )

    if repo_frame:
        file_name = repo_frame.filename
        line_no = repo_frame.lineno
        error_func_name = repo_frame.name
    else:
        file_name = tb[-1].filename
        line_no = tb[-1].lineno
        error_func_name = tb[-1].name

    logger.error(
        f"Exception in file [{file_name}] function [{error_func_name}] line [{line_no}]: {str(e)}"
    )


def apply_decorator_to_all_methods(decorator):
    def decorate(cls):
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            if not name.startswith("__"):
                setattr(cls, name, decorator(method))
        return cls

    return decorate


