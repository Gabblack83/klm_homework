from enum import Enum
from functools import wraps
from typing import Any

from exceptions.user_defined_exceptions import DataException, ServiceException


class ApiResponse(Enum):
    OK: int = 200
    BAD_REQUEST: int = 400
    SERVER_ERROR: int = 500


def send_response(response_type: ApiResponse, payload: Any) -> tuple[Any, int]:
    return payload, response_type.value


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (DataException, ServiceException) as e:
            return send_response(
                ApiResponse.SERVER_ERROR,
                f"Error occurred in the application {'data' if isinstance(e, DataException) else 'service'} layer")
        except Exception:
            return send_response(
                ApiResponse.SERVER_ERROR,
                "General error occurred in the application")

    wrapper.__name__ = func.__name__
    return wrapper


