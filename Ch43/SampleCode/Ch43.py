from threading import Lock
import logging
from contextlib import contextmanager

# lock = Lock()
# lock.acquire()
# try:
#    print('Critical Section')
# finally:
#    lock.release()

# 아래의 코드는 완전히 동일하게 동작한다.

# lock = Lock()
# with lock:
#     print('Critical Section')

print('-' * 40)


def logging_function():
    logging.debug('Some debug data')
    logging.error('Error log')
    logging.debug('More debug data')

# logging_function()

print('-' * 40)


@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)

with debug_logging(logging.DEBUG):
    print('Inside:')
    logging_function()
print('After')
logging_function()

with open('test.txt', 'w') as handle:
    handle.write('Some data')


@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug('This is my message!')
    logging.debug('This will not print')

logger = logging.getLogger('my-log')
logger.debug('This will not print')