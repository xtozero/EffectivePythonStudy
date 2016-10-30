from time import localtime, strftime
from time import mktime, strptime
from datetime import datetime, timezone
import pytz

now = 1407694710
local_tuple = localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'
time_str = strftime(time_format, local_tuple)
print(time_str)

print('-' * 40)

time_tuple = strptime(time_str, time_format)
utc_now = mktime(time_tuple)
print(utc_now)

print('-' * 40)

# 아래의 예제는 정상적으로 동작하지 않음
# parse_format = '%Y-%m-%d %H:%M:%S %Z'
# depart_sfo = '2014-05-01 15:45:16 EDT'
# time_tuple = strptime(depart_sfo, parse_format)
# time_str = strftime(time_format, time_tuple)
# print(time_str)

now = datetime(2016, 10, 30, 21, 5, 30)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print(now_local)

print('-' * 40)

time_str = '2016-10-30 21:05:30'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = mktime(time_tuple)
print(utc_now)

print('-' * 40)


arrival_nyc = '2014-05-01 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(utc_dt)

pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(sf_dt)
