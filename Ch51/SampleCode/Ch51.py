def determine_weight(volume, density):
    if density <= 0:
        raise InvalidDensityError()
        # raise ValueError('Density must be positive')


class Error(Exception):
    """
    이 모듈의 예러를 위한 기본 클래스
    """


class InvalidDensityError(Error):
    """
    인수로 넘어온 Density 값에 문제가 있음.
    """

# 예외가 퍼저나가는 것을 방지
try:
    weight = determine_weight(1, -1)
except Error as e:
    # 해당 예외를 처리
    print(e)