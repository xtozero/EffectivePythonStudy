for i in range(3):
    print('Loop %d' % i)
else:
    print('Else block!')

print('-' * 40)

for i in range(3):
    print('Loop %d' % i)
    if i == 1:
        break;
else:
    print('Else block!')

print('-' * 40)

for x in []:
    print('Never runs')
else:
    print('For Else block')

while False:
    print('Never runs')
else:
    print('While Else block!')

print('-' * 40)

a = 4
b = 9
for i in range(2, min(a,b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')

print('-' * 40)

def corprime(a, b):
    for i in range(2, min(a,b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True

def coprime2(a, b):
    is_corprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_corprime = False
            break;
    return is_corprime

print(corprime(a, b))
print(coprime2(a, b))