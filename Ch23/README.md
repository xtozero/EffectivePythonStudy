# 인터페이스가 간단하면 클래스 대신 함수를 받자

상당수의 파이썬 내장 API는 함수를 전달하여 동작을 커스터마이즈 할 수 있도록 하고 있다.

```py
names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=lambda x: len(x))
print(names)

>>>
['Plato', 'Socrates', 'Aristotle', 'Archimedes']
```

파이썬에서 함수는 일급 객체이기 때문에 함수의 인수로 전달할 수 있다. 또 다른 예를 보자.

defaultdict([Ch46참고](../Ch46))은 찾을 수 없는 키에 접근할 때마다 호출될 함수를 인수로 받는다. 이 함수는 defaultdict 클래스에 존재하지 않는 키에 대한 기본 값을 반환해야 한다.
```py
from collections import defaultdict

def log_missing():
    print('Key added')
    return 0

current = {'green': 12, 'blue': 3}
increments = [('red', 5), ('blue', 17), ('orange', 9)]
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After:', dict(result))

>>>
Before: {'blue': 3, 'green': 12}
Key added
Key added
After: {'orange': 9, 'blue': 20, 'green': 12, 'red': 5}
```

클로저 ([Ch15참고](../Ch15))를 사용하여 defaultdict에 없는 키의 개수를 셀 수도 있다.
```
def increment_with_report(current, increments):
    added_count = 0;

    def missing():
        nonlocal  added_count
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count

result, count = increment_with_report(current, increments)
print(count)

>>>
2
```

다만 이렇게 상태를 보존하는 클로저 함수는 상태가 없는 함수보다 이해하기가 어렵다. 또 다른 방법은 상태를 캡슐화하는 작은 클래스를 정의하는 것이다.
```py
class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter.missing, current)

for key, amount in increments:
    result[key] += amount

print(counter.added)
```

하지만 CountMissing 클래스만 보았을 때 용도가 무엇인지 바로 이해하기 어렵고 클래스 내의 missing 함수를 전달해야 하는 등 불편함이 있다.

파이썬에서는 클래스에 \_\_call\_\_ 특수 메서드를 정의해서 클래스를 함수처럼 호출할 수 있게 해준다.
```py
class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
# 호출 가능하다.
counter()
print(callable(counter))

print('-' * 40)
counter = BetterCountMissing()
result = defaultdict(counter, current)

for key, amount in increments:
    result[key] += amount

print(counter.added)

>>>
True
----------------------------------------
2
```

## 정리
1. 종종 컴포넌트 사이의 간단한 인터페이스용 클래스를 정의하지 않아도 함수만 써도 충분하다.
2. 파이썬의 함수는 일급 객체이다.
3. 파이썬 클래스를 함수처럼 사용하려면 특수 메서드 \_\_call\_\_을 정의해야 한다.
4. 상태를 저장하는 함수가 필요할 때는 호출 가능한 클래스를 이용하자