# 객체를 범용으로 생성하려면 @classmethod 다형성을 이용하자

파이썬에서는 클래스 차원에서의 다형성을 지원한다. 디렉터리에 들어있는 파일들의 문장 수를 세는 기능을 구현하는 예제를 보자.
```py
class InputData(object):
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()
```

PathInputData는 경로를 전달받아 해당 경로의 파일을 여는 클래스이다.
```py
class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result
```

LineCountWorker는 파일을 문장 수를 세는 간단한 카운터 클래스로 스레드에서 동작할 수 있도록 map과 reduce라는 함수를 가지고 있다. <br>
이제 이렇게 작성한 클래스를 적절하게 연결해주면 된다. 생각해 볼 수 있는 방법은 헬퍼 함수로 객체를 생성해서 연결하는 것이다.
```py
def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers
```

generate_inputs과 create_workers 함수를 통해서 객체를 적절하게 생성할 수 있다.<br>
이제 두 함수 조각을 하나로 합쳐서 스레드로 실행시킬 수 있다.
```py
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)
```

테스트로 위에서 작성한 코드를 실행시키면 잘 동작한다.
```py
result = mapreduce('testdir')
print(result)

>>>
38
```

다만 위에서 작성한 코드는 한가지 문제점이 있다. generate_inputs, create_workers 함수가 하나의 클래스만 생성할 수 있으므로 mapreduce 함수가 범용적이지 않다. <br>
만약 InputData, Worker를 상속받는 새로운 클래스를 작성한다면 generate_inputs, create_workers, mapreduce 함수를 모두 다시 작성해야 한다. <br>
이 문제는 @classmethod 다형성을 이용하여 해결할 수 있다.
```py
class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputData):
    # 이전 PathInputData __init__과 동일

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker(object):
    # 이전 Worker의 __init__과 동일

    def map(self):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers
```

@classmethod를 사용하면 일관되게 객체를 생성할 수 있으며 mapreduce 함수도 아래와 같이 범용적으로 작성할 수 있다.
```py
def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

result = mapreduce(LineCountWorker, PathInputData, {'data_dir': 'testdir'})
print(result)

>>>
38
```

이전과 같이 잘 작동하며 새로운 클래스를 생성해도 GenericInputData, GenericWorker 클래스를 상속받아 @classmethod 함수를 구현하면 손쉽게 기능을 확장할 수 있다.

## 정리
1. @classmethod로 클래스 차원의 다형성을 구현할 수 있다.