# 스레드 간의 작업을 조율하려면 Queue를 사용하자

파이프라인은 유용한 병행 작업 방식 중 하나이다. <br>
파이프라인은 일렬로 이어진 단계들로 구성되며, 각 단계에는 특정 함수가 연결되어 있다. <br>
새 작업 요소는 파이프라인의 앞쪽에 추가되며 각 함수는 자신이 속한 단계에 배정된 작업 요소를 처리할 수 있다. <br>
파이프라인 속의 작업은 남겨진 단계가 더는 없을 때까지 처리를 완료할 때마다 다음 단계로 이동한다.

디지털카메라에서 이미지들을 가져와 리사이즈 하고 온라인 포토 갤러리에 추가하는 시스템을 구축한다고 하면 일련의 작업을 3단계로 나눌 수 있다. <br>
1. 새 이미지를 추출
2. 리사이즈 함수로 이미지를 처리
3. 업로드 함수로 이미지를 업로드

이 세 단계를 실행하는 함수 download, resize, upload를 이미 작성했다고 하면 파이프라인을 어떻게 조립할 수 있을까? <br>
가장 먼저 파이프라인 단계 사이에서 작업을 전달하는 방법이다. 이 방법은 스레드 안전 생산자 소비자 큐로 모델링 할 수 있다. <br>
```py
from collections import deque
from threading import Lock


class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    # 새 이미지를 대기 아이템 리스트의 끝에 추가할 수 있다.
    def put(self, item):
        with self.lock:
            self.items.append(item)

    # 처리할 이미지를 대기 아이템 리스트의 앞에서 가져올 수 있다.
    def get(self):
        with self.lock:
            return self.items.popleft()
```

이제 이러한 큐에서 작업을 꺼내와서 함수를 실행한 후 결과를 또 다른 큐에 넣는 파이썬 스레드로 파이프라인의 각 단계를 표현하자.
```py
from collections import deque
from time import sleep

class Woker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)  # 처리할 아이템이 없음
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1
```

이제 작업 조율용 큐와 그에 해당하는 작업 스레드를 생성해서 세 단계를 연결하면 파이프라인이 완성된다.
```py
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Woker(download, download_queue, resize_queue),
    Woker(resize, resize_queue, upload_queue),
    Woker(upload, upload_queue, done_queue)
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())


while len(done_queue.items) < 1000:
    pass

print('Done')
```

이 코드는 잘 동작하지만, 입력 큐에서 새 작업을 가져오는 스레드가 IndexError 예외를 잡는 경우가 많이 실행된다.
```py
processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print('Processed', processed, 'items after polling', polled, 'times')

>>>
Processed 1000 items after polling 3034 times
```

결국 CPU시간을 낭비한다. 그리고 이외에도 피해야 할 문제가 더 있다.
1. 입력 작업을 모두 완료했는지 알기 위해서 done_queue에 결과가 모두 쌓일 때까지 기다려야 한다.
2. Worker의 Run 메서드가 계속 실행된다.
3. 파이프라인이 정체되면 큐가 계속 증가하여 프로그램이 망가질 수 있다.

내장 모듈 queue에 들어있는 Queue 클래스를 사용하면 이런 문제를 해결할 수 있다.
Queue는 새 데이터가 생길 때까지 get 메서드가 블록되게 하여 작업 스레드가 계속 데이터가 있는지 체크하는 상황을 없애준다.
```py
def consumer():
    print('Consumer waiting')
    queue.get()
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()

>>>
Consumer waiting
```

다음과 같이 큐에 아이템을 제공해 줘야지 블록이 해제된다.
```py
print('Producer putting')
queue.put(object())
thread.join()
print('Producer done')
```

파이프라인 정체로 인한 큐의 증가를 막으려면 대기할 작업의 최대 개수를 Queue에 지정해야 한다. <br>
큐가 이미 이 크기만큼 가득 차 있으면 put호출이 블록된다.
```py
queue = Queue(1)


def consumer():
    sleep(0.1)
    queue.get()
    print('Consumer get 1')
    queue.get()
    print('Consumer get 2')

thread = Thread(target=consumer)
thread.start()

queue.put(object)
print('Producer put 1')
queue.put(object)
print('Producer put 2')
thread.join()
print('Producer done')

>>>
Producer put 1
Consumer get 1
Producer put 2
Consumer get 2
Producer done
```

또한 Queue 클래스는 task_down 메서드로 작업 진행을 추적할 수도 있다. <br>
작업 진행을 추적하면 특정 단계의 입력 큐가 빌 때까지 기다릴 수 있으므로 파이프라인의 끝에서 done_queue를 폴링하지 않아도 된다.
```py
in_queue = Queue()


def consumer():
    print('Consumer waiting')
    work = in_queue.get()
    print('Consumer working')
    in_queue.task_done()


Thread(target=consumer).start()

in_queue.put(object())
print('Producer waiting')
in_queue.join()
print('Producer done')
```

Queue 인스턴스의 join은 큐가 비더라도 큐에 추가된 모든 아이템에 task_done을 호출할 때까지 완료되지 않는다.
이제 마지막으로 Queue 클래스를 통해서 처음의 파이프라인을 고쳐보자
```py
class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                # SENTINEL 변수를 만나면 이터레이션을 중단하고 스레드를 종료되게 한다.
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()


class StoppableWoker(Thread):
    def __init__(self, func, in_queue, out_queue):
        # 이전 버전과 동일하여 생략

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWoker(download, download_queue, resize_queue),
    StoppableWoker(resize, resize_queue, upload_queue),
    StoppableWoker(upload, upload_queue, done_queue)
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())
download_queue.close()
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'items finished')

>>>
1000 items finished
```
모든 작업이 정상적으로 처리된 것을 확인할 수 있다.

## 정리
1. 파이프라인을 구축할 때 많은 문제가 발생할 수 있다는 점을 주의하자
2. Queue 클래스는 연산 블로킹, 버퍼 크기, 조인 등 견고한 파이프라인을 만드는 데 필요한 기능을 모두 갖추었다.