# 게터와 세터 메서드 대신에 일반 속성을 사용하자

다른 언어를 사용했던 프로그래머들이 자연스럽게 클래스에 getter와 setter메서드를 명시적으로 구현하는 때도 있다.
```py
class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

r0 = OldResistor()
r0.set_ohms(r0.get_ohms + 5e3)
```

getter와 setter는 익숙하게 사용할 수 있지만 값을 증가시키는 연산 등에서 사용하기가 까다롭다. <br>
이런 메서드가 인터페이스를 정의하고 기능을 캡슐화는 등의 장점이 있지만 파이썬에서는 거의 사용되지 않는다. <br>
파이썬에서는 대신에 공개 속성을 작성한다. 
```py
class ModernResistor(object):
    def __init__(selfs, ohms):
        selfs.ohms = ohms
        selfs.voltage = 0
        selfs.current = 0

r1 = ModernResistor(50e3)
r1.ohms = 10e3
r1.ohms += 5e3
```

값을 증가시키는 연산도 자연스럽게 작성할 수 있다. <br>
나중에 속성에 값이 설정될 때 특별한 동작이 일어나야 하면 @property 데코레이터와 setter 메서드를 사용하는 방식으로 변경할 수 있다.
```py
class PropertyResistor(ModernResistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

r2 = PropertyResistor(1e3)
print('Before: %5r amps' % r2.current)
r2.voltage = 10
print('After: %5r amps' % r2.current)

>>>
Before:     0 amps
After:  0.01 amps
```

제대로 동작하려면 보호 속성값을 사용해야 하며 setter와 getter 메서드의 이름이 속성의 이름과 일치해야 한다. <br>
@property는 부모 클래스의 속성을 불편으로 만드는 데도 사용할 수 있다.
```py

class FixedResistor(ModernResistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._ohms = ohms

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError('Can\'t set attribute')
        self._ohms = ohms

r4 = FixedResistor(1e3)
r4.ohms = 2e3

>>>
Traceback (most recent call last):
    raise AttributeError('Can\'t set attribute')
AttributeError: Can't set attribute
```

@property의 단점은 속성에 대응하는 메서드를 서브 클래스에만 공유할 수 있다는 점이다. <br>
서로 관련이 없는 클래스는 같은 구현을 공유하지 못한다. <br>
하지만 파이썬은 재사용 가능한 속성 로직을 가능하게 하는 디스크립터를 제공한다. [(Ch31 참고)](../Ch31) <br>
마지막으로 getter와 setter 함수에서는 값을 설정하는 이외의 동작을 해선 안 된다. 복잡하거나 느린 작업은 일반 메서드로 분리하는 것이 좋다.

## 정리
1. 파이썬에서는 getter와 setter 메서드를 만들기보다 공개 속성을 사용하는 것이 좋다.
2. 속성에 접근할 때 특정 동작을 해야 할 때 @property를 사용하자
3. getter와 setter가 속성에 값을 가져오거나 설정하는 이외의 행위를 하지 않도록 하자.
4. 느리거나 복잡한 메서드는 별도의 메서드로 만들자