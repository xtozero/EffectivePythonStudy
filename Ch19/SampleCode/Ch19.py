def remainder(number, divisor):
    return number % divisor

print(remainder(20, 7))
print(remainder(20, divisor=7))
print(remainder(number=20, divisor=7))
print(remainder(divisor=7, number=20))

# 아래 주석을 해제하면 에러가 발생
# remainder(number=20, 7)
# remainder(20, number=7)

print('-' * 40)


def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print('%.3f kg per second' % flow)

flow = flow_rate(weight_diff, time_diff, period=3600)
print('%.3f kg per hour' % flow)

print('-' * 40)


def flow_rate_extend(weight_diff, time_diff, period=1, units_per_kg=1):
    return ((weight_diff / units_per_kg) / time_diff) * period

flow = flow_rate_extend(weight_diff, time_diff)
print('%.3f kg per second' % flow)

flow = flow_rate_extend(weight_diff, time_diff, period=3600)
print('%.3f kg per hour' % flow)

flow = flow_rate_extend(weight_diff, time_diff, period=3600, units_per_kg=2.2)
print('%.3f kg per hour' % flow)

flow_rate_extend(weight_diff, time_diff, 3600, 2.2)
