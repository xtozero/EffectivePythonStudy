from functools import wraps


def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r %r) -> %r' %(func.__name__, args, kwargs, result ) )
        return result
    return wrapper


@trace
def fibonacci(n):
    """n 번째 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


fibonacci(3)
print('-' * 40)

print(fibonacci)

print('-' * 40)
help(fibonacci)

print('-' * 40)


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r %r) -> %r' %(func.__name__, args, kwargs, result ) )
        return result
    return wrapper


@trace
def fibonacci(n):
    """n 번째 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)

help(fibonacci)
