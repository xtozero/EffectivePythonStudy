# 속성을 리팩토링하는 대신 @property를 고려하자

[Ch29](../Ch29)에서 @property 데코레이터에 대해서 알게 되었다. <br>
@property로 흔히 사용하는 사용법 중에 단순 숫자 속성을 즉석에서 계산하는 방식이 있다 <br>
이런 방식은 호출하는 쪽을 변경하지 않고도 기존에 클래스를 사용한 곳이 새로운 동작을 하게 해주므로 매우 유용하게 쓰일 수 있다. <br>

아래와 같이 구멍 난 양동이를 파이썬 객체로 표현했다고 해보자.
```py
from datetime import timedelta
from datetime import datetime


class Bucket(object):
    def __init__(self, period):
        self.period_data = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Buket(quota=%d)' % self.quota
```

그리고 양동이를 채우고 비우는 함수를 다음과 같이 정의했다고 하자.
```py
def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_data:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_data:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True
```

이 클래스는 아래와 같은 방식으로 사용할 수 있다.
```py
bucket = Bucket(60)
fill(bucket, 100)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)

>>>
Had 99 quota
Buket(quota=1)
Not enough for 3 quota
Buket(quota=1)
```

이 클래스에서 양동이가 얼마나 채워진 상태로 시작하는지를 모르는데 deduct를 호출한 곳에서 중단된 이유를 알 수 없다는 문제점이 있다. <br>
이럴 때는 호출 부를 수정하지 않아도 @property를 통해서 속성의 변경을 추적하도록 할 수 있다.
```py
class Bucket(object):
    def __init__(self, period):
        self.period_data = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return 'Buket(max_quota=%d, quota_consume=%d)' % (self.max_quota, self.quota_consumed)

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta
```

같은 호출 코드에서 아래와 같이 값이 추적되는 것을 확인할 수 있다.
```py
>>>
Had 99 quota
Buket(max_quota=100, quota_consume=99)
Not enough for 3 quota
Buket(max_quota=100, quota_consume=99)
```

@property를 이런 방식으로 사용하면 Bucket.quota를 사용하는 코드를 변경하거나 Bucket 클래스가 변경된 사실을 몰라도 정상적으로 동작한다는 점이다. <br>
하지만 @property를 과용하지는 말아야 한다. @property 메서드를 계속 확장하고 있다면 클래스를 새롭게 리팩토링할 시점이 된 것이다.

## 정리
1. 기존 인스턴스 속성에 새 기능을 부여하려면 @property를 사용하자
2. @property를 사용하면 좀 더 나은 데이터 모델로 발전할 수 있다.
3. @property의 사용이 증가한다면 클래스와 이를 호출하는 모든 곳을 리팩토링하는 방안을 고려하자