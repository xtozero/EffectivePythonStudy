from datetime import datetime
from time import sleep
import json


def log(message, when=datetime.now()):
    print('%s: %s' % (when, message))

log('Hi there!')
sleep(0.1)
log('Hi again!')

print('-' * 40)


def log2(message, when=None):
    """
    :param message: Message to print.
    :param when: datetime of when the message occurred. Default to the present time
    :return: None
    """
    when = datetime.now() if when is None else when
    print('%s: %s' % (when, message))

log2('Hi there!')
sleep(0.1)
log2('Hi again!')

print('-' * 40)


def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also data')
bar['meep'] = 1
print('Foo: ', foo)
print('Bar: ', bar)

print('-' * 40)


def decode2(data, default=None):
    ''' Load Json data from a string
    :param data: JSON data to decode
    :param default: Value to return if decoding fails Default to an empty dictionary
    :return: None
    '''
    try:
        return json.loads(data)
    except ValueError:
        return {} if default is None else default

foo = decode2('bad data')
foo['stuff'] = 5
bar = decode2('also data')
bar['meep'] = 1
print('Foo: ', foo)
print('Bar: ', bar)