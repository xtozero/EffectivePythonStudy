# super로 부모 클래스를 초기화하자

파이썬에서는 자식 클래스에서 부모 클래스를 초기화할 때 \_\_init\_\_ 메서드를 직접 호출하는 방법을 사용하였다.
```py
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
```

이런 방법은 간단한 클래스에서는 잘 동작하지만 __부모 클래스의 초기화 순서가 중요할 때__ 는 제대로 동작하지 못한다. <br>
아래 예제와 같이 다중상속을 받는 객체가 있다.
```py
class TimesTwo(object):
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    def __init__(self):
        self.value += 5


class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


foo = OneWay(5)
print('Five ordering is (5 * 2) + 5 =', foo.value)

>>>
Five ordering is (5 * 2) + 5 = 15
```

이 예제는 생각했던 것 처럼 동작한다. TimesTwo,  PlusFive는 \_\_init\_\_을 호출한 순서대로 초기화된다. <br>
그럼 상속받는 부모 클래스의 순서를 뒤바꿔도 생각했던 것 처럼 동작할까?
```py
class OneWay(MyBaseClass, PlusFive, TimesTwo):
# ...

>>>
Five ordering is (5 * 2) + 5 = 15
```

\_\_init\_\_을 이전과 같이 호출해주고 부모 클래스의 상속 순서를 변경하였으나 이전과 같이 동작하는 것을 볼 수 있다. <br>
또 다른 문제 상황은 __다이아몬드 상속__ 을 받을 때이다.
```py
class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5


class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2


class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)

foo = ThisWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)

>>>
Should be (5 * 5) + 2 = 27 but is 7
```

결과는 27이어야 하지만 다이아몬드 상속을 받아서 \_\_init\_\_이 두 번 호출되어 잘 못된 결과가 반환되었다. <br>
파이썬 2.2에서는 이 문제를 해결하기 위해서 super라는 내장 함수를 추가하고 메서드 해석 순서(MRO, Method Resolution Order)를 정의했다. <br>
MRO는 어떤 클래스부터 초기화 해야 하는지를 정해서 다이아몬드 상속에서 \_\_init\_\_이 두 번 이상 호출되는 것을 방지한다.
```py
class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super(TimesFiveCorrect, self).__init__(value)
        self.value *= 5


class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super(PlusTwoCorrect, self).__init__(value)
        self.value += 2


class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        super(GoodWay, self).__init__(value)

foo = GoodWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)

>>>
Should be (5 * 5) + 2 = 27 but is 35
```

그런데 여전히 값이 맞지 않는다. super로 호출되는 생성자의 순서는 MRO에 의해서 결정되기 때문이다. mro 클래스 메서드로 실행 순서를 확인할 수 있다.
```py
print(GoodWay.mro())

>>>
[<class '__main__.GoodWay'>, <class '__main__.TimesFiveCorrect'>, <class '__main__.PlusTwoCorrect'>, <class '__main__.MyBaseClass'>, <class 'object'>]
```

GoodWay -> TimesFiveCorrect -> PlusTwoCorrect -> MyBaseClass -> object 순으로 초기화가 되어 35가 나왔다는 것을 확인 할 수 있다.
그럼 __MRO의 순서를 변경__ 할 수 있을까? 아쉽게도 그것은 __불가능__ 하다. <br>
파이썬 3에서는 파이썬 2.2에서의 문법이 간략화되어 아래와 같이 super()를 호출할 수 있게 되었다.

```py
class Explicit(MyBaseClass):
    def __init__(self, value):
    # 클래스 내에서 __class__ 변수를 사용하면 현재 클래스를 올바르게 참조해 준다. 2.2에서는 사용할 수 없다.
        super(__class__, self).__init__(value * 2)


class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)


print(Explicit(10).value, Implicit(10).value)

>>>
20 20
```

## 정리
1. 파이썬의 표준 메서드 해석 순서는 슈퍼클래스의 초기화 순서와 다이아몬드 상속 문제를 해결한다.
2. 항상 내장 함수 super로 부모 클래스를 초기화해야 한다.