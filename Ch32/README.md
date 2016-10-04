# 지연 속성에는 \_\_getattr\_\_, \_\_getattribute\_\_, \_\_setattr\_\_을 사용하자

DB 테이블의 한 행을 파이썬 객체로 표현할 때 DB의 형태를 모르는 상태로 범용적인 코드를 작성할 수 있다. <br>
다만 사용하기에 앞서 정의가 필요한 일반 인스턴스 속성, @property메서드 디스크립터는 이렇게 할 수 없고 \_\_getattr\_\_ 특수 메서드를 통해서 이런 코드를 작성할 수 있게 해준다. <br>
클래스에 \_\_getattr\_\_ 메서드를 정의하면 객체의 인스턴스 딕셔너리에서 속성을 찾을 수 없을 때 \_\_getattr\_\_ 메서드가 호출된다.
```py
class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

db = LazyDB()
print('Before:', db.__dict__)
print('Foo:', db.foo)
print('After:', db.__dict__)

>>>
Before: {'exists': 5}
Foo: Value for foo
After: {'exists': 5, 'foo': 'Value for foo'}
```

인스턴스 딕셔너리에 없는 속성에 접근하였을 때 \_\_getattr\_\_가 호출되는 것을 확인할 수 있다. <br>
다음은 \_\_getattr\_\_가 실제로 호출되는 시점을 확인해 보자.
```py
class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

db = LoggingLazyDB()
print('Exist:', db.exists)
print('Foo:', db.foo)
print('Foo:', db.foo)

>>>
Exist: 5
Called __getattr__(foo)
Foo: Value for foo
Foo: Value for foo
```

exist 속성은 인스턴스 딕셔너리에 존재하므로 \_\_getattr\_\_가 호출되지 않는 것을 확인할 수 있다. <br>
foo는 인스턴스 딕셔너리에 없으므로 처음 접근할 때 \_\_getattr\_\_가 호출된다. 하지만 한번 접근하면 setattr함수로 인해서 딕셔너리에 저장되게 되고 두 번째 접근에서는 호출되지 않는다. <br>
이런 동작은 속성에 지연(Lazy) 접근하는 경우에 특히 도움이 된다. <br>
다른 가정으로 DB에 트랜잭션이 필요한 상황에서 대응하는 DB의 행이 여전히 유효한지 알고 싶다면 인스턴스 딕셔너리를 사용하는 \_\_getattr\_\_로는 불충분하다. <br>
파이썬에는 이런 쓰임새를 고려한 \_\_getattribute\_\_ 특수 메서드가 제공된다. <br>
\_\_getattribute\_\_ 는 \_\_getattr\_\_ 와는 다르게 _속성에 접근할 때 항상 호출_ 되며 _인스턴스 딕셔너리에 해당 속성이 있어도 호출된다._
```py
class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

db = ValidatingDB()
print('Exist:', db.exists)
print('Foo:', db.foo)
print('Foo:', db.foo)

>>>
Called __getattribute__(exists)
Exist: 5
Called __getattribute__(foo)
Foo: Value for foo
Called __getattribute__(foo)
Foo: Value for foo
```

동적으로 접근하는 속성이 존재하지 않아야 할 때에는 AttributeError를 일으켜서 파이썬 표준 동작이 일어나게 할 수 있다.
```py
class MissingPropertyDB(object):
    def __getattr__(self, name):
        if name == 'invalid_name':
            raise AttributeError('%s is invalid name' % name)
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

db = MissingPropertyDB()
db.invalid_name

>>>
Traceback (most recent call last):
db.invalid_name
raise AttributeError('%s is invalid name' % name)
AttributeError: invalid_name is invalid name
```

때때로 파이썬 코드로 범용적인 기능을 구현할 때 속성이 있는지를 확인할 때는 hasattr 내장 함수를 사용하여 확인할 수가 있다.
```py
print('foo exsit', hasattr(db, 'foo'))

>>>
foo exsit True
```

hasattr를 호출할 경우 \_\_getattr\_\_는 한 번만 호출되는 반면, \_\_getattribute\_\_는 hasattr이나 getattr를 호출할 때마다 호출된다. <br>
지연 방식으로 데이터를 기록하는 것은 \_\_setattr\_\_ 특수 메서드로 가능하다.
```py
class SavingDB(object):
    def __setattr__(self, key, value):
        print('Called __setattr__(%s %r)' %(key, value))
        super().__setattr__(key, value)

db = SavingDB()
print('Before:', db.__dict__)
db.foo = 5
print('After:', db.__dict__)
db.foo = 7
print('Finally:', db.__dict__)

>>>
Before: {}
Called __setattr__(foo 5)
After: {'foo': 5}
Called __setattr__(foo 7)
Finally: {'foo': 7}
```

\_\_setattr\_\_는 \_\_getattribute\_\_와 마찬가지로 속성에 접근해야 할 때마다 호출된다는 문제점이 있다. <br>
속성에 접근할 때 연관 딕셔너리에서 키를 찾는 상황에서는 이런 동작이 문제가 된다.
```py
class BrokenDictionaryDB(object):
    def __init__(self):
        self._data = {}

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return self._data[name]

db = BrokenDictionaryDB()

>>>
RecursionError: maximum recursion depth exceeded while calling a Python object
```

속성에 접근할 때마다 \_\_getattribute\_\_가 재귀 호출되어 스택이 넘치게 된다. <br>
이를 방지하기 위해서는 아래와 같은 방법으로 \_\_setattr\_\_를 \_\_getattribute\_\_ 사용해야 한다.
```py
class DictionaryDB(object):
    def __init__(self):
        self._data = {}

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')
        return data_dict[name]
```

## 정리
1. \_\_getattr\_\_, \_\_getattribute\_\_, \_\_setattr\_\_ 사용해서 속성에 지연 접근할 수 있다.
2. \_\_getattr\_\_는 존재하지 않는 속성에 접근 시 한번 호출되지만 \_\_getattribute\_\_는 속성에 접근할 때마다 호출된다.
3. \_\_setattr\_\_는 \_\_getattribute\_\_와 마찬가지로 속성 접근마다 호출된다.
4. \_\_setattr\_\_, \_\_getattribute\_\_ 내부에서 속성에 접근할 때 무한 재귀 호출이 일어난다. 이는 super()를 사용하여 해결할 수 있다.