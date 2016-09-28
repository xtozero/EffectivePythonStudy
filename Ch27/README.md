# 공개 속성보다는 비공개 속성을 사용하자

파이썬에서 클래스 속성의 가시성은 공개와 비공개만 있다.
```py
class SampleObject(object):
    def __init__(self):
        self.public_field = 5 # 어디서든 접근 가능
        self.__private_field = 10 # 외부에서 직접 접근 불가

    def get_private_field(self):
        return self.__private_field

obj = SampleObject()
print(obj.public_field)
print(obj.__private_field)

>>>
5
Traceback (most recent call last):
    print(obj.__private_field)
AttributeError: 'SampleObject' object has no attribute '__private_field'
```

공개 속성은 클래스 외부에서 자유롭게 접근 가능하지만 비공개 속성은 직접 접근할 수 없다. <br>
서브 클래스에서 부모 클래스의 비공개 속성에 접근하려고 해도 마찬가지로 접근할 수 없다. <br>
하지만 파이썬은 가시성을 C++, Java 등의 언어처럼 강하게 강제하는 것은 아니다. <br>
'객체.\_클래스명\_\_비공개속성이름' 으로 여전히 클래스 외부에서 접근할 수 있다.
```py
print(obj._SampleObject__private_field)

>>>
10
```

파이썬이 가시성을 강제하지 않는 이유는 가시성을 강제하는 것이 그렇지 않은 것보다 더 좋지 않다고 믿기 때문이다. <br>
그렇다면 비공개 속성은 왜 존재하는 것일까? <br>
일반적으로 보호 속성을 사용해서 서브 클래스가 더 많은 일을 할 수 있게 하는 것을 권장하며 보호 필드를 문서화 해서 그대로 둬야 할지 변경할 수 있을지 설명해놔야 한다.
```py
class ParentClass(object):
    def __init__(self, value):
        # 사용자가 객체에 전달한 값을 저장한다.
        # 문자열로 강제할 수 있는 값이어야 하며,
        # 객체에 할당하고 나면 불변으로 취급해야 한다.
        self.value = value
```

비공개 속성을 사용할지 고민할 시점은 서브 클래스와 이름이 충돌할 때다.
```py
class ApiClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' #충돌

a = Child()
print(a.get(), 'and', a._value, 'should be different'

>>>
hello and hello should be different
```

주로 클래스가 공개 API의 일부일 때 문제가 되는데 이런 충돌이 일어날 염려가 있다면 부모 클래스에서 비공개 속성을 사용해서 자식 클래스와 속성 이름이 겹치지 않게 하면 된다.
```py
class ApiClass(object):
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' #충돌

a = Child()
print(a.get(), 'and', a._value, 'should be different')

>>>
5 and hello should be different
```

## 정리
1. 파이썬은 비공개 속성을 엄격하게 강제하지 않는다.
2. 서브 클래스가 내부 API의 속성에 접근하지 못하게 막기보다 처음부터 내부 API와 속성으로 더 많은 일을 할 수 있도록 하자.
3. 보호 필드를 문서로 만들어 서브 클래스에 필요한 지침을 제공하자.
4. 직접 제어할 수 없는 서브 클래스와 이름이 충돌하지 않게 할 때만 비공개 속성을 사용하자.