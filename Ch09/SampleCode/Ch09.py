value = [len(x) for x in open('my_file.txt')]
print(value)

it = (len(x) for x in open('my_file.txt'))
print(it)

print(next(it))
print(next(it))

root = ((x, x ** 5) for x in it)
print(next(root))
