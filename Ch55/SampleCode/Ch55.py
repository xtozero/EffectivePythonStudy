print(5)
print('5')

print('-' * 40)

print(repr(5))
print(repr('5'))

print('-' * 40)

a = 5
b = eval(repr(a))
if a == b:
    print('Equal')
else:
    print('Not Equal')

print('-' * 40)


class OpaqueClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = OpaqueClass(1, 5)
print(obj)

print('-' * 40)


class ImprovedClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'ImprovedClass(%d, %d)' % (self.x, self.y)


one = ImprovedClass(1, 5)
other = eval(repr(one))
print(other)

print(other.__dict__)
