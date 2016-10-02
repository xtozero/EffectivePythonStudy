from weakref import WeakKeyDictionary


class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must ve between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value


class Grade(object):
    def __init__(self):
        self.value = 0

    def __get__(self, instance, instance_type):
        return self.value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must ve between 0 and 100')
        self.value = value


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

mid_exam = Exam()
mid_exam.writing_grade = 82
mid_exam.math_grade = 100
mid_exam.science_grade = 87
print('Writing', mid_exam.writing_grade)
print('Math', mid_exam.math_grade)
print('Science', mid_exam.science_grade)

print('-' * 40)

final_exam = Exam()
final_exam.writing_grade = 50
final_exam.math_grade = 40
final_exam.science_grade = 10
print('Mid Writing', mid_exam.writing_grade)
print('Final Writing', final_exam.writing_grade)

print('-' * 40)


class Grade(object):
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must ve between 0 and 100')
        self._values[instance] = value


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

mid_exam = Exam()
mid_exam.writing_grade = 82
final_exam = Exam()
final_exam.writing_grade = 50
print('Mid Writing', mid_exam.writing_grade)
print('Final Writing', final_exam.writing_grade)

print('-' * 40)


class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must ve between 0 and 100')
        self._values[instance] = value
        print(len(self._values))


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

mid_exam = Exam()
mid_exam.writing_grade = 82
mid_exam = None
final_exam = Exam()
final_exam.writing_grade = 50
