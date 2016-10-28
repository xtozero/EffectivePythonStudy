from time import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

numbers = [(1963309, 2265973), (2030677, 3814172), (1551645, 2229620), (2039045, 2020802)]
# start = time()
# result = list(map(gcd, numbers))
# end = time()
# print('Took %.3f seconds' % (end - start))

# print('-' * 40)

# start = time()
# pool = ThreadPoolExecutor(max_workers=2)
# result = list(pool.map(gcd, numbers))
# end = time()
# print('Took %.3f seconds' % (end - start))

# print('-' * 40)

# ProcessPoolExecutor 새로운 인터프리터를 띄워서 이 파일을 실행하는 구조로 추측된다.
# 위의 코드의 주석을 풀면 이상하게 동작하는 것을 확인 할 수 있었다.
if __name__ == "__main__":
    start = time()
    pool = ProcessPoolExecutor(max_workers=2)
    result = list(pool.map(gcd, numbers))
    end = time()
    print('Took %.3f seconds' % (end - start))

