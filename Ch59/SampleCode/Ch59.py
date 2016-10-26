import gc
import tracemalloc


found_objects = gc.get_objects()
print('%d objects before' % len(found_objects))

x = [1, 2, 3, 4, 5, 6]
found_objects = gc.get_objects()
print('%d objects after' % len(found_objects))
for obj in found_objects[:3]:
    print(repr(obj)[:100])

print('-' * 40)

# 스택 프레임을 최대 10개 저장
tracemalloc.start(10)

time1 = tracemalloc.take_snapshot()
x = [1, 2, 3, 4, 5, 6]
time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'lineno')
for stat in stats[:3]:
    print(stat)

print('-' * 40)
stats = time2.compare_to(time1, 'traceback')
top = stats[0]
print('\n'.join(top.traceback.format()))