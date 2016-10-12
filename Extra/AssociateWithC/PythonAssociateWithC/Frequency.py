class FrequencyList(list):
    def __init__(self, numbers):
        super().__init__(numbers)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts
