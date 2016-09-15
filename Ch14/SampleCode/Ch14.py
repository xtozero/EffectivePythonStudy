def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

x = 1
y = 0
result = divide(x, y)
if result is None:
    print('Invaid inputs')

print('-' * 40)

x = 0
y = 5
result = divide(x, y)
if not result:
    print('Invaid inputs')

print('-' * 40)

def divide_except(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise  ValueError('Invalid inputs') from e


x, y = 5, 2
try:
    result = divide(x, y)
except ValueError:
    print('Invaid inputs')
else:
    print('Result is %.1f' % result)