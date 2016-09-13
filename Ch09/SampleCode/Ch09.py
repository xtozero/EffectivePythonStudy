value = [len(x) for x in open('my_file.txt')]
print(value)

print('-' * 40)

it = (len(x) for x in open('my_file.txt'))
print(it)

print('-' * 40)

print(next(it))
print(next(it))

print('-' * 40)

root = ((x, x ** 5) for x in it)
print(next(root))
