# 리스트를 반환하는 대신 제너레이터를 고려하자

문자열에 있는 모든 단어의 인덱스를 출력하고자 한다면 해당 인덱스의 리스트를 반환할 수 있다.
```py
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

address = 'Four score and seven years ago...'
result = index_words(address)
print(result[:3])


>>>
[0, 5, 11]
```

리스트로 결과를 반환하는 위의 예제는 두 가지 문제점을 가지고 있다.
1. 코드가 약간 복잡하고 깔끔하지 않다.
2. 결과를 반환하기 전에 모든 값을 리스트에 추가하므로 큰 입력에 대해서는 메모리가 고갈될 수 있다.

리스트를 반환하는 함수는 제너레이터를 사용하면 깔끔하게 작성할 수 있다.
```py
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text, 1):
        if letter == ' ':
            yield index

result = list(index_words_iter(address))
print(result)

>>>
[0, 5, 11, 15, 21, 27]
```

제너레이터는 yield 문을 사용하는 함수이다. 리스트에 값을 넣는 부분이 모두 사라져 훨씬 깔끔해진다. 제너레이터 호출로 반환되는 이터레이터는 내장 함수 list에 전달하면 리스트로 변환할 수 있다. ([Ch09 참고][..\Ch09])

제너레이터를 사용한 다른 예를 살펴보면 아래와 같다.
```py
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

with open('testfile.txt', 'r') as f:
    it = index_file(f)
    results = islice(it, 0, 3)
    print(list(results))

>>>
[0, 5, 11]
```

위 예제의 함수가 동작할 때 사용하는 메모리는 입력 한 줄의 최대 길이까지로 큰 입력에도 메모리를 절약할 수 있다.

다만 이와 같은 제너레이터를 정의 할 때는 반환되는 이터레이터에 '__상태가 있고 재사용할 수 없다__' 는 점을 명심해야 한다.

## 정리
1. 제너레이터를 사용하면 리스트를 반환하는 것보다 코드를 이해하기 쉬워지고 메모리를 아낄 수 있다.
2. 제너레이터가 반환한 이터레이터는 상태가 있고 재사용할 수 없다.