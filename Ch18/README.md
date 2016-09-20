# 가변 위치 인수로 깔끔하게 보이게 하자

가변 위치 인수를 사용하면 함수를 더욱더 깔끔하게 작성할 수 있다.

로그를 남기는 함수를 아래와 같이 작성한다고 해보자
```py
def log( message, values ):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))

log('My numbers are', [1, 2])
log('Hi there', [])

>>>
log('My numbers are', [1, 2])
log('Hi there', [])
```

로그에 넘길 인수가 없어도 불필요하게 빈 리스트를 넘겨야만 한다. 두 번째 인수를 넘길 필요가 없다면 아예 넘기지 않는 것이 더 좋다.

파이썬에서는 * 기호를 인수에 사용하면 가변 위치 인수를 사용할 수 있다. 아래 예제와 같이 두 번째 인수에 붙이면 첫 ㄴ번째 인수를 필수지만 두 번째 인수는 선택적으로 전달할 수 있다.
```py
def log2(message, *values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))

log2('My numbers are', [1, 2])
log2('Hi there')

>>>
My numbers are: [1, 2]
Hi there
```

만약 리스트를 log2 와 같은 가변 인수에 넘기고 싶다면 * 연산자를 써서 전달하면 된다.
```py
numbers = [1, 2, 3, 4, 5]
log2('You number is', *numbers)

>>>
You number is: 1, 2, 3, 4, 5
```

다만 가변 위치 인수는 두 가지 문제점이 있다.
1. 가변 인수가 함수에 전달되기에 앞서 항상 튜플로 변환되기 때문에 제너레이터를 전달하여도 메모리 부족이 일어날 수 있다.
2. 다음부터 새 위치 인수를 추가할 때 호출 코드를 수정하지 않으면 예상치 않은 버그가 발생할 수 있다.

제너레이터가 튜플로 변환되는 현상은 아래의 코드에서 확인해 볼 수 있다.
```py
def generator():
    for i in range(10):
        yield i


def test_func(*args):
    print(args)

it = generator()
test_func(*it)

>>>
(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
```

따라서 가변 호출 인수는 함수의 인수가 매우 크지 않을 때 사용할 수 있는 방식이다.

추후 호출 코드를 수정하지 않았고 새 위치 인수를 추가하였을 때 기존 호출 코드가 문제를 일으키는 현상은 아래의 코드에서 확인해 볼 수 있다.
```py
def log3(sequence, message, *values):
    if not values:
        print('%s: %s' %(sequence, message))
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s: %s' % (sequence, message, values_str))

log3(1, 'My numbers are', [1, 2])
log3('My numbers are', [1, 2])
log3('Hi there')
>>>
1: My numbers are: [1, 2]
My numbers are: [1, 2]
Traceback (most recent call last):
  File "C:/Users/xtozero.NEXON/Documents/GitHub/EffectivePythonStudy/Ch18/SampleCode/Ch18.py", line 55, in <module>
    log3('Hi there')
TypeError: log3() missing 1 required positional argument: 'message'
```

첫 번째로 호출되는 함수는 정상적으로 동작한다.

두 번째로 호출되는 log3 함수에서는 아무런 에러 없이 함수가 오동작하는 것을 볼 수 있다. 

세 번째로 호출하는 log3 함수에서는 새로 추가된 sequence 인수로 인해서 message 인수가 전달되지 않아서 에러가 발생한 것을 볼 수 있다. 첫 번째 경우보다는 그나마 낫다.

이런 버그가 생길 가능성을 없애려면 가변 인수를 받는 함수를 확장할 때 키워드 전용 인수를 사용하는 것이 좋다.[(Ch21 참고)](../Ch21)

## 정리
1. *를 사용해서 가변 인수를 받을 수 있다.
2. 가변 인수를 사용하면 인수를 튜플로 변환하기 때문에 많은 메모리를 사용할 위험이 있다.
3. 가변 인수를 사용하면 추후 인수를 추가할 때 함수가 오동작할 수 있다.
