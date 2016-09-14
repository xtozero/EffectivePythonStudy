from itertools import zip_longest

names = ['Cecilia', 'Lise', 'Marie']
letters = [len(n) for n in names]
print(letters)

print('-' * 40)

longest_name = None
max_latters = 0;

for i in range(len(names)):
    count = letters[i]
    if count > max_latters:
        longest_name = names[i]
        max_latter = count

print(max_latters)

print('-' * 40)

for i, name in enumerate(names):
    count = letters[i]
    if count > max_latters:
        longest_name = name
        max_latters = count

print(max_latters)

print('-' * 40)

for name, count in zip(names, letters):
    if count > max_latters:
        longest_name = name
        max_latters = count

print(max_latters)

print('-' * 40)

names.append('Rosalind')
for name, count in zip(names, letters):
    print(name)

print('-' * 40)

for name, count in zip_longest( names, letters ):
    print(name, count)