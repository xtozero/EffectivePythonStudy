# for와 whil 루프 뒤에는 else 블록을 쓰지 말자

파이썬 루프는 다른 언어에서 볼 수 없는 추가적인 기능이 있는데 루프에서 반복되는 내부 블록 다음에 else 블록을 둘 수 있는 기능이다.

```py
for i in range(3):
    print('Loop %d' % i)
else:
    print('Else block!')

>>>
Loop 0
Loop 1
Loop 2
Else block!
```

else 블록은 루프가 종료되면 실행된다.

이전 블록이 실행되지 않으면 이 블록이 실행된다는 의미의 if/else 문이나 이전 블록이 실패하지 않으면 실행하라는 의미의 try/except/else( Ch13 참조 )와는 다르다.

for/else의 else 부분은 루프가 완료되지 않는다면 이 블록이 실행된다는 의미가 아니다. 실제로는 정확히 반대이다.
```py
for i in range(3):
    print('Loop %d' % i)
    if i == 1:
        break;
else:
    print('Else block!')

>>>
Loop 0
Loop 1
```

for 문이 빈 시퀀스를 처리하거나 while 루프가 처음부터 거짓인 경우에도 else 문은 실행된다.
```py
for x in []:
    print('Never runs')
else:
    print('For Else block')

while False:
    print('Never runs')
else:
    print('While Else block!')

>>>
For Else block
While Else block!
```

이렇게 동작하는 이유는 else는 루프로 먼가를 검색할 때 유용하기 때문이다. 두 숫자가 서로소인지 판별하는 예제를 보면 모든 옵션을 시도해 본 다음 루프가 끝나고 else 문은 루프가 break 문을 만나지 않아 서로소 일 때만 실행된다.
```py
a = 4
b = 9
for i in range(2, min(a,b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')

>>>
Testing 2
Testing 3
Testing 4
Coprime
```

실제로 이렇게 코드를 작성하기보다는 헬퍼함수를 작성하는 것이 좋다.
```py
def corprime(a, b):
    for i in range(2, min(a,b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True

def coprime2(a, b):
    is_corprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_corprime = False
            break;
    return is_corprime

print(corprime(a, b))
print(coprime2(a, b))

>>>
True
True
```

이렇게 작성하는 것이 낯선 코드를 접하는 개발자들이 코드를 훨씬 쉽게 이해할 수 있으며 else 문을 사용한 표현의 장점이 코드를 이해하려는 사람들이 받을 부담감보다 크지 않다.

## 정리
1. 파이썬에는 for, while 다음 else 문이 오는 문법이 있다.
2. 루프 본문이 break 문으로 끝나지 않으면 else 문이 실행된다.
3. else 문을 루프 구문에 사용하면 혼란스러우니 쓰지 말자.