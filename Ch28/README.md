# 커스텀 컨테이너 타입은 collections.abc의 클래스를 상속받게 만들자

모든 파이썬 클래스는 일종의 컨테이너이다. <br>
시퀀스처럼 쓰임새가 간단한 클래스를 설계한다면 파이썬 내장 타입인 list을 상속받아 클래스를 작성할 수 있다.
```py
class FrequencyList(list):
    def __init__(self, numbers):
        super().__init__(numbers)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts

foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('Length is', len(foo))
foo.pop()
print('After pop:', repr(foo))
print('Frequency', foo.frequency())

>>>
Length is 7
After pop: ['a', 'b', 'a', 'c', 'b', 'a']
Frequency {'b': 2, 'a': 3, 'c': 1}
```

list를 상속받았기 때문에 list의 표준 기능을 모두 갖췄으며 필요한 동작을 추가할 수도 있다. <br>
만약 list의 서브 클래스는 아니지만, 인덱스로 접근할 수 있게 해서 list와 같이 동작하는 객체를 제공하고 싶다면 아래와 같이 코드를 작성할 수 있다.
```py
class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class IndexableNode(BinaryNode):
    def _search(self, count, item):
        found = None
        if self.left:
            found, count = self.left._search(count, item)
        if found is None and count == item:
            found = self
        else:
            count += 1
        if found is None and self.right:
            found, count = self.right._search(count, item)
        return found, count

    def __getitem__(self, item):
        found, _ = self._search(0, item)
        if not found:
            raise IndexError('Index out of range')
        return found.value

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(6, right=IndexableNode(7))),
    right=IndexableNode(
        15, left=IndexableNode(11)))

print('LRR=', tree.left.right.right.value)
print('Index 0 =', tree[0])
print('Index 1 =', tree[1])
print('11 in the three?', 11 in tree)
print('17 in the three?', 17in tree)
print('Tree is', list(tree))
```

트리를 시퀀스 처럼 접근할 수 있고 탐색은 물론 list로도 만들 수도 있다. <br>
하지만 문제가 있는데 \_\_getitem\_\_ 함수만 제공하는 것만으로는 시퀀스의 모든 기능을 제공하지 못한다. <br>
내장 함수 len 을 지원하기 위해서는 특수 메서드 \_\_len\_\_를 제공해야 하며 시퀀스의 총 원소 갯수를 세는 count 메서드도 없다. <br>
시퀀스 처럼 동작하려면 어떤 메서드를 제공해야 하는지 파악하기 어려우므로 파이썬에서는 collection.abc를 통해서 제공해야 할 메서드들을 빼먹지 않도록 해준다.
```py
class BadType(Sequence):
    pass

foo = BadType()

>>>
Traceback (most recent call last):
    foo = BadType()
TypeError: Can't instantiate abstract class BadType with abstract methods __getitem__, __len__
```

## 정리
1. 쓰임새가 간단할 때는 list, map과 같은 내장 컨테이너 타입을 직접 상속받자.
2. 커스텀 컨테이너를 올바르게 작성하기 위해서 collections.abc에서 제공하는 인터페이스를 상속받도록 하자.