class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

r0 = OldResistor(50)
r0.set_ohms(r0.get_ohms() + 5e3)


class ModernResistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = ModernResistor(50e3)
r1.ohms = 10e3
r1.ohms += 5e3


class PropertyResistor(ModernResistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

r2 = PropertyResistor(1e3)
print('Before: %5r amps' % r2.current)
r2.voltage = 10
print('After: %5r amps' % r2.current)


class FixedResistor(ModernResistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._ohms = ohms

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError('Can\'t set attribute')
        self._ohms = ohms

r4 = FixedResistor(1e3)
# 주석을 풀면 에러
# r4.ohms = 2e3
