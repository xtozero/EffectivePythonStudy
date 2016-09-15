# None을 반환하기보다는 예외를 일으키자

헬퍼 함수를 작성할 때 None을 반환하는 것이 자연스러워 보이는 경우가 있다.

만약 어떤 헬퍼 함수 어떤 숫자를 다른 숫자로 나눈다고 했을 때 0으로 나눌 떄에는 결과가 정의되어 있지 않으므로 None을 반환하는 게 자연스럽다. 하지만 이 함수의 값을 출력할 때는 아래와 같이 항상 검사가 필요하다.
```py
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

x = 1
y = 0

result = divide(x, y)
if result is None:
    print('Invaid inputs')

>>>
Invaid inputs
```

None에 특별한 의미를 정하면 아래와 같이 False에 해당하는 값으로 에러가 발생했는지를 검사( None은 암시적으로 False이므로 )했을 때 잘 못된 결과가 발생한다.
```py
x = 0
y = 5
result = divide(x, y)
if not result: # 0도 마찬가지로 암시적으로 False이다.
    print('Invaid inputs')

>>>
Invaid inputs
```

이런 경우를 해결하는 방법은 절대로 None을 반환하지 않고 대신 예외를 발생시키는 것이다.
```py
x, y = 5, 2
try:
    result = divide(x, y)
except ValueError:
    print('Invaid inputs')
else:
    print('Result is %.1f' % result)

>>>
Result is 2.5
```

예외를 발생시키면 try, except, else, finally 구문을 통해서 쉽게 결과를 다룰 수 있고 더는 반환 값을 조건식으로 검사하지 않아도 된다.

## 정리
1. None을 반환하면 암시적으로 False로 평가되는 것을 이용한 조건식에서 의도한 것과 다르게 동작할 수 있다.
2. 함수에서 None을 반환하기보다는 예외를 발생시키는 것이 더 좋다.