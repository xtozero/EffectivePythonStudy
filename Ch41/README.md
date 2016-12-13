# 진정한 병렬성을 실현하려면 concurrent.future를 고려하자

파이썬 표준은 GIL로 스레드가 병렬적으로 실행되는 것을 막는다. <br>
따라서 성능이 중요하다면 일반적으로는 중요 부분을 C언어 확장 모듈로 재작성할 수 있지만, C로 코드를 재작성 하는데는 상당한 비용이 든다 <br>
파이썬에서는 간단한 코드가 C언어에서는 매우 복잡해진다. <br>
C언어 확장 모듈을 작성하는 것은 물론 가치가 있고 Cython이나 Numba와 같은 변환작업을 도와주는 오픈 소스 도구도 있지만 모든 경우를 해결해 주지 않는다. <br>

파이썬에 집중하여 성능을 높이기 위해서는 concurrent.future를 사용하는 방법이 있다. <br>
이 모듈을 사용하면 파이썬에서 자식 프로세스로 추가적인 인터프리터를 실행하여 병렬로 CPU 코어를 활용할 수 있다. <br>
멀티 스레드가 아니라 멀티 프로세스이다. 이런 자식 프로세스는 주 인터프리터와는 별개이므로 전역 인터프리터 잠금도 분리되는 효과를 가진다. <br>

하나의 예로 최대 공약수를 아래와 같은 함수로 찾는다고 해보자.
```py
from time import time


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

numbers = [(1963309, 2265973), (2030677, 3814172), (1551645, 2229620), (2039045, 2020802)]
start = time()
result = list(map(gcd, numbers))
end = time()
print('Took %.3f seconds' % (end - start))

>>>
Took 1.507 seconds
```

병렬성이 없으므로 함수를 실행하면 시간이 선형적으로 증가한다. <br>
이번에는 concurrent.future 모듈의 ThreadPoolExcutor 클래스를 사용해보자
```py
start = time()
pool = ThreadPoolExecutor(max_workers=2)
result = list(pool.map(gcd, numbers))
end = time()
print('Took %.3f seconds' % (end - start))

>>>
Took 1.749 seconds
```

오히려 느려지는 것을 볼 수 있는데 이는 스레드 풀을 시작하고 통신하는데 드는 오버헤드 때문이다. <br>
여기서 코드 한줄을 수정하면 마법과 같이 빨라지는 것을 확인할 수 있다. <br>
```py
if __name__ == "__main__":
    start = time()
    pool = ProcessPoolExecutor(max_workers=2)
    result = list(pool.map(gcd, numbers))
    end = time()
    print('Took %.3f seconds' % (end - start))

>>>
Took 0.939 seconds
```

ProcessPoolExecutor 클래스는 사용법은 간단하지만, 아래와 같은 작업을 실제로 수행한다.

1. 입력 데이터에서 map으로 각 아이템을 가져온다.
2. pickle 모듈을 사용하여 바이너리 데이터로 직렬화한다 [(Ch44 참고)](../Ch44)
3. 주 인터프리터 프로세스에서 직렬화한 데이터를 지역 소켓을 통해 자식 인터프리터 프로세스로 복사한다.
4. 자식 인터프리터에서는 pickle을 사용해서 데이터를 파이썬 객체로 역직렬화한다.
5. gcd 함수가 들어 있는 파이썬 모듈을 임포트한다.
6. 다른 자식 프로세스를 사용하여 병렬로 입력 데이터를 처리한다.
7. 결과를 다시 바이트로 직렬화한다.
8. 소켓을 통해 바이트를 다시 복사한다.
9. 바이트를 부모 프로세스에 있는 파이썬 객체로 역직렬화한다.
10. 여러 자식에 있는 결과를 하나의 결과로 합친다.

이 방법은 고립되어 다른 프로그램과 상태를 공유할 필요가 없고 데이터를 조금만 전송해도 많은 양의 계산이 일어나는 지렛대 효과가 큰 경우에 적합하다. <br>
계산이 그런 특성이 있지 않다면 multiprocessing의 비용이 병렬성을 통한 속도 향상보다 커서 성능 향상이 미비할 수 있다. <br>
multiprocessing은 이런 상황에서 쓸 수 있는 공유 메모리, 프로세스 간 잠금, 큐, 프록시 같은 고급 기능을 제공하지만 너무 복잡하므로 우선은 concurrent.future모듈을 시험해보고 모든 옵션이 바닥났을 때 multiprocessing모듈을 직접 사용하는 것이 좋다.

## 정리
1. CPU 병목점을 C언어로 옮기는 것은 성능을 개선할 수 있는 효과적인 방법이지만 복잡하고 테스트 해야 할 양도 늘어난다.
2. multiprocessing 모듈은 파이썬에서 특정 유형의 계산을 최소한의 노력으로 병렬화할 수 있는 도구를 제공한다.
3. multiprocessing의 기능은 concurrent.future와 그 안에 들어 있는 간단한 ProcessPoolExecutor 클래스로 접근하는 것이 좋다.
4. multiprocessing의 고급 기능은 너무 복잡하므로 피하는 것이 좋다.

