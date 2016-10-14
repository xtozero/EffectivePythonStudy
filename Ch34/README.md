# 메타클래스로 클래스의 존재를 등록하자

메타클래스를 사용해서 프로그램에 있는 타입을 자동으로 등록할 수 있다. <br>
파이썬 객체를 JSON으로 직렬화한다고 해보자.
```py
import json


class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d %d)' %(self.x, self.y)

point = Point2D(5, 3)
print('Object:', point)
print('Serialized', point.serialize())

>>>
Object: Point2D(5 3)
Serialized {"args": [5, 3]}
```

JSON으로 직렬화를 하였다면 이 JSON 문자열을 역직렬화해서 JSON이 표현하는 Point2D 객체를 생성할 수도 있을 것이다.
```py
class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


class Point2D(Deserializable):
    # 이하 생략

point = Point2D(5, 3)
print('Before:', point)
data = point.serialize()
print('Serialized', data)
after = Point2D.deserialize(data)
print('After', after)

>>>
Before: Point2D(5 3)
Serialized {"args": [5, 3]}
After Point2D(5 3)
```

위의 예제는 직렬화된 데이터에 대응하는 타입을 미리 알고 있을 때만 동작한다는 점이다. <br>
이상적으로는 JSON으로 직렬화되는 클래스를 많이 갖추고 그중 어떤 클래스든 대응하는 파이썬객체로 역직렬화하는 공통함수를 하나만 두려고 할 것이다. <br>
이렇게 만들려면 직렬화 데이터에 클래스 이름을 포함하면 된다.
```py
class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args
        })

registry = {}


def register_class(target_class):
    registry[target_class.__name__] = target_class


def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])
```

문제는 deserialize가 제대로 동작하기 위해서 register_class를 모든 클래스마다 호출해 주어야 한다는 점이다. <br>
이런 누락을 해소하기 위해서 메타클래스를 사용할 수 있다. <br>
```py
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls


class Serializable(object, metaclass=Meta):
    # 이하 생략


class Point2D(Serializable):
    # 이하 생략

point = Point2D(5, 3)
print('Before:', point)
data = point.serialize()
print('Serialized', data)
after = deserialize(data)
print('After', after)

>>>
Before: Point2D(5 3)
Serialized {"class": "Point2D", "args": [5, 3]}
After Point2D(5 3)
```

## 정리
1. 메타클래스를 이용하면 기반클래스로 서브 클래스를 만들 때마다 자동으로 등록 코드를 실행할 수 있다.
2. 메타클래스를 사용해서 클래스를 등록하면 누락을 방지할 수 있다.