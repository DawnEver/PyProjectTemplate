from .logger import log

__all__ = ['ParameterException', 'deprecated', 'not_implemented']


class ParameterException(Exception):
    """Exception for unexpected parameters."""

    def __init__(self, message='') -> None:
        self.message = message

    def __str__(self) -> str:
        msg = f'ParameterException: {self.message}'
        log(msg, level='ERROR')
        return msg


def not_implemented(func):
    def wrapper(*_, **__):
        msg = f'{func.__name__} is not implemented yet.'
        raise NotImplementedError(msg)

    return wrapper


def deprecated(func):
    def wrapper(*_, **__):
        msg = f'{func.__name__} has been deprecated.'
        raise DeprecationWarning(msg)

    return wrapper
