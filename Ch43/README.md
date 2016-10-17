# 재사용 가능한 try/finally 동작을 만드려면 contextlib와 with 문을 고려하자

파이썬에서는 with 문을 통해서 코드를 특별한 컨텍스트에서 실행할 수 있다. <br>
with 문을 사용하면 try/finally 구문을 반복하여 사용할 필요가 없어진다. <br>
```py
from threading import Lock

lock = Lock()
lock.acquire()
try:
    print('Critical Section')
finally:
    lock.release()
    
# 아래의 코드는 완전히 동일하게 동작한다.

lock = Lock()
with lock:
    print('Critical Section')

```

내장모듈 contextlib를 사용하면 객체와 함수를 with 문에서 사용할 수 있게 만들 수 있다. <br>
이 모듈에는 간단한 함수를 with 문에 사용할 수 있도록 해주는 데코레이터 contextmanager를 포함하고 있다. <br>
이 데코레이터를 이용하는 방법이 \_\_enter\_\_ 와 \_\_exit\_\_ 특수 메서드를 담을 클래스를 정의하기 보다 쉽다. <br>
한 가지 예를 들면 아래와 같은 디버깅 로그용 함수가 있다고 하자.
```py
import logging


def logging_function():
    logging.debug('Some debug data')
    logging.error('Error log')
    logging.debug('More debug data')

logging_function()

>>>
ERROR:root:Error log
```
프로그램의 기본 로그 수준이 WARNING이기 때문에 함수는 오류 메세지만 출력한다. <br>
이함수에 컨텍스트 매니저를 정의해서 일시적으로 로그 수준을 낮추었다가 올릴 수 있다.
```py
@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        # with 블록의 내용이 실행되는 부분
        yield
    finally:
        logger.setLevel(old_level)

with debug_logging(logging.DEBUG):
    print('Inside:')
    logging_function()
print('After')
logging_function()
```

with 문에 전달되는 컨텍스트 매니저에서 객체를 반환할 수도 있다. 이 객체는 복합문 as 부분에 있는 지역 변수에 할당된다.
```py
with open('test.txt', 'w') as handle:
    handle.write('Some data')
```

위와 같은 as 구문을 지원하기 위해서는 컨텍스트 매니저의 yield 문에서 값을 넘겨주면 된다.
```py
@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug('This is my message!')
    logging.debug('This will not print')

logger = logging.getLogger('my-log')
logger.debug('This will not print')

>>>
DEBUG:my-log:This is my message!
```

logger로 전달받은 로깅 객체만 로그 레벨을 낮추었으므로 logging의 debug 메세지는 출력되지 않는다. <br>
그리고 with 문이 끝난 다음 로그 레벨이 원상태로 돌아갔으므로 debug 메세지가 출력되지 않는 것을 확인할 수 있다.

## 정리
1. with 문을 사용하면 try/finally 블록을 재사용할 수 있다.
2. 내장모듈 contextlib의 contextmanager 데코레이터를 사용해서 함수를 with 문에 사용할 수 있다.
3. 컨텍스트 매니저에서 yield한 값은 with 문의 as 부분에 할당된다.