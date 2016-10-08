from threading import Thread
from threading import Lock


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

print('-' * 40)


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

print('-' * 40)
