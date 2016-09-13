a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = a[::2]
evens = a[1::2]
print(odds)
print(evens)

print('-' * 40)

x = b'mongoose'
y = x[::-1]
print(y)

print('-' * 40)

w = '파이썬 코딩의 기술'
x = w.encode('utf-8')
y = x[::-1]
# 아래 코드 주석을 풀면 에러가 납니다.
# z = y.decode('utf-8')

# 유니코드 샌드위치를 지켜서 스트라이드 해야합니다.
y = w[::-1]
print(y)

print('-' * 40)

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print(a[::2])
print(a[::-2])
print(a[2::2])
print(a[-2::-2])
print(a[-2:2:-2])
print(a[2:2:-2])

print('-' * 40)

b = a[::2]
c = b[1:-1]
print(b)
print(c)

print('-' * 40)

odd_elements = slice(0, None, 2)
print(a[odd_elements])
