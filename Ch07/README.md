# map과 filter 대신 리스트 컴프리헨션을 사용하자

파이썬에는 리스트에서 다른 리스트를 만들어내는 문법이 있는데 이를 리스트 컴프리헨션이라고 한다.

어떤 리스트에 있는 각 숫자의 제곱을 구해서 새로운 리스트를 만든다고 하면 아래와 같이 리스트 컴프리헨션을 사용할 수 있다.
```py
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x ** 2 for x in a]
print(squares)

>>>
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

간단한 연산에는 내장 함수 map보다 리스트 컴프리헨션이 명확하다.
```py
squares = list(map(lambda x: x ** 2, a))
print(squares)

>>>
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

리스트 컴프리헨션에서는 입력 리스트에 있는 아이템을 쉽게 걸러낼 수도 있다.
```py
even_squares = [x ** 2 for x in a if x % 2 == 0]
print(even_squares)

>>>
[4, 16, 36, 64, 100]
```

내장함수 map에서 같은 동작을 수행하려면 내장 함수 filter를 같이 사용해야 한다.
```py
alt = map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)
```

map과 filter를 동시에 사용한 경우 한눈에 봐도 리스트 컴프리헨션보다 복잡하다.

딕셔너리와 세트에도 리스트 컴프리헨션에 해당하는 문법이 있다. 컴프리헨션 문법을 쓰면 알고리즘을 작성할 때 파생되는 자료구조를 쉽게 작성할 수 있다.
```py
chile_ranks = {'ghost': 1, 'habanero': 2, "cayenne": 3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}
chile_len_set = {len(name) for name in rank_dict.values()}
print(rank_dict)
print(chile_len_set)

>>>
{1: 'ghost', 2: 'habanero', 3: 'cayenne'}
{8, 5, 7}
```

## 정리
1. 리스트 컴프리헨션을 통해서 추가적인 lambda 표현식 없이 내장 함수 map, filter와 같은 기능을 사용할 수 있다.
3. 딕셔너리와 세트도 컴프리헨션 표현식을 지원한다.