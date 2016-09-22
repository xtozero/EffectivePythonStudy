def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division(1, 10**500, True, False)
print(result)
result = safe_division(1, 0, False, True)
print(result)

print('-' * 40)


def safe_division_2(number, divisor, ignore_overflow=False, ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division_2(1, 10**500, ignore_overflow=True)
print(result)
result = safe_division_2(1, 0, ignore_zero_division=True)
print(result)

print('-' * 40)


def safe_division_3(number, divisor, *, ignore_overflow=False, ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# 아래 주석을 해제하면 에러가 발생
# result = safe_division_3(1, 10**500, True, False)


def safe_division_ver_python2(number, divisor, **kwargs):
    ignore_overflow = kwargs.pop('ignore_overflow', False)
    ignore_zero_division = kwargs.pop('ignore_zero_division', False)
    # 여기서 kwargs에 여전히 변수가 남아있는 지를 검사
    if kwargs:
        raise TypeError('Unexpected **kwargs : %r' % kwargs)
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# 아래 주석을 해제하면 에러가 발생
# result = safe_division_ver_python2(1, 10**500, True, False)
# result = safe_division_ver_python2(0, 0, unexpected=True)