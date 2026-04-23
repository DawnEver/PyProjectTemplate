import functools
import logging
import time

__all__ = ['add_handle', 'log', 'log_decorator', 'timer']


for pack in ['matplotlib']:
    logging.getLogger(pack).setLevel(logging.ERROR)

# Initialize root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def add_handle() -> None:
    """Add a series of logging handlers based on Config.
    Because config.py depends on logger.py (config.py -> io.py -> logger.py),
    we cannot import config.py at module level here to avoid circular imports.
    """
    from .config import CONF, PathData, Utils  # noqa: PLC0415

    utils_config: Utils = CONF.utils
    # Log file handler
    logging_file_handler = logging.FileHandler(PathData.log_folder_path / PathData.log_filename, encoding='utf-8')
    logging_file_handler.setLevel(logging.INFO)
    logging_file_format = logging.Formatter(fmt=utils_config.log_file_format, datefmt=utils_config.log_date_format)
    logging_file_handler.setFormatter(logging_file_format)
    logger.addHandler(logging_file_handler)

    # Console handler
    logging_console_handler = logging.StreamHandler()
    logging_console_handler.setLevel(logging.INFO)
    logging_console_format = logging.Formatter(
        fmt=utils_config.log_console_format,
        datefmt=utils_config.log_date_format,
    )
    logging_console_handler.setFormatter(logging_console_format)
    logger.addHandler(logging_console_handler)


def log(msg: str, level: str = 'INFO') -> None:
    """Logging output function.

    Args:
    ----
        msg (str): Log message
        level (str): Log level
    Returns:
        None

    Examples:
    --------
        ```python
        log('hello world', level='INFO')
        ```

    Available levels: ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        - DEBUG | Most detailed messages, typically for troubleshooting;
        - INFO | Less detailed than DEBUG, usually record key milestones to confirm things are working as expected;
        - WARNING | Recorded when something unexpected happens (e.g., low disk space), but the application is still running;
        - ERROR | Recorded when a more serious problem causes some functionality to fail;
        - CRITICAL | Recorded when a severe error causes the application to stop running.

    """
    level = level.upper()
    match_str = level
    if match_str == 'DEBUG':
        logging.debug(msg)
    elif match_str == 'INFO':
        logging.info(msg)
    elif match_str == 'WARNING':
        logging.warning(msg)
    elif match_str == 'ERROR':
        logging.error(msg)
    elif match_str == 'CRITICAL':
        logging.critical(msg)
    else:
        error_msg = f'Log level error! Unknown log level {level}! {msg}'
        logging.error(error_msg)
        raise ValueError(error_msg)


def log_decorator(msg: str, level: str = 'INFO'):
    """Logging decorator.

    Args:
        msg (str): Log message
        level (str): Log level
    Returns:
        callable

    Examples:
        ```python
        @log_decorator('hello world', level='INFO')
        def func(): ...
        ```

    """

    def wrapper(func):
        def exc(*args, **kwargs):
            result = func(*args, **kwargs)
            log(msg, level)
            return result

        return exc

    return wrapper


def timer(func):
    """Timer decorator to record function execution time.

    Args:
        func: The function to be decorated
    Returns:
        wrapper: The decorated function

    Example:
        ```python
        @timer
        def func(): ...
        ```

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed_sec = end - start
        log(
            f'Function {func.__name__} took {elapsed_sec:.6f} seconds',
            level='INFO',
        )
        # Decorator arguments are only provided once at initialization
        return result

    return wrapper
