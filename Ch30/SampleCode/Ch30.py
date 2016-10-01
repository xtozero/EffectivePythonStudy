from datetime import timedelta
from datetime import datetime


class Bucket(object):
    def __init__(self, period):
        self.period_data = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Buket(quota=%d)' % self.quota


def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_data:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_data:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True

bucket = Bucket(60)
fill(bucket, 100)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)

print('-' * 40)


class Bucket(object):
    def __init__(self, period):
        self.period_data = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return 'Buket(max_quota=%d, quota_consume=%d)' % (self.max_quota, self.quota_consumed)

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

bucket = Bucket(60)
fill(bucket, 100)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)
