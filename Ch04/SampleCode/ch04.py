from urllib.parse import parse_qs

my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
# __repr__ 호출
print(repr(my_values))

print('-'*40)

print('Red          ', my_values.get('red'))
print('Green        ', my_values.get('green'))
print('Opacity      ', my_values.get('opacity'))

print('-'*40)

# dict.get(key, default=None)
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print('Red          ', red)
print('Green        ', green)
print('Opacity      ', opacity)

print('-'*40)

red = my_values.get('red', [''])
red = int(red[0]) if red[0] else 0

green = my_values.get('green')
green = int(green[0]) if green[0] else 0

opacity = my_values.get('opacity', [''])
opacity = int(opacity[0]) if opacity[0] else 0
print('Red          ', red)
print('Green        ', green)
print('Opacity      ', opacity)

print('-'*40)

def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found

red = get_first_int(my_values, 'red', 0)
green = get_first_int(my_values, 'green', 0)
opacity = get_first_int(my_values, 'opacity', 0)
print('Red          ', red)
print('Green        ', green)
print('Opacity      ', opacity)
