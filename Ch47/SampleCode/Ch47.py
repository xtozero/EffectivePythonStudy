from decimal import Decimal
from decimal import ROUND_UP

rate = 0.05
seconds = 5
cost = rate * seconds / 60
print(round(cost, 2))

print('-' * 40)

rate = 1.45
seconds = 222
cost = rate * seconds / 60
print(cost)

rate = Decimal('1.45')
seconds = Decimal('222')
cost = rate * seconds / Decimal('60')
print(cost)

print('-' * 40)

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)
