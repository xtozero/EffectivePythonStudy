def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))

log('My numbers are', [1, 2])
log('Hi there', [])

print('-' * 40)


def log2(message, *values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))

log2('My numbers are', [1, 2])
log2('Hi there')

print('-' * 40)

numbers = [1, 2, 3, 4, 5]
log2('You number is', *numbers)

print('-' * 40)


def generator():
    for i in range(10):
        yield i


def test_func(*args):
    print(args)

it = generator()
test_func(*it)

print('-' * 40)


def log3(sequence, message, *values):
    if not values:
        print('%s: %s' %(sequence, message))
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s: %s' % (sequence, message, values_str))

log3(1, 'My numbers are', [1, 2])
log3('My numbers are', [1, 2])
log3('Hi there')
