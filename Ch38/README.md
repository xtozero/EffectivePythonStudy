# 스레드에서 데이터 경쟁을 막으려면 Lock을 사용하자

파이썬에서 GIL덕에 병렬처리시 Lock을 걸지 않아도 된다고 생각할 수 있다. <br>
하지만 실제로는 그렇지 않다. 인터럽트로 인해서 원자적이지 않은 연산은 언제든지 문제를 일으킬 수 있다. <br>
```py
from threading import Thread


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(how_many, counter):
    for _ in range(how_many):
        counter.increment(1)


def run_thread(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


how_many = 10**5
counter = Counter()
run_thread(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))

>>>
Counter should be 500000, found 283223
```

예상했던 결과와 다르다. <br>
파이썬 인터프리터는 모든 스레드가 동등한 처리 시간 동안 실행하게 하려고 한다.<br>
공평성을 유지하기 위해서 파이썬 인터프리터는 실행 중인 스레드를 중지하고 다른 스레드를 재개한다.<br>
따라서 원자적이지 않은 연산은 문제를 일으킬 수 있다. <br>
self.count += offset 은 하나의 연산으로 보이지만 사실 아래와 같은 단계를 거치는 분리된 연산이다.
1. self.count에 저장된 값을 불러온다.
2. self.count + offset을 계산한다.
3. self.count에 계산 결과를 저장한다.

따라서 1 ~ 3의 과정중에 인터럽트가 걸린다면 연산이 정상적으로 수행되지 않는다. 이런 현상을 data race라고 한다. <br>
data race를 방지하려면 다음과 같이 Lock을 걸어 연산도중 인터럽트가 걸리지 않도록 해야한다.
```py
class LockCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

how_many = 10**5
counter = LockCounter()
run_thread(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))

>>>
Counter should be 500000, found 500000
```

결과가 정확하게 나오는 것을 확인 할 수 있다.

## 정리
1. 파이썬 GIL가 data race를 막아주진 못한다.
2. data race를 방지하기 위해서는 Lock을 사용해야 한다.