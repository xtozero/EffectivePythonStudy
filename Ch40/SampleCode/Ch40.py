def coroutine():
    while True:
        received = yield
        print('Received:', received)

it = coroutine()
next(it)            # 코루틴 준비
it.send('First')
it.send('Second')


def minimize():
    current = yield
    while True:
        new = yield current
        current = min(new, current)

it = minimize()
next(it)
print(it.send(100))
print(it.send(50))
print(it.send(60))
print(it.send(40))
print(it.send(12))


def minimize():
    print('0')
    current = yield
    print('1')
    while True:
        print('2')
        new = yield current
        print('3')
        current = min(new, current)
        print('4')

it = minimize()
next(it)
it.send(100)
it.send(50)


# From https://github.com/bslatkin/effectivepython/blob/master/example_code/item_40.py
import logging
from pprint import pprint
from sys import stdout as STDOUT

# Example 4
ALIVE = '*'
EMPTY = '-'


# Example 5
from collections import namedtuple
Query = namedtuple('Query', ('y', 'x'))


# Example 6
def count_neighbors(y, x):
    n_ = yield Query(y + 1, x + 0)  # North
    ne = yield Query(y + 1, x + 1)  # Northeast
    # Define e_, se, s_, sw, w_, nw ...
    e_ = yield Query(y + 0, x + 1)  # East
    se = yield Query(y - 1, x + 1)  # Southeast
    s_ = yield Query(y - 1, x + 0)  # South
    sw = yield Query(y - 1, x - 1)  # Southwest
    w_ = yield Query(y + 0, x - 1)  # West
    nw = yield Query(y + 1, x - 1)  # Northwest
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


# Example 7
it = count_neighbors(10, 5)
q1 = next(it)                  # Get the first query
print('First yield: ', q1)
q2 = it.send(ALIVE)            # Send q1 state, get q2
print('Second yield:', q2)
q3 = it.send(ALIVE)            # Send q2 state, get q3
print('...')
q4 = it.send(EMPTY)
q5 = it.send(EMPTY)
q6 = it.send(EMPTY)
q7 = it.send(EMPTY)
q8 = it.send(EMPTY)
try:
    it.send(EMPTY)     # Send q8 state, retrieve count
except StopIteration as e:
    print('Count: ', e.value)  # Value from return statement


# Example 8
Transition = namedtuple('Transition', ('y', 'x', 'state'))


# Example 9
def game_logic(state, neighbors):
    pass

def step_cell(y, x):
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


# Example 10
def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY     # Die: Too few
        elif neighbors > 3:
            return EMPTY     # Die: Too many
    else:
        if neighbors == 3:
            return ALIVE     # Regenerate
    return state


# Example 11
it = step_cell(10, 5)
q0 = next(it)           # Initial location query
print('Me:      ', q0)
q1 = it.send(ALIVE)     # Send my status, get neighbor query
print('Q1:      ', q1)
print('...')
q2 = it.send(ALIVE)
q3 = it.send(ALIVE)
q4 = it.send(ALIVE)
q5 = it.send(ALIVE)
q6 = it.send(EMPTY)
q7 = it.send(EMPTY)
q8 = it.send(EMPTY)
t1 = it.send(EMPTY)     # Send for q8, get game decision
print('Outcome: ', t1)


# Example 12
TICK = object()

def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


# Example 13
class Grid(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output


# Example 14
    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state


# Example 15
def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:  # Must be a Transition
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny


# Example 16
grid = Grid(5, 9)
grid.assign(0, 3, ALIVE)
grid.assign(1, 4, ALIVE)
grid.assign(2, 2, ALIVE)
grid.assign(2, 3, ALIVE)
grid.assign(2, 4, ALIVE)
print(grid)


# Example 17
class ColumnPrinter(object):
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(row_count, len(data.splitlines()) + 1)
        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line
                if (i + 1) < len(self.columns):
                    rows[j] += ' | '
        return '\n'.join(rows)

columns = ColumnPrinter()
sim = simulate(grid.height, grid.width)
for i in range(5):
    columns.append(str(grid))
    grid = live_a_generation(grid, sim)

print(columns)


# Example 20
# This is for the introductory diagram
grid = Grid(5, 5)
grid.assign(1, 1, ALIVE)
grid.assign(2, 2, ALIVE)
grid.assign(2, 3, ALIVE)
grid.assign(3, 3, ALIVE)

columns = ColumnPrinter()
sim = simulate(grid.height, grid.width)
for i in range(5):
    columns.append(str(grid))
    grid = live_a_generation(grid, sim)

print(columns)