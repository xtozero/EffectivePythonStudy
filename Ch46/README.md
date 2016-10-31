# 내장 알고리즘과 자료 구조를 사용하자

파이썬의 표준 라이브러리는 많은 알고리즘과 자료 구조를 갖추고 있다. <br>
이 장에서는 파이썬이 제공하는 표준 라이브러리 중 몇 가지를 살펴본다. <br>

## double-ended queue
collections 모듈을 deque 클래스는 double-ended queue로 처음과 끝에 아이템을 삽입할 때 항상 일정한 시간이 걸리는 연산을 제공한다 <br>
이러한 기능은 선입선출 큐를 만들 때 이상적이다.
```py
from collections import deque

fifo = deque()
fifo.append(1)
x = fifo.popleft()
print(x)

>>>
1
```

내장 타입 list도 큐와 유사하게 사용할 수 있으나 리스트의 시작 부분에서 아이템을 삽입하거나 삭제하는 연산에는 선형적 시간이 걸린다.

## ordered dict
표준 딕셔너리는 해시테이블이기 때문에 정렬되어 있지 않다. 즉, 같은 키와 값을 담은 dict을 순회해도 다른 결과가 나온다.
```py
from random import randint

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
```

정렬된 딕셔너리가 필요한 경우 collections 모듈의 OrderedDict 클래스를 사용할 수 있다.
```py
from collections import OrderedDict

a = OrderedDict()
a['foo'] = 1
a['bar'] = 2

b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)
```

## 기본값을 가지는 딕셔너리가
딕셔너리는 통계를 관리하는 데 유용한데 딕셔너리를 사용할 때 어떤 키가 이미 존재한다고 가정할 수 없는 점이 까다롭다. <br>
이때 collections의 defaultdict 클래스를 사용해서 키가 존재하지 않으면 자동으로 기본값을 저장하도록 할 수 있다.
```py
from collections import defaultdict

stats = defaultdict(int)
stats['my_counter'] += 1
print(stats['my_counter'])
```

defaultdict 에는 기본값을 반환할 함수를 제공하면 되는데 위의 예제에서 내장 함수 int는 0을 반환한다.

## 힙 큐
힙은 우선순위 큐를 유지하는 데 유용한 자료 구조다. <br>
heapq 모듈을 사용하면 list타입으로 힙을 생성할 수 있다.
```py
from heapq import heappush, heappop, nsmallest

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

>>>
3 4 5 7
```

각 heapq 연산에 걸리는 시간은 리스트의 길이에 비례하여 로그 형태로 증가한다. <br>
반면 표준 파이썬 리스트로 같은 동작을 수행하면 시간이 선형적으로 늘어난다.

## 바이섹션
bisect_left 와 같은 bisect 모듈의 함수는 정렬된 아이템의 시퀀스를 대상으로한 이전 검색을 제공한다. <br>
bisect_left 가 반환한 인덱스는 시퀀스에 들어간 값의 삽입 지점이 된다.
```py
x = list(range(10**6))
i = x.index(991234)

j = bisect_left(x, 991234)
print(i, j)

>>>
991234 991234
```

## 이터레이터 도구
내장 모듈 itertools는 이터레이터를 구성하거나 상호 작용하는 데 유용한 함수를 제공한다. <br>
itertools는 크게 세 가지 주요 카테고리로 나뉜다.
- 이터레이터 연결
1. chain : 여러 이터레이터를 하나의 순차적인 이터레이터로 결합한다.
2. cycle : 이터레이터의 아이템을 영원히 반복한다.
3. tee : 이터레이터 하나를 병렬 이터레이터 여러 개로 나눈다.
4. zip_longest : 길이가 서로 다른 이터레이터들에도 잘 동작하는 zip이다.

- 이터레이터에서 아이템 필터링
1. islice : 복사 없이 이터레이터를 숫자로 된 인덱스로 슬라이스한다.
2. takewhile : 서술 함수(predicate function)가 True를 반환하는 동안 이터레이터의 아이템을 반환한다.
3. dropwhile : 서술 함수가 처음으로 False를 반환하고 나면 이터레이터의 아이템을 반환한다.
4. filterfalse : 서술 함수가 False를 반환하는 이터레이터의 모든 아이템을 반환한다. filter의 반대기능이다.

- 이터레이터에 있는 아이템의 조합
1. product : 이터레이터의 아이템들의 카테시안 곱을 반환한다.
2. permutations : 이터레이터에 있는 아이템을 담은 길이 N의 순서 있는 순열을 반환한다.
3. combinations : 이터레이터에 있는 아이템을 중복되지 않게 담은 길이 N의 순서 없는 조합을 반환한다.

## 정리
1. 파이썬 표준라이브러리는 다양한 알고리즘과 자료구조를 제공한다.
2. 기능을 직접 만들기보다는 표준라이브러리가 제공하는 기능을 사용하자.