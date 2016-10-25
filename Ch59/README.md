# tracemalloc으로 메모리 사용 현황과 누수를 파악하자

파이썬 표준 구현체 CPython은 참조 카운팅으로 메모리를 관리한다. <br>
참조 카운팅은 객체의 참조가 모두 해제되면 참조된 객체 역시 해제됨을 보장한다 <br>
파이썬은 자기 참조 객체가 가비지 컬렉션되는 것을 보장하는 Cycle detector도 갖추고 있어 이론적으로 프로그래머가 메모리 할당과 해제를 걱정하지 않아도 된다 <br>
하지만 실제로 프로그램이 메모리 부족에 처하는 경우가 있다. 이런 경우 다음과 같은 방식으로 누수를 찾아 볼 수 있다. <br>

첫번째 방법은 내장 모듈 gc에 요청하여 가비지 컬렉터의 모든 객체를 나열하는 것이다.
```py
import gc
found_objects = gc.get_objects()
print('%d objects before' % len(found_objects))

x = [1, 2, 3, 4, 5, 6]
found_objects = gc.get_objects()
print('%d objects after' % len(found_objects))
for obj in found_objects[:3]:
    print(repr(obj)[:100])
```