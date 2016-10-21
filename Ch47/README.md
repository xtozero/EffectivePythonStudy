# 정밀도가 중요할 때는 decimal을 사용하자

파이썬은 숫자 데이터를 다루는 데 적합한 언어다. <br>
파이썬의 정수 타입은 현실적인 크기의 값을 모두 표현할 수 있다. <br>
다만 모든 상황을 충족하지 못하는 경우가 있다. 아래와 같이 부동 소수점의 결과가 너무 작아서 반올림하면 0이 되는 경우가 있다.
```py
rate = 0.05
seconds = 5
cost = rate * seconds / 60
print(round(cost, 2))

>>>
0.0
```

이런 경우에는 내장 모듈 decimal의 Decimal 클래스를 사용할 수 있다. <br>
Decimal 클래스는 기본적으로 소수점이 28자리인 고정 소수점 연산을 제공하며 필요하다면 자릿수를 늘릴 수 있다. <br>
Decimal 클래스는 다음과 같은 연산에서 정확한 값을 제공한다.
```py
from decimal import Decimal

rate = 1.45
seconds = 222
cost = rate * seconds / 60
print(cost)

rate = Decimal('1.45')
seconds = Decimal('222')
cost = rate * seconds / Decimal('60')
print(cost)

>>>
5.364999999999999
5.365
```

또한 Decimal 클래스는 원하는 반올림 동작에 따라 필요한 소수점 위치로 정확하게 반올림하는 내장 함수를 지원한다.
```py
from decimal import ROUND_UP

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)
>>>

5.37
```

Decimal이 고정 소수점의 수에도 잘 동작하지만 1/3은 근삿값으로 계산되는 등 아직도 정확도 면에서는 제약이 있다. <br>
정확도 제한이 없는 유리수를 표현하려면 내장모듈 fractions의 Fraction 클래스를 사용해야 한다.

## 정리
1. 정밀도가 중요할 때는 Decimal 클래스를 사용하자.
2. 정확도 제한이 없는 유리수를 표현하려면 Fraction 클래스를 사용하자.
