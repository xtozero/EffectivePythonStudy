# python 2.7.12 version
# coding: utf-8


def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value


def to_str(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value


encoded_unicode = to_str('파이썬 코딩의 기술')
print(type(encoded_unicode))
print(encoded_unicode)

decoded_byte = to_unicode(encoded_unicode)
print(type(decoded_byte))
print(decoded_byte)

with open('test.txt', 'w') as f:
    f.write('파이썬 코딩의 기술')

with open('test.txt', 'r') as f:
    print(f.read())

