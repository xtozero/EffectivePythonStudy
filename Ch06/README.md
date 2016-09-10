# 한 슬라이스에 start, end, stride를 함께 쓰지 말자

파이썬 슬라이스는 가져올 아이템의 간격을 지정할 수 있다.
> sequence[start : end : __stride__]

이 문법을 사용하여 시퀀스의 홀수와 짝수 아이템을 손쉽게 얻을 수 있다.
```py
a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = a[::2]
evens = a[1::2]
print(odds)
print(evens)

>>>
['red', 'yellow', 'blue']
['orange', 'green', 'purple']
```

문제는 stride 문법이 원하지 않은 동작을 하여 버그를 만들어내기도 한다는 점이다. 예를 들어 문자열을 뒤집고 싶다면 stride를 -1로 하여 슬라이스하면 된다.
```py
x = b'mongoose'
y = x[::-1]
print(y)

>>>
b'esoognom'
```

위의 코드는 바이트 문자열이나 아스키 문자에는 잘 동작하지만 UTF-8 바이트 문자열로 인코드된 유니코드 문자에는 원하는데로 동작하지 않는다.
```py
w = '파이썬 코딩의 기술'
x = w.encode('utf-8')
y = x[::-1]
z = y.decode('utf-8')

>>>
Traceback (most recent call last):
  File "C:/Users/xtozero/Documents/GitHub/EffectivePythonStudy/Ch06/SampleCode/Ch06.py", line 14, in <module>
    z = y.decode('utf-8')
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa0 in position 0: invalid start byte
```

위의 코드는 유니코드 샌드위치를 어긴 방식이다. str으로 그대로 문자를 다루면 아래와 같이 정상적으로 슬라이스된다.
```py
y = w[::-1]
print(y)

>>>
술기 의딩코 썬이파
```

유니코드 샌드위치를 어긴 상황이 아니라도 stride 부분은 매우 혼란스러울 수 있다.
```py
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print(a[::2])
print(a[::-2])
print(a[2::2])
print(a[-2::-2])
print(a[-2:2:-2])
print(a[2:2:-2])

>>>
['a', 'c', 'e', 'g']
['h', 'f', 'd', 'b']
['c', 'e', 'g']
['g', 'e', 'c', 'a']
['g', 'e']
[]
```

대괄호 안에 숫자가 세 개나 있거나 stride가 음수인 경우 읽기가 어렵다. 이런 문제를 방지하기 위해서 stride를 start, end인덱스와 분리하여 사용하여야 한다.

stride를 양수 값으로 먼서 사용하고 그 결과에 start, end인덱스를 적용하는 것이 좋다.
```py
b = a[::2]
c = b[1:-1]
print(b)
print(c)

>>>
['a', 'c', 'e', 'g']
['c', 'e']
```

이렇게 슬라이싱의 나눠서 할 때 첫 번째 연산의 결과로 나오는 슬라이스의 크기를 최대한 줄이는 것이 좋다.

프로그램에서 두 과정에 필요한 시간과 메모리가 충분하지 않다면 내장 모듈 __itertool의 islice 메서드__( Ch46 참조 )를 사용하자 islice 메소드는 start, end, stride에 음수 값을 허용하지 않는다.

slice 객체를 이용해서 슬라이스에 이름을 붙이는 것도 가독성을 높이는데 도움을 준다.
```py
odd_elements = slice(0, None, 2)
print(a[odd_elements])

>>>
['a', 'c', 'e', 'g']
```

위와 같은 코드가 가능한 까닭은 sequence[start : end : stride] 표현식을 평가할 떄 아래와 같은 형식으로 함수를 호출하기 때문이다.
> sequence.\_\_getitem\_\_(slice(start, end, stride))

## 정리
1. 한 슬라이스에 start, end, stride를 모두 사용하는 것은 혼란스럽다.
2. 슬라이스에 start와 end인덱스 없이 양수 stride를 사용하자. 음수는 되도록 피하자
3. start, end, stride 파라미터를 모두 사용해야 한다면 두 단계로 나눠서 사용하거나 itertools.islice를 사용하자