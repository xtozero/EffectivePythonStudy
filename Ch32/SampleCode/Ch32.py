class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

db = LazyDB()
print('Before:', db.__dict__)
print('Foo:', db.foo)
print('After:', db.__dict__)

print('-' * 40)


class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

db = LoggingLazyDB()
print('Exist:', db.exists)
print('Foo:', db.foo)
print('Foo:', db.foo)

print('-' * 40)


class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

db = ValidatingDB()
print('Exist:', db.exists)
print('Foo:', db.foo)
print('Foo:', db.foo)

print('-' * 40)


class MissingPropertyDB(object):
    def __getattr__(self, name):
        if name == 'invalid_name':
            raise AttributeError('%s is invalid name' % name)
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

db = MissingPropertyDB()
# db.invalid_name

print('foo exsit', hasattr(db, 'foo'))

print('-' * 40)


class SavingDB(object):
    def __setattr__(self, key, value):
        print('Called __setattr__(%s %r)' %(key, value))
        super().__setattr__(key, value)

db = SavingDB()
print('Before:', db.__dict__)
db.foo = 5
print('After:', db.__dict__)
db.foo = 7
print('Finally:', db.__dict__)

print('-' * 40)


class BrokenDictionaryDB(object):
    def __init__(self):
        self._data = {}

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return self._data[name]

db = BrokenDictionaryDB()
# db.foo


class DictionaryDB(object):
    def __init__(self):
        self._data = {}

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')
        return data_dict[name]
