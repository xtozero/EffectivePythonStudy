# 자식 프로세스를 관리하려면 subprocess를 사용하자

파이썬은 자식 프로세스 실행과 관리용 라이브러리를 갖추고 있다. <br>
파이썬으로 시작한 자식 프로세스는 병렬로 실행할 수 있으므로 파이썬을 이용하면 CPU 코어를 모두 사용하여 프로그램의 처리량을 증가시킬 수 있다. <br>
파이썬에서는 subprocess 모듈을 사용해서 자식 프로세스를 간단하게 관리할 수 있다.
```py
import subprocess

proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
print(out.decode('utf-8'))

>>>
"Hello from the child!"
```

Popen 생성자가 프로세스를 시작하고 communicate 메서드는 자식 프로세스의 출력을 읽어오고 자식 프로세스가 종료할 때까지 대기한다. <br>
자식 프로세스는 부모 프로세스와 파이썬 인터프리터와는 독립적으로 실행되며 자식 프로세스의 상태는 파이썬이 다른 작업을 하는 동안 주기적으로 확인한다.
```py
proc = subprocess.Popen(['sleep', '0.3'], shell=True)
while proc.poll() is None:
    print('Working...')

print('Exit status', proc.poll())

>>>
.
.
.
Working...
Working...
Exit status 1
```

부모에서 자식 프로세스를 실행하면 부모 프로세스가 자유롭게 여러 자식 프로세스를 병렬로 실행할 수 있다.
```py
def run_sleep(period):
    proc = subprocess.Popen(['sleep', '0.3'], shell=True)
    return proc

start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)

for proc in procs:
    proc.communicate()
end = time()
print('Finished in %.3f seconds' % (end - start))

>>>
Finished in 0.748 seconds
```

또한, 파이프를 이용해서 데이터를 자식 프로세스로 보낸 다음 해당 결과를 받아올 수 있다.
자식 프로세스가 종료되지 않거나 입력 또는 출력 파이프에서 블록될 염려가 있다면 communicate 메서드에 timeout 인수를 넘겨서 일정 시간 동안 응답이 없을 때 예외를 일으키게 할 수 있다.
```py
proc = run_sleep(10)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()
```

## 정리
1. 자식 프로세스를 실행하고 자식 프로세스의 입출력 스트림을 관리하려면 subprocess 모듈을 사용하자.
2. 자식 프로세스는 파이썬 인터프리터와 병렬로 실행된다.
3. communicate에서 timeout 인수를 통해서 자식 프로세스들이 교착 상태에 빠졌을 때 빠져나올 수 있다.