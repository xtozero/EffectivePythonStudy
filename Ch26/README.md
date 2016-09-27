# 믹스인 유틸리티 클래스에만 다중 상속을 사용하자

파이썬은 다중 상속 시 발생하는 초기화 문제를 해결해 주는 super함수를 가지고 있다. [(Ch25 참고)](../Ch25) <br>
하지만 다중 상속은 믹스인에만 적용하는 것이 좋다.

> 믹스인이란 클래스에서 제공해야 하는 추가적인 메서드만 정의하는 작은 클래스를 의미한다.

다음 예제와 같은 클래스를 믹스인이라 부른다.
```py
class ToDicMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDicMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value
```

이제 이런 믹스인을 통해서 새로운 클래스가 제공해야 하는 메서드를 제공할 수 있다.
```py
class BinaryTree(ToDicMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10,
                  left=BinaryTree(7, right=BinaryTree(9)),
                  right=BinaryTree(13, left=BinaryTree(11)))
print(tree.to_dict())

>>>
{'right': {'right': None, 'left': {'right': None, 'left': None, 'value': 11}, 'value': 13}, 'left': {'right': {'right': None, 'left': None, 'value': 9}, 'left': None, 'value': 7}, 'value': 10}
```

믹스인은 범용 기능을 각 클래스에서 특수화하는 것도 가능하게 해준다.
```py
class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left, right)
        self.parent = parent

    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent)) and key == 'parent':
            return value.value
        else:
            return super()._traverse(key, value)

tree = BinaryTreeWithParent(10)
tree.left = BinaryTreeWithParent(7, parent=tree)
tree.right = BinaryTreeWithParent(13, parent=tree)

print(tree.to_dict())

>>>
{'parent': None, 'right': {'parent': 10, 'right': None, 'left': None, 'value': 13}, 'left': {'parent': 10, 'right': None, 'left': None, 'value': 7}, 'value': 10}
```

이제 본론으로 들어가서 믹스인을 다중 상속받아 조합시켜 보자 아래와 같은 JSON 믹스인이 있다.
```
class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())
```

JsonMixin은 클래스가 to_dict() 메서드와 키워드 인수를 받는 \_\_init\_\_메서드를 요구하고 있다. <br>
해당 요구사항에 맞춰 믹스인 클래스를 조합하여 아래와 같이 사용할 수 있다.
```py
class MixinExample(ToDicMixin, JsonMixin):
    def __init__(self, keyword1=None, keyword2=None):
        self.keyword1 = keyword1
        self.keyword2 = keyword2


serialized = '''{
    "keyword1": 1,
    "keyword2": 2
}'''

deserialized = MixinExample.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)

>>>
```
이렇게 믹스인 클래스를 사용하면 상속한 객체에서 이미 믹스인을 상속하고 있어도 새로 정의한 클래스는 정상적으로 동작한다.

## 정리
1. 클래스를 다중상속하는 것은 지양하자
2. 믹스인은 상속받은 클래스에서 동작을 변경하는 것이 가능하다.
3. 믹스인을 조합하여 기능을 확장할 수 있다.