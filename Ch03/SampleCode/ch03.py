# python 3.5.2 version


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value


encoded_str = to_bytes('파이썬 코딩의 기술')
print(type(encoded_str))
print(encoded_str)
decoded_str = to_str(encoded_str)
print(type(decoded_str))
print(decoded_str)

with open('test.txt', 'w', encoding='utf-8') as f:
    f.write('파이썬 코딩의 기술')

# 여기서 에러가 발생합니다.
with open('test.txt', 'r') as f:
    print(f.read())


