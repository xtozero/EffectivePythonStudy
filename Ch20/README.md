# 동적 기본 인수를 지정하려면 None과 docstring을 사용하자

키보드 인수의 기본값을 비정적 타입(=동적 타입)을 사용해야 할 때가 있다.
```py
from datetime import datetime
from time import sleep


def log(message, when=datetime.now()):
    print('%s: %s' % (when, message))

log('Hi there!')
sleep(0.1)
log('Hi again!')

>>>
2016-09-21 19:56:00.401271: Hi there!
2016-09-21 19:56:00.401271: Hi again!
```

log 함수에서 when의 기본값으로 설정된 datetime.now()는 단 한 번만 평가되어 기대한 것과는 다르게 동작한다.

기대한 대로 함수가 동작하게 하려면 동적 기본 인수를 지정하지 말고 None을 기본 값으로 설정한 다음에 docstring을 작성하여 해당 내용을 남기는 것이 좋다.
```py
def log2(message, when=None):
    """
    :param message: Message to print.
    :param when: datetime of when the message occurred. Default to the present time
    :return: None
    """
    when = datetime.now() if when is None else when
    print('%s: %s' % (when, message))

log2('Hi there!')
sleep(0.1)
log2('Hi again!')
>>>
2016-09-21 20:01:26.046833: Hi there!
2016-09-21 20:01:26.146843: Hi again!
```
동적 기본 인수는 특히 기본값이 수정 가능할 때 의도와 다르게 동작할 수 있다.
```py
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also data')
bar['meep'] = 1
print('Foo: ', foo)
print('Bar: ', bar)

>>>
print('Foo: ', foo)
print('Bar: ', bar)
```

위의 예제를 보면 기본값이 공유되는 것을 볼 수 있다. log 함수 예제와 마찬가지로 기본값은 단 한 번만 평가되기 때문에 모든 함수 호출이 같은 기본 인수를 공유하기 때문이다.

이 예제도 마찬가지로 기본값을 None으로 하고 docstring을 작성하는 것으로 문제를 회피할 수 있다.
```
def decode2(data, default=None):
    ''' Load Json data from a string
    :param data: JSON data to decode
    :param default: Value to return if decoding fails Default to an empty dictionary
    :return: None
    '''
    try:
        return json.loads(data)
    except ValueError:
        return {} if default is None else default

foo = decode2('bad data')
foo['stuff'] = 5
bar = decode2('also data')
bar['meep'] = 1
print('Foo: ', foo)
print('Bar: ', bar)
```

## 정리
1. 기본 인수는 모듈 로드 시점에서 단 한 번만 평가된다. 그래서 동적 값에서는 이상하게 동작할 수 있다.
2. 동적 기본 인수를 사용해야 할 때는 None을 기본값으로 설정하고 docstring을 잘 작성하자.