class SampleObject(object):
    def __init__(self):
        self.public_field = 5 # 어디서든 접근 가능
        self.__private_field = 10 # 외부에서 직접 접근 불가

    def get_private_field(self):
        return self.__private_field

obj = SampleObject()
print(obj.public_field)
# 아래 주석을 해제하면 에러
#print(obj.__private_field)

print('-' * 40)

print(obj._SampleObject__private_field)

print('-' * 40)


class ParentClass(object):
    def __init__(self, value):
        # 사용자가 객체에 전달한 값을 저장한다.
        # 문자열로 강제할 수 있는 값이어야 하며,
        # 객체에 할당하고 나면 불변으로 취급해야 한다.
        self.value = value


class ApiClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' #충돌

a = Child()
print(a.get(), 'and', a._value, 'should be different')

print('-' * 40)


class ApiClass(object):
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' #충돌

a = Child()
print(a.get(), 'and', a._value, 'should be different')