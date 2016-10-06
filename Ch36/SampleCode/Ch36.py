import subprocess
from time import time

proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
print(out.decode('utf-8'))

print('-' * 40);

proc = subprocess.Popen(['sleep', '1'], shell=True)
while proc.poll() is None:
    print('Working...')

print('Exit status', proc.poll())


def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)], shell=True)
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


proc = run_sleep(10)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()