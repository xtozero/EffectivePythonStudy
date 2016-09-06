# 복잡한 표현식 대신 헬퍼 함수를 작성하자

파이썬은 풍부한 표현력을 가지는 언어로 많은 로직을 쉽게 작성할 수 있다.

URL에서 쿼리 문자열을 디코드해야 한다면 아래와 같이 코드를 작성할 수 있다.
```py
from urllib.parse import parse_qs

my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
print(repr(my_values))

>>>
{'blue': ['0'], 'red': ['5'], 'green': ['']}
```

parse_qs 함수의 결과로 반환되는 딕셔너리에 get()을 통해서 결괏값을 가져올 수 있는데 쿼리 문자열 파라미터에 따라서 값이 있을 수도 없을 수도 있다.
```py
print('Red          ', my_values.get('red'))
print('Green        ', my_values.get('green'))
print('Opacity      ', my_values.get('opacity'))

>>>
Red           ['5']
Green         ['']
Opacity       None
```

딕셔너리에 원하는 값이 없다면 0을 반환하도록 하여 일관되게 처리해 볼 수 있다.

딕셔너리의 get 함수는 두 번째 인자로 초깃값을 받을 수 있다. 빈 문자열 리스트가 암시적으로 False로 평가 되는 것을 이용하여 결괏값이 없을 때 일관되게 기본값 0을 얻을 수 있다.
```py
# dict.get(key, default=None)
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print('Red          ', red)
print('Green        ', green)
print('Opacity      ', opacity)

>>>
Red           5
Green         0
Opacity       0
```

다만 이 표현 식은 읽기가 난해하다. python2.5에서 추가된 if/else 조건식(삼항 연산자)을 이용해서 코드를 더 보기 쉽게 만들 수 있다.
```py
red = my_values.get('red', [''])
red = int(red[0]) if red[0] else 0
print('Red          ', red)
```

하지만 삼항 연산자도 여전히 복잡하며 여러 줄에 걸친 if/else 문을 대체할 정도로 명확하지는 않다. 재사용성도 떨어진다. 이 로직을 반복하는 경우 헬퍼 함수를 만드는 것이 좋다.
```py
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found is not None:
        found = int(found[0])
    else:
        found = default
    return found
```

## 정리
* 파이썬의 풍부한 표현력을 통해서 한 줄짜리 표현 식을 쉽게 작성할 수 있지만, 코드가 복잡해지고 읽기 어려워진다면 함축적인 문법을 사용하기보다 표현 식을 나누어 읽기 쉽게 하여 헬퍼 함수로 분리하는 것이 좋다.
