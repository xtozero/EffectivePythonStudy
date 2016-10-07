# 스레드를 블로킹 I/O용으로 사용하고 병렬화용으로는 사용하지 말자

표준 파이썬은 C언어로 구현되어 있어 CPython이라 한다. <br>
CPython은 프로그램을 두 단계로 나눠서 실행한다. <br>
1. 소스를 바이트 코드로 컴파일한다.
2. 스택 기반 인터프리터로 바이트 코드를 실행한다.

인터프리터는 파이썬이 실행되는 동안 일관성 있는 상태를 유지하기 위해서 GIL( Global Interpreter Lock )을 사용한다. <br>
GIL는 상호 배제 잠금(mutex)이고 CPython이 선점형 멀티스레딩으로 인해서 다른 스레드에 프로그램의 제어를 뺏기는 것을 막아준다. <br>
인터럽트가 예상치 못한 시간에 발생하면 인터프리터의 상태가 망가지기 때문에 이런 인터럽트를 막아 프로그램이 올바르게 동작하도록 한다. <br>

다만 GIL는 한가지 문제가 있는데 한 번에 한 스레드만 실행될 수 있으므로 스레드가 병렬적으로 실행되지 못한다. <br>
예를 들어 다음과 같이 인수 분해를 멀티스레드를 이용해서 수행한다고 하자.
```py
from threading import Thread
from time import time


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

>>>
Took 1.099 seconds
```

실행 결과 __1.099__ 초가 걸렸다. 반면 스레드를 사용하지 않으면 __1.088__ 가 걸렸다. <br>
GIL이 성능에 미치는 영향을 엿볼 수 있다. 파이썬에서는 쓰레드를 아래 같은 경우에 사용해야 한다.
1. 스레드를 사용하면 마치 함수를 병렬로 실행하는 것처럼 해주는 일을 파이썬에게 위임할 수 있다.
2. 블로킹 I/O를 처리할 때 유용하다.
아래와 같은 시스템 호출 함수가 있다고 하면 함수를 호출할 때마다 시간이 선형으로 증가하는 것을 볼 수 있다.
```py
def slow_systemcall():
    select.select([socket(AF_INET, SOCK_STREAM)], [], [], 0.1)


start = time()
for _ in range(5):
    slow_systemcall()
end = time()

print('Took %.3f seconds' % (end - start))

>>>
Took 0.504 seconds
```

slow_systemcall는 블로킹 I/O를 사용하기 때문에 함수 실행 동안 프로그램이 멈추게 된다. 이럴 때 스레드를 사용할 수 있다.
```py
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

>>>
Took 0.101 seconds
```

스레드를 사용했을 때 실행 시간이 짧아지는 것을 볼 수 있다. <br>
파이썬에서 시스템 호출은 스레드를 통해서 모두 병렬로 실행될 수 있다. <br>
이는 파이썬 스레드가 시스템 호출을 만들기 전에 GIL를 풀고 시스템 호출이 끝나면 다시 GIL를 얻기 때문이다. <br>
스레드 외에도 내장 모듈 asyncio처럼 블로킹 I/O를 다루는 다양한 수단이 있고 이점도 있지만 이런 수단을 선택하면 해당 수단에 맞춰 코드를 작성해야 한다. <br>
따라서 가장 간단하게 블로킹 I/O를 실행하는 데는 스레드가 매우 효과적이다.

## 정리
1. 파이썬은 GIL로 인해서 병렬적으로 스레드를 실행할 수 없다.
2. 스레드는 여러 작업을 동시에 하는 것처럼 보여주기 쉽게 해준다.
3. 여러 시스템 호출을 수행할 때는 스레드가 효과적이다.