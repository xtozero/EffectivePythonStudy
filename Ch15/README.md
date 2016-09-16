# 클로저가 변수 스코프와 상호 작용하는 방법을 알자

숫자 리스트를 정렬할 때 특정 그룹의 숫자들이 먼저 오도록 할 수 있다.
```py
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 7, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)

>>>
[2, 3, 5, 7, 7, 1, 6, 8]
```

위의 함수는 3가지 이유로 정상적으로 동작한다.
1. 파이썬은 __클로저를 지원__ 한다. 클로저는 자신이 정의된 스코프(Lexical Scope)에 있는 변수를 참조할 수 있는 함수이다.
2. 파이썬에서 __함수는 일급 객체__ 이다. 함수를 변수에 저장하거나, 함수의 인자로 전달하거나, 함수의 반환 값으로 사용할 수 있으면 함수 내부에서 새로운 함수를 정의할 수 있다.
3. 파이썬에는 튜플을 비교하는 특정한 규칙이 있는데 인덱스를 차례대로 증가해 나가면서 비교한다. 위의 예제에서 그룹 내부의 값이 먼저 나온 이유는 key 함수가 (0, x)를 반환하고 있기 때문이다.

만약 함수가 우선순위가 높은 아이템을 발견했는지 여부를 반환할 수 있도록 하는 기능을 추가한다고 하자.

클로저를 사용한다면 아래와 같이 코드를 작성할 수 있을 것이다.
```py
def sort_priority2(values, group):
    found = False
    def helper(x):
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found
    
found = sort_priority2(numbers, group)
print('Found:', found)
print(numbers)
>>>
Found: False
[2, 3, 5, 7, 7, 1, 6, 8]
```

결과는 올바르게 정렬되었지만, found 결과는 잘 못 되었다.

표현식에서 변수를 참조할 때 파이썬 인터프리터는 다음과 같은 순서로 스코프를 탐색한다.

1. 현재 함수의 스코프
2. 감싸고 있는 스코프 (현재 스코프를 담고 있는 다른 함수 같은)
3. 코드를 포함하고 있는 모듈의 스코프(전역 스코프)
4. 내장 스코프 (len이나 str같은 함수를 담고 있는)

이 중 어느 스코프에도 참조한 이름의 변수가 없으면 NameError 예외가 발생한다.

값을 할당하는 경우는 조금 다른데 변수가 현재 __스코프에 존재하지 않으면 변수의 정의로 취급하여 새로운 변수가 생성되게 된다.__ sort_priority2에서 found는 helper 함수에 정의되어 있지 않았고 새로운 found 변수가 할당되었기 때문에 값이 변하지 않았다.

sort_priority2를 의도한대로 동작하게 하려면 특별한 문법인 nonlocal을 사용해야 한다. nonlocal 문은 특정 변수 이름에 할당할 때 스코프 탐색이 일어나도록 한다. 다만 스코프 탐색의 4번째 단계 __내장 스코프까지는 탐색하지 않는다.__
```py
def sort_priority3(values, group):
    found = False

    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found

found = sort_priority3(numbers, group)
print('Found:', found)
print(numbers)

>>>
Found: True
[2, 3, 5, 7, 7, 1, 6, 8]
```

nonlocal 문은 변수 할당이 모듈 스코프에 직접 들어가게 하는 global 문을 보완한다.

하지만 간단한 함수 외에는 nonlocal을 사용하지 않아야 한다. nonlocal을 사용할 때 복잡해진다면 헬퍼 클래스로 상태를 감싸는 방법을 이용하는 것이 낫다.
```py
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
print('Found:', sorter.found)

>>>
Found: True
```

파이썬2에서는 nonlocal 키워드가 지원되지 않는데 리스트를 통해서 이를 해결할 수 있다.
```py
def sort_priority4(values, group):
    found = [False]

    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found[0]

found = sort_priority4(numbers, group)
print('Found:', found)
print(numbers)

>>>
Found: True
[2, 3, 5, 7, 7, 1, 6, 8]
```

found 변수의 현재 값은 스코프 탐색 방식에 의해서 상위 스코프를 검색해서 얻어온다 다만 found 변수가 수정 가능한 리스트이기 때문에 리스트의 원소를 수정하여 값을 찾았는지 반환하는 형태이다.

## 정리
1. 클로저 함수는 자신이 정의된 스코프 중 어디에 있는 변수도 참조할 수 있다.
2. 기본적으로 클로저에서 변수를 할당하면 외부 변수에 영향을 미치지 않는다.
3. 파이썬 3에서는 nonlocal 문을 통해서 클로저를 감싸고 있는 스코프의 변수를 수정할 수 있음을 알린다.
4. 파이썬 2에서는 수정 가능한 리스트와 같은 값을 전달하는 것으로 문제를 우회한다.
5. 간단한 함수 이외에는 nonlocal 문을 사용하지 말자