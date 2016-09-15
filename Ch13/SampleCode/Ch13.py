import json

# 아래 주석들을 풀면 예외 발생
# handle = open('random_data.txt')
# try:
#    data = handle.read() # UnicodeDecodeError의 가능성
# finally:
#    print('finally')
#    handle.close() # try: 이후에 항상 실행


def load_json_key(data, key):
    try:
        result_dic = json.loads(data)
    except ValueError as e:
        raise KeyError from e
    else:
        return result_dic[key]

print(load_json_key('{"bar":["baz", null, 1.0, 2]}', 'bar'))

print('-' * 40)

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
