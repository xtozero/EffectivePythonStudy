# functools.wraps 함수 데코레이터를 정의하자

파이썬에는 함수에 적용되는 데코레이터라는 문법이 있다. <br>
데코레이터는 감싸고 있는 함수를 호출하기 전이나 후에 필요한 작업을 수행할 수 있도록 해준다. <br>
```py
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r %r) -> %r' %(func.__name__, args, kwargs, result ) )
        return result
    return wrapper


@trace
def fibonacci(n):
    """n 번째 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


fibonacci(3)

>>>
fibonacci((1,) {}) -> 1
fibonacci((0,) {}) -> 0
fibonacci((1,) {}) -> 1
fibonacci((2,) {}) -> 1
fibonacci((3,) {}) -> 2
```

위와 같은 데코레이터를 호출하는 것은 결국 아래와 같은 코드와 똑같이 동작한다.
```py
fibonacci = trace(fibonacci)
```

다만 이렇게 작성된 데코레이터는 한가지 문제점이 있는데 데코레이터에서 반환된 객체가 fibonacci 함수가 아니라는 점이다.
```py
print(fibonacci)

>>>
<function trace.<locals>.wrapper at 0x0053BAE0>
```

데코레이터 내부에서 wrapper 함수를 정의한 다음 반환하였기 때문에 나타나는 당연한 결과이나 객체 내부를 조사하는 도구를 사용할 때( [Ch44](../Ch44), [Ch57](../Ch57) 참고 ) 문제가 될 수 있다.
예를 들어 데코레이터가 적용된 fibonacci함수는 help가 제대로 동작하지 않는다.
```py
help(fibonacci)

>>>
Help on function wrapper in module __main__:

wrapper(*args, **kwargs)
```

해결방법은 functools.wraps 헬퍼 함수를 사용하는 것이다. functools.wraps는 데코레이터를 작성하는 데 사용하는 데코레이터이다.<br>
이 데코레이터는 중요한 메타 정보를 모두 외부 함수에 복사해서 객체 내부를 조사하는 도구를 사용해도 정상적으로 동작할 수 있도록 해준다.
```py
def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # ...


@trace
def fibonacci(n):
    # ...

help(fibonacci)

>>>
fibonacci(n)
    n 번째 피보나치 수를 반환한다.
```

help 함수가 정상적으로 동작하는 것을 확인할 수 있다.

## 정리
1. 데코레이터는 함수 호출 전이나 후에 원하는 동작을 할 수 있도록 해준다.
2. 데코레이터를 사용하면 객체 내부를 조사하는 도구를 사용할 경우 정상적으로 작동하지 않을 수 있다.
3. functools.wraps 데코레이터를 사용해서 원치 않은 동작을 하는 것을 피할 수 있다.