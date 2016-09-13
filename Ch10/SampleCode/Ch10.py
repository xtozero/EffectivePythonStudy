from random import randint


random_bits = 0
for i in range(64):
    if randint(0, 1):
        random_bits |= 1 << i

print(random_bits)

print('-' * 40)

flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for flavor in flavor_list:
    print('%s is delicius' % flavor)

print('-' * 40)

for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d: %s is delicius' % (i + 1,  flavor))

print('-' * 40)

for i, flavor in enumerate(flavor_list):
    print('%d: %s' % (i + 1, flavor))

print('-' * 40)

for i, flavor in enumerate(flavor_list, 1):
    print('%d: %s' % (i, flavor))
