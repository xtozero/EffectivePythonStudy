from collections import deque
from threading import Lock
from threading import Thread
from time import sleep
from queue import Queue


def download(item):
    # print('download')
    pass


def resize(item):
    # print('resize')
    pass


def upload(item):
    # print('upload')
    pass


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

# 아이템이 모두 처리되기를 대기
while len(done_queue.items) < 1000:
    pass

print('Done')

print('-' * 40)

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print('Processed', processed, 'items after polling', polled, 'times')

print('-' * 40)

queue = Queue()


def consumer():
    print('Consumer waiting')
    queue.get()
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()

print('Producer putting')
queue.put(object())
thread.join()
print('Producer done')

print('-' * 40)

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

print('-' * 40)

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

print('-' * 40)


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
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

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