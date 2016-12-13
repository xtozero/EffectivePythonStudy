# 디버깅 출력용으로는 repr 문자열을 사용하자

프로그램을 디버깅 할 때 print를 사용하여 상태를 검사하는 방법은 매우 유용하다. <br>
파이썬의 print 함수는 사람이 읽기 쉬운 문자열 버전으로 결과를 출력한다. <br>
다만 문제는 사람이 읽기 쉬운 문자열로 출력하는 과정에서 실제 타입이 무엇인지 파악하기 어렵다는 점이다. <br>
예로 print로 문자열 '5'와 숫자 5를 각각 출력해보면 동일하게 표시되는 것을 확인할 수 있다.
```py
print(5)
print('5')

>>>
5
5
```

따라서 객체를 명확하게 이해할 수 있는 문자열 표현을 제공하는 내장 함수 repr을 사용한다.
```py
print(repr(5))
print(repr('5'))

>>>
5
'5'
```

repr이 반환한 값을 내장 함수 eval에 전달하면 원래의 파이썬 객체와 동일한 결과가 나와야 한다.
```py
a = 5
b = eval(repr(a))
if a == b:
    print('Equal')
else:
    print('Not Equal')
```

동적 파이썬 객체의 경우 기본으로 사람이 이해하기 쉬운 문자열이 repr 값과 같다. <br>
즉 print에 동적 객체를 넘기면 명시적으로 repr을 호출하지 않아도 된다. 반면 object 인스턴스에 대한 repr의 기본값은 특별히 도움이 되지 않는다.
```py
class OpaqueClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = OpaqueClass(1, 5)
print(obj)

>>>
<__main__.OpaqueClass object at 0x004E5A70>
```

객체의 속성값에 대한 정보를 전혀 알려주지 않으며 eval 함수에 전달할 수도 없다. <br>
이 문제는 두 가지 방법으로 해결할 수 있다. <br>
1) \_\_repr\_\_이라는 특별한 메서드를 정의해서 객체를 재생성할 수 있는 파이썬 표현식을 담은 문자열을 반환한다.
```py
class ImprovedClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'ImprovedClass(%d, %d)' % (self.x, self.y)


one = ImprovedClass(1, 5)
other = eval(repr(one))
print(other)

>>>
ImprovedClass(1, 5)
```

2) \_\_dict\_\_ 속성에 저장된 객체의 인스턴스 딕셔너리를 이용한다.
```py
print(other.__dict__)

>>>
{'y': 5, 'x': 1}
```

## 정리
1. print는 사람이 보기 쉬운 형태로 자료를 가공하여 보여주나 본래의 타입을 알기 어렵다.
2. repr 내장 함수를 사용하면 타입 정보를 포함한 사람이 보기 쉬운 형태로 가공된 문자열 버전 값이 나온다.
3. repr의 결과를 eval에 전달하면 원래의 값을 얻을 수 있다.
4. \_\_repr\_\_ 메서드를 정의하여 클래스의 출력 가능한 표현을 사용자화 할 수 있다.
5. \_\_dict\_\_ 로 객체 내부의 속성을 볼 수 있다.
