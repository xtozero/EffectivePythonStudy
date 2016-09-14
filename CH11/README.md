# 이터레이터를 병렬로 처리하려면 zip을 이용하자

파이썬에서는 관련 객체로 구성된 리스트를 많이 사용한다.

리스트 컴프리헨션을 사용하면 파생 리스트(derived list)를 쉽게 얻을 수 있다.( [Ch07](../Ch07) 참고 )
```py
names = ['Cecilia', 'Lise', 'Marie']
letters = [len(n) for n in names]
print(letters)

>>>
[7, 4, 5]
```

파생 리스트와 원본 리스트의 아이템은 서로 인덱스로 연관되어 있다. 따라서 두 리스트를 동시에 순회하려면 소스 리스트인 names의 길이만큼 순회하면 된다.
```py
longest_name = None
max_latters = 0;

for i in range(len(names)):
    count = letters[i]
    if count > max_latters:
        longest_name = names[i]
        max_latter = count

print(max_latter)

>>>
7
```

문제는 루프문이 별로 보기 안 좋다는 것이다. 코드도 읽기 어렵고 배열에 2번 접근하게 된다. enumerate를( [Ch10](../Ch10/) 참고 ) 사용하면 이런 문제점을 개선할 수 있지만 완벽하지 않다.
```py
for i, name in enumerate(names):
    count = letters[i]
    if count > max_latters:
        longest_name = name
        max_latters = count

print(max_latter)

>>>
7
```

파이썬은 위의 코드를 좀 더 명료하게 하는 내장함수 zip을 제공한다.

파이썬3에서 zip은 지연 제너레이터로 이터레이터 두 개 이상을 감싼 다음 각 이터레이터로 부터 다음 값을 담은 튜플을 얻어온다.
```py
for name, count in zip(names, letters):
    if count > max_latters:
        longest_name = name
        max_latters = count

print(max_latters)

>>>
7
```

내장 함수 zip을 사용할 때는 두 가지 문제가 있다.
1. 파이썬 2에서는 zip이 제너레이터가 아니다. 따라서 메모리 문제가 발생할 수 있으니 파이썬 2에서는 itertools의 izip을 사용해야 한다.( Ch46 참조 )
2. 입력 이터레이터들의 길이가 다르면 zip이 이상하게 동작한다.
```py
names.append('Rosalind')
for name, count in zip(names, letters):
    print(name)

>>>
Cecilia
Lise
Marie
```

새 아이템 Rosalind가 결과에 없는 것을 볼 수 있다. zip은 길이가 맞지 않으면 짧은 길이에 맞춰 출력을 잘라낸다. zip으로 실행할 리스트의 길이가 같다고 확신할 수 없다면 대신 내장 모듈 itertools의 zip_longest를 사용하는 방안을 고려해보자( 파이썬2에서는 izip_longest )
```py
for name, count in zip_longest( names, letters ):
    print(name, count)

Cecilia 7
Lise 4
Marie 5
Rosalind None
```

## 정리
1. 내장 함수 zip은 여러 이터레이터를 동시에 순회할 때 사용한다.
2. 파이썬 3의 zip은 제너레이터지만 파이썬 2는 그렇지 않다.
3. 길이가 다른 이터레이터를 사용하면 zip은 그 결과를 잘라낸다.
4. 내장 모듈 itertools의 zip_longest를 사용하면 여러 이터레이터의 길이에 상관없이 병렬로 순회할 수 있다.
