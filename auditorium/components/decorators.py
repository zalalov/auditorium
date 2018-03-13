import functools
from time import sleep


def no_exceptions(func):
    """
    Decorator to ignore exceptions
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            pass

    return wrapper


def inf(func):
    """
    Infinity loop
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)

    return wrapper


def sleep_after(seconds=0):
    """
    Sleep after execution
    :param seconds:
    :return:
    """
    def interval(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

            sleep(seconds)
        return wrapper
    return interval
