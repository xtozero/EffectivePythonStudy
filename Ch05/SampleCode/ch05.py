a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('First four', a[:4])
print('Last four', a[-4:])
print('Middle four', a[3:-3])

# 처음부터 슬라이스
assert a[:5] == a[0:5]
# 끝까지 슬라이스
assert a[0:] == a[0:len(a)]

print('-'*40)

print(a[:])
print(a[:5])
print(a[:-1])
print(a[4:])
print(a[-3:])
print(a[2:5])
print(a[2:-1])
print(a[-3:-1])

print('-'*40)

first_twenty_items = a[:20]
last_twenty_items = a[-20:]
print(first_twenty_items)
print(last_twenty_items)

print('-'*40)

b = a[4:]
print('Before   ', b)
b[1] = 99
print('After    ', b)
print('No change', a)

print('-'*40)

print('Before   ', a)
a[2:7] = [99, 22, 14]
print('After    ', a)

print('-'*40)

b = a[:]
assert b == a and b is not a

b = a
print('Before', a)
a[:] = [101, 102, 103]
assert a is b
print('After', a)
