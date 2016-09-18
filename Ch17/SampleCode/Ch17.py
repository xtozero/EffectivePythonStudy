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

print('-' * 40)


def read_visit(data_path):
    with open(data_path, 'r') as f:
        for line in f:
            yield int(line)


it = read_visit('testfile.txt')
percentages = normalize(it)
print(percentages)

print('-' * 40)


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

print('-' * 40)


def normalize_func(get_iter):
    total = sum(get_iter()) # 새 이터레이터
    result = []
    for value in get_iter(): # 새 이터레이터
        percent = 100 * value / total
        result.append(percent)
    return result

percentages = normalize_func(lambda: read_visit('testfile.txt'))
print(percentages)

print('-' * 40)


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
# 아래 주석을 풀면 예외 발생
# normalize_defensive(it)
