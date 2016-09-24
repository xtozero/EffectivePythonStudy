from collections import defaultdict


names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=lambda x: len(x))
print(names)

print('-' * 40)


def log_missing():
    print('Key added')
    return 0

current = {'green': 12, 'blue': 3}
increments = [('red', 5), ('blue', 17), ('orange', 9)]
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After:', dict(result))

print('-' * 40)


def increment_with_report(current, increments):
    added_count = 0;

    def missing():
        nonlocal  added_count
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count

result, count = increment_with_report(current, increments)
print(count)

print('-' * 40)


class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter.missing, current)

for key, amount in increments:
    result[key] += amount

print(counter.added)

print('-' * 40)


class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
# 호출 가능하다.
counter()
print(callable(counter))

print('-' * 40)
counter = BetterCountMissing()
result = defaultdict(counter, current)

for key, amount in increments:
    result[key] += amount

print(counter.added)
