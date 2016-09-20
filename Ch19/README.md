# 키워드 인수로 선택적인 동작을 제공하자

파이썬에서는 인수를 위치로 넘길 수 있을 뿐만이 아니라 키워드로 전달할 수도 있다.
```py
def remainder(number, divisor):
    return number % divisor

print(remainder(20, 7))
print(remainder(20, divisor=7))
print(remainder(number=20, divisor=7))
print(remainder(divisor=7, number=20))
>>>
6
6
6
6
```
다만 위치 인수는 반드시 키워드 인수보다 앞에 전달해야 한다.
```py
remainder(number=20, 7)

>>>
SyntaxError: positional argument follows keyword argument
```
또한, 각 인수는 한 번만 지정할 수 있다.
```py
remainder(20, number=7)

>>>
TypeError: remainder() got multiple values for argument 'number'
```
키워드 인수를 사용하면 세가지 이점을 얻을 수 있다.
1. 코드를 처음 보는 사람이 함수 호출을 더 명확하게 이해할 수 있다.
> 위의 예제의 remainder의 본문을 보지 않아도 어떤 인수가 나눗수인지 분명하게 알 수 있다.
2. 함수를 정의할 때 기본값을 설정할 수 있다.
> ```py
> def flow_rate(weight_diff, time_diff, period=1):
>    return (weight_diff / time_diff) * period
>
> weight_diff = 0.5
> time_diff = 3
> flow = flow_rate(weight_diff, time_diff)
> print('%.3f kg per second' % flow)
> 
> flow = flow_rate(weight_diff, time_diff, period=3600)
> print('%.3f kg per hour' % flow)
>
>>>>
>0.167 kg per second
>600.000 kg per hour
> ```
>위의 예제에서 period는 선택적인 인수가 되었으면 인수를 전달하지 않으면 기본값 1을 가진다. 위의 코드는 매우 간단한 예제이며 기본값이 복잡할 때는 다루기 까다롭다. [(Ch20참조)](../Ch20)

3. 기존 호출 코드와 호환성을 유지하면서도 함수의 파라미터를 확장할 수 있다.
> 2.의 코드에 새로운 인수를 추가하면 아래와 같이 기존 호출 코드의 변화 없이 함수를 확장할 수 있다.
> ```py
> def flow_rate_extend(weight_diff, time_diff, period=1, units_per_kg=1):
>     return ((weight_diff / units_per_kg) / time_diff) * period
> 
> flow = flow_rate_extend(weight_diff, time_diff)
> print('%.3f kg per second' % flow)
> 
> flow = flow_rate_extend(weight_diff, time_diff, period=3600)
> print('%.3f kg per hour' % flow)
> 
> flow = flow_rate_extend(weight_diff, time_diff, period=3600, units_per_kg=2.2)
> print('%.3f kg per hour' % flow)
>>>>
> 0.167 kg per second
> 600.000 kg per hour
> 272.727 kg per hour
>```
> 이 방식의 유일한 문제는 period, units_per_kg을 여전히 위치 인수로 넘길 수 있다는 점이다.
>```py
>flow_rate_extend(weight_diff, time_diff, 3600, 2.2)
>```
> 이 문제를 해결하는 방식은 [Ch21](../Ch21)에서 다룰 것이다.

## 정리
1. 함수의 인수를 위치뿐만이 아니라 키워드로 전달할 수 있다.
2. 키워드 인수로 호출하면 함수의 인수를 명확하게 이해할 수 있다.
3. 키워드 인수를 사용하면 기본값을 지정할 수 있다.
4. 키워드 인수를 사용하면 함수를 손쉽게 확장할 수 있다.