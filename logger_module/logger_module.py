import functools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f'Entering function {func.__name__}')
            result = func(*args, **kwargs)
            # logger.info(f'Exiting function {func.__name__}{result}')
            return result
        except Exception as error:
            logger.exception(f'Exception raised in {func.__name__}. exception: {str(error)}')
            raise error
    return wrapper