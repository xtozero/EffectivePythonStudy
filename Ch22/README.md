# 딕셔너리와 튜플보다는 헬퍼 클래스로 관리하자

파이썬의 딕셔너리는 예상치 못한 식별자를 관리하는데 매우 편리하다.

하지만 구조가 복잡해지면 딕셔너리와 튜플을 사용했을 때 코드를 이해하기가 훨씬 어려워진다. 예제를 통해서 딕셔너리와 튜플을 사용했을 때 코드가 복잡해지는 과정을 정리해보자.

학생의 점수를 받아서 평균을 내는 클래스가 있다고 하면 아래와 같이 작성할 수 있다.
```py
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

>>>
90.0
```

아주 간단하게 사용할 수 있는 클래스이다. 이 정도로 구현할 내용이 간단하다면 딕셔너리를 사용하는 것도 괜찮다. 하지만 성적을 과목별로 저장한다고 가정해서 위의 클래스를 확장하면 점점 복잡해지는 것을 느낄 수 있다.
```py
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

>>>
81.25
```

학생별 성적을 저장하는 딕셔너리 안에 과목별 성적을 저장하기 위한 딕셔너리를 하나 더 만들어 각각의 성적을 기록하고 있다. 여기에 과목별 성적에 비중을 다르게 주길 원한다고 하면 더 복잡해진다.
```py
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

>>>
71.66666666666667
```

average_grade 함수는 매우 복잡해졌다. 관리하기가 복잡하다고 느껴졌다면 즉시 클래스로 옮겨야 한다.

우선 성적부터 옮기자. 성적을 표현하는 데는 튜플이면 충분하다. collections의 namedtuple 을 사용하면 성적을 간단하게 표현할 수 있다.
```py
Grade = namedtuple('Grade', ('score', 'weight'))
p = Grade(100, 0.5)
# 이름으로 접근할 수 있다.
print(p.score, p.weight)

>>>
100 0.5
```

다음으로는 단일 과목에 대한 성적을 담는 클래스를 작성하자.
```py
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
```

다음으로 학생 클래스를 작성하자 학생은 여러 과목을 공부할 수 있다.
```py
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
```

마지막으로 컨테이너 클래스를 작성하여 학생들을 관리하도록 하자.
```py
class Gradebook(object):
    def __init__(self):
        self._student = {}

    def student(self, name):
        if name not in self._student:
            self._student[name] = Student()
        return self._student[name]
```

코드의 양은 늘었지만 각 부분의 로직은 간단하게 변하였고 사용하는 방식도 더욱더 명료하다.
```py
book = Gradebook()
someone = book.student('someone')
math = someone.subject('math')
math.report_grade(80, 0.10)

print(someone.average_grade())

>>>
80.0
```

## 정리
1. 다른 딕셔너리나 긴 튜플을 담은 딕셔너리를 생성하지 말자
2. 정식 클래스의 유연성이 필요 없는 가벼운 불변 데이터 컨테이너에는 namedtuple 이 적절하다.
3. 딕셔너리를 사용했을 때 복잡해지면 클래스로 작성하는 것이 좋다.