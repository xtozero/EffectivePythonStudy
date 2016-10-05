# 메타클래스로 클래스 속성에 주석을 달자

메타클래스를 이용하면 클래스를 정의한 다음 사용하기 이전에 속성을 수정하거나 주석을 붙이는 것이 가능하다. <br>
보통 이 기법은 디스크립터와 함께 사용한다. [(Ch31 참고)](../Ch31)
예를 들어 데이터베이스의 한 행을 표현하는 새 클래스를 정의한다고 하면 DB 테이블의 열에 대응하는 클래스의 속성이 있어야 한다.
```py
class Field(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, owner):
        if instance is None: return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)
```

한 행을 표현하는 클래스를 정의할 때는 클래스의 속성에 대응하는 행의 이름을 지정해야 한다.
```py
class Customer(object):
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')

foo = Customer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euclid'
print('Before:', repr(foo.first_name), foo.__dict__)

>>>
Before: '' {}
Before: 'Euclid' {'_first_name': 'Euclid'}
```

Field 디스크립터가 인스턴스 딕셔너리 __dict__를 기대한 대로 수정하는 것을 확인할 수 있다. <br>
다만 한 가지 아쉬운 점은 Customer 클래스에서 속성을 지정할 때 first_name = Field('first_name')처럼 first_name이 겹쳐서 사용된다는 점이다. <br>
이는 연산 순서가 Field('first_name')가 먼저 평가된 다음 속성에 할당되기 때문에 Field에서 어느 속성에 자신이 할당될지를 모른다는 문제가 있다. <br>
이런 중복성을 제거하는데 메타클래스가 사용될 수 있다.
```py
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls
```

메타클래스의 \_\_new\_\_ 메서드는 class의 본문이 끝나자마자 실행되어 원하는 동작을 처리할 수 있다. <br>
이제 이 메타클래스를 사용하는 기반 클래스를 정의하고 db의 행을 표현하는 클래스가 모두 이 클래스를 상속받게 한다.
```py
class DatabaseRow(object, metaclass=Meta):
    pass
```

Field 클래스는 메타클래스가 속성을 할당하므로 생성자에서 인수를 제거해 주면 된다.
```py
class Field(object):
    def __init__(self):
        self.name = None
        self.internal_name = None

    # 이하 코드는 이전 Field와 동일

class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()
```

이렇게 작성된 클래스는 이전과 같이 동작한다.
```py
foo = BetterCustomer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euclid'
print('Before:', repr(foo.first_name), foo.__dict__)

>>>
Before: '' {}
Before: 'Euclid' {'_first_name': 'Euclid'}
```

## 정리
1. 메타클래스를 통해서 클래스가 완전히 정의된 다음 클래스의 속성을 수정할 수 있다.
2. 메타클래스와 디스크립터를 연계해서 사용하면 메모리 누수와 weakref 모듈의 사용을 모두 피할 수 있다.