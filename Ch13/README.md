# try/except/else/finally에서 각 블록의 장점을 이용하자

파이썬에는 예외를 처리하는 과정에서 네 가지 블록을 사용한다. __try, except, else, finally__ 가 그것이다. 각 블럭은 독자적인 기능을 하며 이를 조합하면 유용하게 사용할 수 있다.

예외를 전달하고는 싶지만, 예외가 발생해도 반드시 실행돼야 하는 구문이라면 finally를 사용하면 된다.
```py
handle = open('random_data.txt') # IOError의 가능성
try:
    data = handle.read() # UnicodeDecodeError의 가능성
finally:
    print('finally')
    handle.close() # try: 이후에 항상 실행

>>>
finally
Traceback (most recent call last):
  File "C:/Users/xtozero/Documents/GitHub/EffectivePythonStudy/Ch13/SampleCode/Ch13.py", line 5, in <module>
    data = handle.read() # UnicodeDecodeError의 가능성
UnicodeDecodeError: 'cp949' codec can't decode byte 0xec in position 0: illegal multibyte sequence
```

이와 같이 handle.close()가 호출되는 것이 보장된다.

else 문은 try 문에서 예외가 발생하지 않았을 때 실행된다. JSON 파일에서 데이터를 로드하여 그 안에 든 키의 값을 반환한다고 하면 아래와 같이 코드를 작성할 수 있다.
```py
def load_json_key(data, key):
    try:
        result_dic = json.loads(data)
    except ValueError as e:
        raise KeyError from e
    else:
        return result_dic[key]

print(load_json_key('{"bar":["baz", null, 1.0, 2]}', 'bar'))

>>>
['baz', None, 1.0, 2]
```

복합문을 한번에 사용하면 아래와 같다.

```py
UNDEFINED = object()


def divide_json(path):
    handle = open(path, 'r+')
    try:
        data = handle.read()
        op = json.loads(data)
        value = (op['numerator'] / op['denominator'])
    except ZeroDivisionError as e:
        return UNDEFINED
    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)
    finally:
        handle.close()

divide_json('random_data.txt')

>>> 해당 json 파일에 기록됨
{"result": 0.5, "denominator": 20, "numerator": 10}
```

여기서 try 문에서 발생한 예외가 except에서 처리되고 예외가 발생하지 않았다면 JSON 파일에 값을 쓰는 작업이 수행된다. 예외가 발생하든 발생하지 않든 finally에서 정상적으로 파일 핸들이 해제된다.

## 정리
1. finally 문은 예외 발생 여부에 상관없이 실행된다.
2. 예외가 발생하지 않으면 else 문이 실행된다.