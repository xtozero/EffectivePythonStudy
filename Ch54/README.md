# 배포 환경을 구성하는 데는 모듈 스코프 코드를 고려하자

프로그램을 작성하거나 수정하려면 개발에 사용 중인 컴퓨터에서 프로그램이 동작하게 해야 한다. <br>
개발 환경의 설정은 제품 환경과 다를 수 있다. 일례로 리눅스 워크스테이션으로 슈퍼컴퓨터용 프로그램을 작성할 수 있다. <br>
pyvenv([Ch53 참조](../Ch53))를 사용하면 파이썬 패키지를 동일하게 설정하기는 쉽지만 제품 환경에서 요구되는 많은 외부 구현을 고려하기 어렵다.

이런 경우에는 배포 환경별로 서로 다른 기능을 제공할 수 있도록 프로그램 일부를 오버라이드할 수 있다.
```py
# dev_main.py
TESTING = True
import db_connection
db = db_connection.Database()

# prod_main.py
TESTING = False
import db_connection
db = db_connection.Database()
```

위의 예제 코드는 서로 다른 파일에 대한 코드로 TESTING 상수의 값이 서로 다르게 설정되어 있다. <br>
프로그램에서 다른 모듈들은 \_\_main\_\_ 모듈을 임포트하고 TESTING 상수의 값을 통해서 동작을 분기하는 형태로 구현된다.
```py
# db_connection.py
import __main__

class TestingDatabase(Object):
    #...

class RealDatabase(Obeject):
    #...

if __main__.TESTING:
    Database = TestingDatabase
else:
    Database = RealDatabase
```

모듈 수준에서 if문을 사용하여 모듈이 이름을 정의하는 방법을 결정할 수 있으며 모듈을 다양한 배포 환경에 맞게 만들 수 있다. <br>

## 정리
1. 배포 환경마다 고유한 설정이 있다.
2. 모듈 스코프에서 if문을 통한 분기로 모듈 콘텐츠를 다른 배포 환경에 맞출 수 있다.