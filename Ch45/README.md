# 지역 시간은 time이 아닌 datetime으로 표현하자

시간대에 의존하지 않는 표준 시간 표현은 UTC이다. <br>
UTC는 유닉스 기원 이후로 지나간 초로 시간을 표현하는 컴퓨터에서 잘 작동한다. <br>
하지만 실제로 사람이 사용하는 시간은 지역에 따라 제각각이기 때문에 UTC 시간을 기준으로 변환해야 한다. <br>
파이썬은 두 가지 시간대 변환 방법을 제공하는데 내장모듈 time과 내장모듈 datetime을 사용하는 방법이다. <br>
time은 치명적인 오류가 발생할 가능성이 크기 때문에 datetime을 사용해서 시간을 나타내야 한다. <br>

datetime에 대해서 알아보기 전에 time을 사용하는 방식을 살펴보면 다음과 같다.
```py
from time import localtime, strftime

now = 1407694710
local_tuple = localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'
time_str = strftime(time_format, local_tuple)
print(time_str)

>>>
2014-08-11 03:18:30
```

time의 localtime 함수는 유닉스 타임스탬프를 호스트 컴퓨터의 시간대와 일치하는 지역 시간으로 변환한다. <br>
때로는 이와 반대로 지역 시간을 UTC 시간으로 변환해야 하는 경우도 있다. 이럴 때는 strptime 함수로 시간 문자열을 파싱하여 mktime으로 지역 시간을 유닉스 타미스탬프로 변환할 수 있다.
```py
from time import mktime, strptime

time_tuple = strptime(time_str, time_format)
utc_now = mktime(time_tuple)
print(utc_now)

>>>
1407694710.0
```

그렇다면 지역 시간을 다른 시간대의 지역 시간으로 변환하려면 어떻게 해야 할까? <br>
time, localtime, strptime 함수의 반환 값을 직접 조작해서 시간대를 변경하는 건 좋지 않은 생각이다. <br>
시간대를 변경하는 규칙은 매우 복잡하다. <br>
많은 운영체제는 시간대 변경을 자동으로 관리하는 설정 파일을 갖추고 있지만 이런 파일을 이용하는 time 모듈은 플랫폼에 의존적이기 때문에 신뢰하기 어렵다. <br>
time 모듈은 UTC와 호스트 컴퓨터의 지역 시간을 변환하는 목적으로만 사용해야 한다.

파이썬에서 시간을 표현하는 두 번째 방법은 내장 모듈 datetime의 datetime 클래스를 사용하는 것이다.
```py
from datetime import datetime, timezone

now = datetime(2016, 10, 30, 21, 5, 30)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print(now_local)

>>>
2016-10-31 06:05:30+09:00
```

datetime 모듈도 지역 시간을 UTC의 유닉스 타임스탬프로 쉽게 변경할 수 있다.
```py
time_str = '2016-10-30 21:05:30'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = mktime(time_tuple)
print(utc_now)

>>>
1477829130.0
```

datetime은 time과 달리 다른 지역 시간으로 신뢰성 있는 변경을 제공한다. <br>
하지만 tzinfo 클래스와 관련 메서드를 이용한 시간대 변환 기능만 제공하여 UTC 이외의 시간대 정의를 제외되어 있다. <br>
다행히도 모든 시간대에 대한 정의를 담고 있는 pytz모듈을 pip를 통해 설치해서 이를 해결할 수 있다.
```py
arrival_nyc = '2014-05-01 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(utc_dt)

pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(sf_dt)

>>>
2014-05-02 03:33:24+00:00
2014-05-01 20:33:24-07:00
```

datetime과 pytz를 이용하면 이런 변환이 호스트 컴퓨터에서 구동하는 운영체제와 상관없이 모든 환경에서 동일하게 동작한다.

## 정리
1. 서로 다른 시간대를 변화하는 데는 datetime과 pytz모듈을 사용하자
2. 항상 UTC로 시간을 표현하고 시간을 표시하기 전에 마지막으로 UTC 시간을 지역 시간으로 변환하자.