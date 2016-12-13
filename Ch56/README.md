# unittest로 모든 것을 테스트하자

파이썬은 정적 타임 검사를 제공하지 않기 때문에 인터프리터가 코드를 실행해 보기 전에 프로그램이 제대로 동작할 것이라고 보장할 수 없다. <br>
어떤 프로그램이든 코드를 꾸준히 테스트하는 것이 중요하지만 파이썬에서는 프로그램을 신뢰할 수 있도록 작성하는 유일한 방법이 직접 테스트를 작성하는 것밖에 없다. <br>
테스트를 작성하는 가장 간단한 방법은 내장 모듈 unittest를 사용하는 것이다.
한가지 예로 아래와 같은 유틸리티 함수를 정의했다고 하자.
```py
#util.py

def to_str(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        raise TypeError('Must supply str or bytes')
```

위의 코드를 테스트하기 위해서 unittest 내장 모듈을 사용하여 아래와 같은 테스트 코드를 작성할 수 있다.
```py
from unittest import TestCase, main
from util import to_str


class UtilsTestCase(TestCase):
    def test_to_str_byte(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_to_str_bad(self):
        self.assertRaises(TypeError, to_str, object())

if __name__ == '__main__':
    main()

>>>
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

테스트는 TestCase 클래스로 구성되어 있으며 test로 시작하는 메서드를 작성하여 테스트 케이스를 작성할 수 있다. <br>
테스트 메서드가 어떠한 종류의 예외도 발생하지 않고 실행되면 테스트를 성공적으로 통과한 것이다. <br>
TestCase 클래스는 테스트에서 assertion을 발생시키는 데 필요한 헬퍼 메서드를 제공한다. 몇 가지 예를 들면 다음과 같다. <br>

1. assertEqual - 동등성 검사
2. assertTrue - bool 표현식 검사
3. assertRaises - 적절할 때 예외가 발생하는지 검사

TestCase 서브 클래스에 자신만의 헬퍼 메서드를 정의하여 테스트를 더 이해하기 쉽게 할 수 있다. 다만 이름이 test로 시작하지만 않으면 된다. <br>
때때로 TestCase 클래스에서 테스트 메서드를 실행하기 전에 환경을 설정해야 하는 경우가 있다 <br>
이 경우 setUp과 tearDown메서드를 오버라이드하면 된다.
```py
class UtilsTestCase(TestCase):
    def setUp(self):
        print('Setup')

    def tearDown(self):
        print('Clean Up')

# ...
>>>
...
Setup
Clean Up
Setup
Clean Up
Setup
Clean Up
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

## 정리
1. 파이썬 프로그램을 신뢰할 수 있는 유일한 방법은 테스트 케이스를 작성하는 것이다.
2. 테스트 케이스는 unittest 내장 모듈의 TestCase 클래스를 통해서 작성할 수 있다.
3. TestCase의 각 테스트 케이스틑 test로 시작하는 메서드이다.
4. 단위 테스트(고립된 기능용)와 통합 테스트(상호 작용하는 모듈용) 모두를 작성해야 한다.
