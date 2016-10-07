from threading import Thread
from time import time
from socket import *
import select


def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


start = time()
threads = []
numbers = [2139079, 1214759, 1516637, 1852285, 333213]
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
end = time()

print('Took %.3f seconds' % (end - start))

print('-' * 40)

start = time()
threads = []
numbers = [2139079, 1214759, 1516637, 1852285, 333213]
for number in numbers:
    list(factorize(number))

end = time()

print('Took %.3f seconds' % (end - start))
print('-' * 40)


def slow_systemcall():
    select.select([socket(AF_INET, SOCK_STREAM)], [], [], 0.1)


start = time()
for _ in range(5):
    slow_systemcall()
end = time()

print('Took %.3f seconds' % (end - start))

print('-' * 40)

start = time()
threads = []
for number in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time()

print('Took %.3f seconds' % (end - start))
print('-' * 40)
