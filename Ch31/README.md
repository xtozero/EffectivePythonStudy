# 재사용 가능한 @property 메서드에는 디스크립터를 사용하자

@property 데코레이터는 같은 클래스에 속한 여러 속성에 사용하지 못하거나 관련 없는 클래스에 재사용할 수 없어 재사용성이 떨어진다. <br>
시험 과목별 성적을 기록하는 클래스가 있다고 한다면 @property를 각 과목별로 작성해야 한다.
```py
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
```

이런 방식은 재사용성이 매우 떨어져 점수 구간 검증을 하려면 @property 관련 코드를 반복적으로 작성하여야 한다. <br>
파이썬에서는 이런 작업을 할 때 디스크립터를 사용해서 범용적으로 코드를 작성할 수 있다. <br>
디스크립터 프로토콜은 속성에 대한 접근을 언어에서 해석하는 방법을 정의하며 반복 코드 없이 \_\_get\_\_과 \_\_set\_\_메서드를 제공할 수 있다. <br>
아래와 같은 Grade 클래스가 존재한다고 하자.
```py
class Grade(object):
    def __get__(*args, **kwargs):
        pass

    def __set__(*args, **kwargs):
        pass


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

exam = Exam()
exam.writing_grade = 40
```

속성에 대한 대입 코드는 아래와 같이 해석된다.
```py
Exam.__dict__['writing_grade'].__set__(exam, 40)
```

속성을 얻어올 때에는 아래와 같이 해석된다.
```py
Exam.__dict__['writing_grade'].__get__(exam, Exam)
```

이렇게 클래스가 동작하는 것은 object의 __getattribute__ 메서드 때문이다. Exam 인스턴스에 writing_grade 속성이 없다면 파이썬은 대신 Exam 클래스의 속성을 사용하며 이 클래스의 속성이 \_\_get\_\_, \_\_set\_\_ 메서드를 갖춘 객체라면 디스크립터 프로토콜을 따른다고 가정한다. <br>
이런 동작을 이해하고 Grade 클래스를 완성해보면 아래와 같다.
```py
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

>>>
Writing 82
Math 100
Science 87
```

잘 동작하는 것처럼 보이지만 여러 인스턴스를 사용하면 예상하지 못했던 동작을 보여준다.
```py
final_exam = Exam()
final_exam.writing_grade = 50
final_exam.math_grade = 40
final_exam.science_grade = 10
print('Mid Writing', mid_exam.writing_grade)
print('Final Writing', final_exam.writing_grade)

>>>
Mid Writing 50
Final Writing 50
```

문제는 한 Grade 인스턴스가 모든 Exam 인스턴스의 속성을 공유해서 발생한다. <br>
이 문제를 해결하려면 Grade 클래스가 인스턴스 별로 값을 추적하도록 해야 한다.
```py
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
    # 이전 예제와 같음

mid_exam = Exam()
mid_exam.writing_grade = 82
final_exam = Exam()
final_exam.writing_grade = 50
print('Mid Writing', mid_exam.writing_grade)
print('Final Writing', final_exam.writing_grade)
```

이 구현은 잘 동작하지만 여전히 한 가지 문제점을 가지고 있다. 사용하지 않는 인스턴스에 대한 정보를 계속 가지고 있다는 점이다. <br>
이런 경우 파이썬 내장 모듈 weakref를 사용해서 사용하지 않는 인스턴스의 정보를 해제하도록 할 수 있다. <br>
weakref는 dict를 대체하는 WeakKeyDictionary 클래스를 제공한다. WeakKeyDictionary 클래스는 런타임에 마지막으로 남은 Exam 인스턴스의 참조를 가지고 있을 때 키집합에서 Exam 인스턴스를 제거한다.
```py
class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()
    
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

>>>
1
1
```

\_\_set\_\_ 에서 현재 dict의 원소 개수를 출력하도록 한 결과 인스턴스가 정상적으로 해제되는 것을 확인할 수 있었다.

## 정리
1. 디스크립터 클래스를 정의하면 @property 메서드의 동작을 재사용할 수 있다.
2. WeakKeyDictionary를 사용하여 디스크립터 클래스의 메모리 누수를 해결할 수 있다.