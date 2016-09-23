from collections import namedtuple


class SimpleGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)


book = SimpleGradebook()
book.add_student('some one')
book.report_grade('some one', 90)

print(book.average_grade('some one'))

print('-' * 40)


class BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grade in by_subject.values():
            total += sum(grade)
            count += len(grade)
        return total / count

book = BySubjectGradebook()
book.add_student('some one')
book.report_grade('some one', 'Math', 75)
book.report_grade('some one', 'Math', 65)
book.report_grade('some one', 'Gym', 90)
book.report_grade('some one', 'Gym', 95)

print(book.average_grade('some one'))

print('-' * 40)


class WeigthedGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, grade, weight):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append((grade, weight))

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total_grade, total_weight = 0, 0
            for grade, weight in grades:
                total_grade += grade * weight
                total_weight += weight
            total += total_grade / total_weight
            count += len(by_subject)
        return total / count

book = WeigthedGradebook()
book.add_student('some one')
book.report_grade('some one', 'Math', 75, 1.0)
book.report_grade('some one', 'Math', 65, 0.5)

print(book.average_grade('some one'))

print('-' * 40)

Grade = namedtuple('Grade', ('score', 'weight'))
p = Grade(100, 0.5)
# 이름으로 접근할 수 있다.
print(p.score, p.weight)

print('-' * 40)


class Subject(object):
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student(object):
    def __init__(self):
        self._subjects = {}

    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
        count += len(self._subjects)
        return total / count


class Gradebook(object):
    def __init__(self):
        self._student = {}

    def student(self, name):
        if name not in self._student:
            self._student[name] = Student()
        return self._student[name]

book = Gradebook()
someone = book.student('someone')
math = someone.subject('math')
math.report_grade(80, 0.10)

print(someone.average_grade())