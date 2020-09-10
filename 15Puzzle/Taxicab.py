import math
import time
from heapq import heappush, heappop
goal = "0ABCDEFGHIJKLMNO"
size = 4


def mhd(s, g):
    return abs(s // size - g // size) + abs(s % size - g % size)


def taxicab(state):
    total = 0
    for a in range(1, len(state)):
        total += mhd(a, state.index(goal[a]))
    return total


def get_child_dir(state):
    (x, y) = get_coordinate(state.index("0"))
    move = {}
    children = {}
    if (x + 1) < size:
        move[get_index(x + 1, y)] = "DOWN"
    if (x - 1) >= 0:
        move[get_index(x - 1, y)] = "UP"
    if (y + 1) < size:
        move[get_index(x, y + 1)] = "RIGHT"
    if (y - 1) >= 0:
        move[get_index(x, y - 1)] = "LEFT"
    for key in move:
        children[swap(state, state.index("0"), key)] = move[key]
    return children


def get_coordinate(ind):
    x = ind // size
    y = ind % size
    return x, y


def get_index(x, y):
    index = 0
    index += size * x
    index += y
    return index


def swap(s, a, b):
    n = list(s)
    temp = n[a]
    n[a] = n[b]
    n[b] = temp
    return ''.join(n)


def path(state):
    heap = list()
    visited = set()
    heappush(heap, (taxicab(state), 0, state))
    while len(heap) > 0:
        v = heappop(heap)
        if v[2] in visited:
            continue
        visited.add(v[2])
        if v[2] == goal:
            return v[1]
        temp = get_child_dir(v[2])
        for a in temp:
            if temp[a] == "UP":
                (x, y) = get_coordinate(a.index("0"))
                moved = get_index(x + 1, y)
                goal_pos = goal.index(a[moved])
                if goal_pos // size >= a.index("0") // size:
                    heappush(heap, (v[0] + v[1] + 2, v[1] + 1, a))
                else:
                    heappush(heap, (v[0] + v[1], v[1] + 1, a))
            if temp[a] == "DOWN":
                (x, y) = get_coordinate(a.index("0"))
                moved = get_index(x - 1, y)
                goal_pos = goal.index(a[moved])
                if goal_pos // size <= a.index("0") // size:
                    heappush(heap, (v[0] + v[1] + 2, v[1] + 1, a))
                else:
                    heappush(heap, (v[0] + v[1], v[1] + 1, a))
            if temp[a] == "LEFT":
                (x, y) = get_coordinate(a.index("0"))
                moved = get_index(x, y + 1)
                goal_pos = goal.index(a[moved])
                if goal_pos % size >= a.index("0") % size:
                    heappush(heap, (v[0] + v[1] + 2, v[1] + 1, a))
                else:
                    heappush(heap, (v[0] + v[1], v[1] + 1, a))
            if temp[a] == "RIGHT":
                (x, y) = get_coordinate(a.index("0"))
                moved = get_index(x, y - 1)
                goal_pos = goal.index(a[moved])
                if goal_pos % size <= a.index("0") % size:
                    heappush(heap, (v[0] + +v[1] + 2, v[1] + 1, a))
                else:
                    heappush(heap, (v[0] + v[1], v[1] + 1, a))


file = open("ext.txt", "r")
for line in file:
    a = line.split()
    start = time.process_time()
    b = path(a[0])
    end = time.process_time()
    print(a[0] + " " + str(b) + " " + str(end - start))
    if b == 13:
        break
