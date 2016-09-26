class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)


class TimesTwo(object):
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    def __init__(self):
        self.value += 5


# class OneWay(MyBaseClass, TimesTwo, PlusFive ):
class OneWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


foo = OneWay(5)
print('Five ordering is (5 * 2) + 5 =', foo.value)

print('-' * 40)


class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5


class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2


class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)

foo = ThisWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)


class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super(TimesFiveCorrect, self).__init__(value)
        self.value *= 5


class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super(PlusTwoCorrect, self).__init__(value)
        self.value += 2


class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        super(GoodWay, self).__init__(value)

foo = GoodWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)

print(GoodWay.mro())


class Explicit(MyBaseClass):
    def __init__(self, value):
        # 클래스 내에서 __class__ 변수를 사용하면 현재 클래스를 올바르게 참조해 준다. 2.2에서는 사용할 수 없다.
        super(__class__, self).__init__(value * 2)


class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)


print(Explicit(10).value, Implicit(10).value)