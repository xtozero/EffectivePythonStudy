# range보다는 enumerate를 사용하자

range는 정수 집할을 순회하는 루프에서 유용하다.
```py
from random import randint


random_bits = 0
for i in range(64):
    if randint(0, 1):
        random_bits |= 1 << i

print(random_bits)

>>>
9990477111924273814
```

문자열 리스트와 같이 직접 순회할 자료구조가 있다면 직접 순회할 수도 있다.
```py
flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for flavor in flavor_list:
    print('%s is delicius' % flavor)

>>>
vanilla is delicius
chocolate is delicius
pecan is delicius
strawberry is delicius
```

때때로 리스트 아이템을 순회하면서 몇 번째 아이템을 순회 중인지 알고 싶은 경우 range를 사용할 수 있다.
```py
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d: %s is delicius' % (i + 1,  flavor))

1: vanilla is delicius
2: chocolate is delicius
3: pecan is delicius
4: strawberry is delicius
```

위의 코드는 range에서 flavor_list의 길이를 얻어 오는 것을 보았을 때 먼저 보았던 순회 예제보다 좋지 않아 보인다.

파이썬에서는 이런 상황을 처리하기 위해 내장 함수 enumerate를 제공한다. enumerate는 지연 제너레이터로 이터레이터를 감싸서 루프 인덱스와 다음 값을 한 쌍으로 넘겨준다.
```py
for i, flavor in enumerate(flavor_list):
    print('%d: %s' % (i + 1, flavor))

>>>
1: vanilla
2: chocolate
3: pecan
4: strawberry
```

enumerate는 두 번째 인자로 세기 시작할 수를 지정할 수 있으므로 코드를 더욱더 짧게 작성할 수 있다.
```py
for i, flavor in enumerate(flavor_list, 1):
    print('%d: %s' % (i, flavor))

>>>
1: vanilla
2: chocolate
3: pecan
4: strawberry
```

## 정리
1. 순회를 돌 때 인덱스값을 같이 알아야 할 경우에는 enumerate를 사용하는 것이 좋다.
2. enumerate는 시작 인덱스값을 정해 줄 수 있다.