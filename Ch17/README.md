# 인수를 순회할 때는 방어적으로 하자

[Ch16](..\Ch16)에서 다루었듯이 이터레이터는 결과를 한 번만 생성한다. 이미 __StopIteration__을 일으킨 이터레이터나 제너레이터를 순회하면 어떤 결과도 얻을 수 없다.

아래와 같이 각 도시를 방문자의 비중을 구하는 프로그램이 있다고 하자.
```py
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)

>>>
[11.538461538461538, 26.923076923076923, 61.53846153846154]
```

리스트에 대해서는 정상적으로 작동하는 것을 볼 수 있다. 이 함수에 만약 제너레이터를 전달한다고 한다면 결과를 한 번만 생성하도록 구현되어 있기 때문에 아래와 같이 잘 못된 결과를 얻게 된다.
```py
def read_visit(data_path):
    with open(data_path, 'r') as f:
        for line in f:
            yield int(line)


it = read_visit('testfile.txt')
percentages = normalize(it)
print(percentages)

>>>
[]
```

위 예제에서 제너레이터에서 생성된 이터레이터는 normalize 함수 내에서 sum을 구하고 전부 소진되어 바로 다음의 for 문을 수행하지 못하였고 그 결과 빈 리스트를 반환하였다.

이미 소진한 이터레이터를 순회하더라도 오류가 일어나지 않는데 파이썬의 for 루프나 list 생성자 등 많은 함수는 이상적인 동작 과정에서 StopIteration 예외가 발생할 것이라고 기대한다.

이 문제를 해결하려면 이터레이터의 전체 복사본을 함수 내에서 생성해야 한다.
```py
def normalize2(numbers):
    numbers = list(numbers)
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

it = read_visit('testfile.txt')
percentages = normalize2(it)
print(percentages)

>>>
[11.538461538461538, 26.923076923076923, 61.53846153846154]
```

정상적으로 작동하는 것을 확인할 수 있지만 이렇게 되면 제너레이터를 사용하는 의미가 없다. 따라서 아래의 예제와 같이 이터레이터를 매번 생성하는 재너레이터 함수를 인자로 넘겨주는 방법을 사용해 볼 수 있다.
```py
def normalize_func(get_iter):
    total = sum(get_iter()) # 새 이터레이터
    result = []
    for value in get_iter(): # 새 이터레이터
        percent = 100 * value / total
        result.append(percent)
    return result

percentages = normalize_func(lambda: read_visit('testfile.txt'))
print(percentages)

>>>
[11.538461538461538, 26.923076923076923, 61.53846153846154]
```

잘 동작하지만 세련되지 못하다. 같은 결과를 얻는 더 좋은 방법은 이터레이터 프로토콜을 구현한 새 컨테이너 클래스를 제공하는 것이다.

이터레이터 프로토콜을 파이썬의 for 루프가 컨테이너 타입을 순회하는 방법이다. 파이썬은 아래와 같은 순서로 콘텐츠를 탐색한다.

1. for x in foo 같은 문장에서 iter(foo)를 호출한다.
2. 내장 함수 iter()는 특수 메서드 foo.\_\_iter\_\_를 호출한다.
3. \_\_iter\_\_ 메서드는 \_\_next\_\_ 메서드를 구현한 이터레이터 객체를 반환한다.
4. for는 StopIteration 예외가 발생할 때까지 이터레이터 객체에 next 함수를 호출한다.

이터레이터 프로토콜에 맞춰 클래스를 작성하면 아래와 같이 정상적으로 동작한다.
```py
class ReadVisit(object):
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path, 'r') as f:
            for line in f:
                yield int(line)

visits = ReadVisit('testfile.txt')
percentages = normalize(visits)
print(percentages)

>>>
[11.538461538461538, 26.923076923076923, 61.53846153846154]
```

매번 새로운 이터레이터를 생성해야 해서 입력 데이터를 여러 번 읽지만 잘 동작하는 것을 확인할 수 있다.

마지막으로 파라미터가 단순한 이터레이터가 아님을 보장하는 함수를 작성하면 된다. 프로토콜에 따르면 내장 함수 iter에 이터레이터를 넘기면 같은 이터레이터가 반환된다. 반면 iter에 위의 예제 코드와 같은 컨테이터 클래스를 전달하면 새로운 이터레이터가 반환된다.
```py
def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers):
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
normalize_defensive(visits)
visits = ReadVisit('testfile.txt')
normalize_defensive(visits)
it = read_visit('testfile.txt')
normalize_defensive(it) # 여기서 예외 발생
```

## 정리
1. 입력 인수를 여러 번 순회하는 함수는 조심해서 작성해야 한다.
2. \_\_iter\_\_메서드를 제너레이터로 구현하면 자신만의 이터러블 컨테이너 타입을 쉽게 정의할 수 있다.
3. 어떤 변수에 iter 메서드를 두 번 호출하였을 때 같은 결과가 나오고 내장 함수 next로 전진시킬 수 있으면 컨테이너가 아닌 이터레이터이다.