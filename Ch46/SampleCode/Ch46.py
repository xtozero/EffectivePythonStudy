from collections import deque
from random import randint
from collections import OrderedDict
from collections import defaultdict
from heapq import heappush, heappop, nsmallest
from bisect import bisect_left


fifo = deque()
fifo.append(1)
x = fifo.popleft()
print(x)

print('-' * 40)

a = {}
a['foo'] = 1
a['bar'] = 1

# 해시 충돌을 일으킨다.
while True:
    z = randint(99, 1013)
    b = {}
    for i in range(z):
        b[i] = i
    b['foo'] = 1
    b['bar'] = 1
    for i in range(z):
        del b[i]
    if str(b) != str(a):
        break;

print(a)
print(b)
print('Equal?', a == b)

print('-' * 40)

a = OrderedDict()
a['foo'] = 1
a['bar'] = 2

b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)

print('-' * 40)

stats = defaultdict(int)
stats['my_counter'] += 1
print(stats['my_counter'])

print('-' * 40)

# a 리스트에 힙과 같이 삽입
a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)

# 자동으로 정렬되어 가장 작은 값이 인덱스 0번에 옴
assert a[0] == nsmallest(1, a)[0] == 3

# pop할 때는 가장 작은 값 부터 제거
print(heappop(a), heappop(a), heappop(a), heappop(a))

print('-' * 40)

x = list(range(10**6))
i = x.index(991234)

j = bisect_left(x, 991234)
print(i, j)
