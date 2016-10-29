# copyreg로 pickle을 신뢰할 수 있게 만들자

내장 모듈 pickle은 객체를 바이트로 직렬화하거나 바이트를 객체로 역직렬화하는데 사용한다. <br>
pickle은 바이너리 채널을 통해 프로그래머가 제어하는 프로그램 간 파이썬 객체를 넘겨주는 데 목적이 있으므로 신뢰할 수 없는 부분과 통신하는 데는 사용하면 안 된다. <br>
신뢰할 수 없는 프로그램 간 통신에는 JSON을 사용하는 것이 더 낫다. <br>
pickle을 사용하는 예제를 하나 보자
```py
import pickle


class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4

state = GameState()
state.level += 1
state.lives -= 1

state_path = './game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f)

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)
print(state_after.__dict__)

>>>
{'lives': 3, 'level': 1}
```

다만 pickle에는 중대한 문제점이 있는데 다음과 같이 GameState에 새로운 속성을 추가하여 기능을 확장할 때 발생한다.
```py
class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0

state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)
print(state_after.__dict__)

>>>
{'lives': 4, 'level': 0, 'points': 0}
{'lives': 3, 'level': 1}
```
기존에 직렬화된 데이터를 읽어오는 과정에서 새로운 속성이 누락되어 버린다. <br>
pickle을 단순한 용도 이상으로 사용하려고 할떄 발생하는 문제로 이를 해결하기 위해서 내장 모듈 copyreg를 사용한다. <br>

GameState 객체가 모든 속성을 담을 것을 보장하기 위한 가장 간단한 방법은 기본 인수가 있는 생성자를 사용하는 것이다. <br>
기본 인수를 가지는 생성자를 pickle에서 사용하기 위해서는 GameState 객체를 받아 copyreg 모듈용 파라미터 튜플로 반환해야 한다.
```py
class GameState(object):
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points


def unpickle_game_state(kwargs):
    return GameState(**kwargs)


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)

copyreg.pickle(GameState, pickle_game_state)

state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

>>>
{'level': 0, 'points': 1000, 'lives': 4}
```

새로운 속성을 추가하고 기존 직렬화 객체를 역직렬화 해보면 기본값이 들어가는 것을 확인할 수 있다.
```py
class GameState(object):
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic

state_after = pickle.loads(serialized)
print(state_after.__dict__)

>>>
{'lives': 4, 'points': 1000, 'magic': 5, 'level': 0}
```

필드를 제거해서 하위 호환성을 유지하지 않도록 해야 할 때도 있다. <br>
문제는 이런 코드는 이전 게임 데이터에 있던 모든 필드가 GameState 생성자로 전달되기 때문에 역직렬화를 깨뜨린다는 점이다. <br>
해결책은 copyreg에 제공하는 함수에 버전 파라미터를 추가하여 버전에 따라서 GameState 생성자에 넘길 인수를 조작하는 것이다.
```py
def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        kwargs.pop('lives')
    return GameState(**kwargs)


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)
```

클래스의 이름이 변경되었을 때 pickle의 기능이 또다시 깨질 수 있다. <br>
클래스의 이름을 바꾸는 것은 매우 잦은 일이기 때문에 pickle을 사용할 경우 주의를 기울여야 한다. <br>
클래스의 이름이 변경되었을 때는 다음과 같이 다시 copyreg를 사용하여 해결할 수 있다.
```py
del GameState


class BatterGameState(object):
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic

def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        kwargs.pop('lives')
    return BatterGameState(**kwargs)


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)

copyreg.pickle(BatterGameState, pickle_game_state)
state_after = pickle.loads(serialized)
print(type(state_after))

>>>
<class '__main__.BatterGameState'>
```

## 정리
1. pickle은 서로 신뢰하는 프로그램 간에 객체를 직렬화, 역직렬화할 때 사용해야 한다.
2. pickle 모듈을 복잡하게 사용하려고 하면 제대로 동작하지 않을 수 있다.
3. pickle을 안정적으로 사용하려면 copyreg 내장 모듈을 함께 사용해야 한다.