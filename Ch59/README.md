# tracemalloc으로 메모리 사용 현황과 누수를 파악하자

파이썬 표준 구현체 CPython은 참조 카운팅으로 메모리를 관리한다. <br>
참조 카운팅은 객체의 참조가 모두 해제되면 참조된 객체 역시 해제됨을 보장한다 <br>
파이썬은 자기 참조 객체가 가비지 컬렉션되는 것을 보장하는 Cycle detector도 갖추고 있어 이론적으로 프로그래머가 메모리 할당과 해제를 걱정하지 않아도 된다 <br>
하지만 실제로 프로그램이 메모리 부족에 처하는 경우가 있다. 이런 경우 다음과 같은 방식으로 누수를 찾아볼 수 있다. <br>

첫 번째 방법은 내장 모듈 gc에 요청하여 가비지 컬렉터의 모든 객체를 나열하는 것이다.
```py
import gc


found_objects = gc.get_objects()
print('%d objects before' % len(found_objects))

x = [1, 2, 3, 4, 5, 6]
found_objects = gc.get_objects()
print('%d objects after' % len(found_objects))
for obj in found_objects[:3]:
    print(repr(obj)[:100])

>>>
7034 objects before
7036 objects after
('builtins', 'ImportWarning')
('exceptions', 'ImportWarning')
('builtins', 'IndentationError')
```

파이썬 3.4부터는 내장 모듈 tracemalloc으로 객체가 어떻게 할당되었는지 정보를 파악할 수 있다.
```py
tracemalloc.start(10)

time1 = tracemalloc.take_snapshot()
x = [1, 2, 3, 4, 5, 6]
time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'lineno')
for stat in stats[:3]:
    print(stat)

>>>
C:\Users\xtozero\AppData\Local\Programs\Python\Python35-32\lib\tracemalloc.py:349: size=48 B (+48 B), count=2 (+2), average=24 B
C:\Users\xtozero\AppData\Local\Programs\Python\Python35-32\lib\tracemalloc.py:487: size=32 B (+32 B), count=1 (+1), average=32 B
C:/Users/xtozero/Documents/GitHub/EffectivePythonStudy/Ch59/SampleCode/Ch59.py:20: size=24 B (+24 B), count=1 (+1), average=24 B
```

어떤 객체들이 프로그램 메모리 사용량을 주로 차지하고 소스 코드의 어느 부분에서 할당되는지를 파악할 수 있다. <br>
tracemalloc은 각 할당의 전체 스택 트레이스도 출력할 수 있다. 다음 코드에서 메모리 사용량이 가장 큰 부분의 스택 트레이스를 출력하는 코드를 확인할 수 있다.
```py
print('-' * 40)
stats = time2.compare_to(time1, 'traceback')
top = stats[0]
print('\n'.join(top.traceback.format()))

>>>
  File "C:\Users\xtozero\AppData\Local\Programs\Python\Python35-32\lib\tracemalloc.py", line 349
    self.traces = _Traces(traces)
  File "C:\Users\xtozero\AppData\Local\Programs\Python\Python35-32\lib\tracemalloc.py", line 487
    return Snapshot(traces, traceback_limit)
  File "C:/Users/xtozero/Documents/GitHub/EffectivePythonStudy/Ch59/SampleCode/Ch59.py", line 19
    time1 = tracemalloc.take_snapshot()
```

## 정리
1. 파이썬 프로그램의 메모리 사용량을 파악하는데 내장 모듈 tracemalloc이 도움이 된다.
2. tracemalloc은 파이썬 3.4 이후로만 지원된다.