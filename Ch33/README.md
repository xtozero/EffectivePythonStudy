# 메타클래스로 서브클래스를 검증하자

메타클래스를 사용하면 클래스를 올바르게 정의했는지 검증할 수 있다. <br>
복잡한 클래스 계층을 만들 때 스타일을 강제하거나 메서드를 오버라이드하도록 강제하고 클래스 속성 사이에 철저한 관계를 두고 싶다면 메타클래스를 사용하여 서브클래스가 정의될 때마다 검증코드가 실행되도록 할 수 있다. <br>
보통 검증 코드는 클래스의 객체가 생성될 때 \_\_init\_\_메서드에서 실행된다.

서브클래스 검증용 메타클래스를 작성하기에 앞서 메타클래스가 어떻게 동작하는지 알아보자 <br>
메타클래스는 type 객체를 상속하여 정의한다.
```py
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        # 연관된 클래스의 컨텐츠를 받는다.
        print((meta, name, bases, class_dict))
        return type.__new__(meta, name, bases, class_dict)


class SubClass(object, metaclass=Meta):
    stuff = 123

    def foo(self):
        pass

>>>
(<class '__main__.Meta'>, 'SubClass', (<class 'object'>,), {'__qualname__': 'SubClass', 'foo': <function SubClass.foo at 0x005ABAE0>, '__module__': '__main__', 'stuff': 123})
```

메타클래스는 클래스의 이름, 상속하는 부모 클래스, class 본문에서 정의한 모든 클래스 속성에 접근할 수 있다. <br>
파이썬2는 문법이 약간 달라서 \_\_metaclass\_\_ 속성으로 메타클래스를 지정한다. 그래도 Meta.\_\_new\_\_인터페이스는 같다.
```py
class SubClassInPython2(object):
    __metaclass__ = Meta
    stuff = 123

    def foo(self):
        pass
```

클래스가 정의되기 전에 클래스의 모든 파라미터를 검증하려면 Meta.\_\_new\_\_ 메서드에 기능을 추가하면 된다.
```py
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # 추상 Polygon 클래스는 검증하지 않음
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)


class Polygon(object, metaclass=ValidatePolygon):
    sides = None  # 서브 클래스에서 설정

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    sides = 3
```

요구 조건을 만족하지 않는 클래스를 정의하면 class 문의 본문이 끝나자마자 class 문을 실패하게 만들어 프로그램이 실행되지 않는다.
```py
class Triangle(Polygon):
    sides = 3

print('Before class')


class Line(Polygon):
    print('Before sides')
    sides = 1
    print('After sides')
print('After class')

>>>
Before class
Before sides
After sides
Traceback (most recent call last):
    class Line(Polygon):
    raise ValueError('Polygons need 3+ sides')
ValueError: Polygons need 3+ sides
```

## 정리
1. 클래스를 검증하는 데는 메타클래스를 사용할 수 있다.
2. 파이썬2와 파이썬3의 메타클래스 문법은 약간 다르다.
3. 메타클래스의 \_\_new\_\_메서드는 class 문 본문 전체가 처리된 다음 실행된다.