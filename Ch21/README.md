# 키워드 전용 인수로 명료성을 강요하자

[Ch19](../Ch19)에서 다루었다시피 파이썬 함수는 키워드 인수를 사용할 수 있다.

아래의 예제는 예외 무시 동작을 제어하는 두 bool 인수의 순서를 혼동할 여지가 있는 함수를 보여준다.
```py
def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division(1, 10**500, True, False)
result = safe_division(1, 0, False, True)

>>>
0.0
inf
```

이런 코드의 가독성을 높이기 위해서 키워드 인수를 사용할 수 있다.
```py
def safe_division_2(number, divisor, ignore_overflow=False, ignore_zero_division=False):
# ... 이하 위의 safe_division와 같음

result = safe_division_2(1, 10**500, ignore_overflow=True)
print(result)
result = safe_division_2(1, 0, ignore_zero_division=True)
print(result)

>>>
0.0
inf
```

하지만 [Ch19](../C19)에서 다루었던 것 처럼 키워드 인수를 사용해도 여전히 위치 인수로 전달하는 것이 가능하다.

이런 동작을 막기 위해서 키워드 전용 인수로 함수를 정의하여 의도를 명확히 드러내도록 할 수 있다. __키워드 전용 인수는 위치로는 절대 넘길 수 없도록 강제를 해준다.__
```py
def safe_division_3(number, divisor, *, ignore_overflow=False, ignore_zero_division=False):
# ... 이하 위의 safe_division와 같음

result = safe_division_3(1, 10**500, True, False)

>>>
TypeError: safe_division_3() takes 2 positional arguments but 4 were given
```

---

파이썬 2에서는 키워드 전용 인수를 지정하는 명시적인 방법이 없다. 다만 인수 리스트에 ** 연산자를 사용해서 올바르지 않은 함수 호출 시 예외를 발생시키도록 할 수 있다.
```py
def safe_division_ver_python2(number, divisor, **kwargs):
    ignore_overflow = kwargs.pop('ignore_overflow', False)
    ignore_zero_division = kwargs.pop('ignore_zero_division', False)
    # 여기서 kwargs에 여전히 변수가 남아있는 지를 검사
    if kwargs:
        raise TypeError('Unexpected **kwargs : %r' % kwargs)
    # ... 이하 위의 safe_division와 같음

result = safe_division_ver_python2(1, 10**500, True, False)
result = safe_division_ver_python2(0, 0, unexpected=True)

>>>
TypeError: safe_division_ver_python2() takes 2 positional arguments but 4 were given
TypeError: Unexpected **kwargs : {'unexpected': True}
```

## 정리
1. 키워드 인수는 함수 호출의 의도를 명확하게 해준다.
2. 파이썬3는 함수의 키워드 전용 인수 문법을 지원한다.
3. 파이썬2에서는 **문법을 사용하고 TypeError를 직접 일으키는 방법으로 의도를 명확하게 파악하는 것을 강제할 수 있다.