import time
import sys
import random
from collections import deque
from heapq import heappush, heappop

goal = "0ABCDEFGHIJKLMNO"
size = 4
ref = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10, "K": 11, "L": 12, "M": 13,
       "N": 14, "O": 15}


class Node:
    def __init__(self, state, path_length):
        self.path_length = path_length
        self.state = state

    def get_path_length(self):
        return self.path_length

    def get_state(self):
        return self.state


class KNode:
    def __init__(self, state):
        self.state = state
        self.depth = 0
        self.ancestors = set()


def mhd(s, g):
    return abs(s // size - g // size) + abs(s % size - g % size)


def taxicab(state):
    total = 0
    for a in range(0, len(state)):
        if state[a] == "0":
            continue
        total += mhd(a, ref[state[a]])
    return total


def get_children(state):
    (x, y) = get_coordinate(state)
    move = []
    children = []
    if (x + 1) < size:
        move.append(get_index(x + 1, y))
    if (x - 1) >= 0:
        move.append(get_index(x - 1, y))
    if (y + 1) < size:
        move.append(get_index(x, y + 1))
    if (y - 1) >= 0:
        move.append(get_index(x, y - 1))
    for a in range(0, len(move)):
        children.append(swap(state, state.index("0"), move[a]))
    return children


def get_coordinate(state):
    index = state.index("0")
    x = index // size
    y = index % size
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


def bfs(state):
    start = Node(state, 0)
    fringe = deque()
    fringe.appendleft(start)
    visited = set()
    visited.add(start.get_state())
    while len(fringe) != 0:
        v = fringe.pop()
        if v.get_state() == goal:
            return v.get_path_length()
        c = get_children(v.get_state())
        temp = []
        for e in c:
            add = Node(e, v.get_path_length() + 1)
            temp.append(add)
        for a in range(0, len(c)):
            if temp[a].get_state() not in visited:
                fringe.appendleft(temp[a])
                visited.add(temp[a].get_state())


def kdfs(starting, k):
    state = KNode(starting)
    fringe = list()
    fringe.append(state)
    while len(fringe) != 0:
        v = fringe.pop()
        if v.state == goal:
            return v.depth
        if v.depth < k:
            for c in get_children(v.state):
                if c not in v.ancestors:
                    child = KNode(c)
                    child.depth = v.depth + 1
                    child.ancestors = v.ancestors.union(c)
                    fringe.append(child)
    return None


def iddfs(start, max):
    for k in range(1, max + 1):
        sol = kdfs(start, k)
        if sol is not None:
            return sol
    return None


def a_star(state):
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
        for a in get_children(v[2]):
            heappush(heap, (taxicab(a) + v[1] + 1, v[1] + 1, a))


def a_star_tie(state):
    heap = list()
    visited = set()
    heappush(heap, (taxicab(state), random.uniform(0.0, 1.0), 0, state))
    while len(heap) > 0:
        v = heappop(heap)
        if v[3] in visited:
            continue
        visited.add(v[3])
        if v[3] == goal:
            return v[2]
        for a in get_children(v[3]):
            heappush(heap, (taxicab(a) + v[2] + 1, random.uniform(0.0, 1.0), v[2] + 1, a))


def a_star_multiplier(state, m):
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
        for a in get_children(v[2]):
            heappush(heap, (taxicab(a) + m * (v[1] + 1), v[1] + 1, a))


file = open(sys.argv[1], "r")
for line in file:
    a = line.split()
    if a[0] == "B" or a[0] == "!":
        start = time.perf_counter()
        p = bfs(a[1])
        end = time.perf_counter()
        print(str(p) + " BFS " + str(end - start))
    if a[0] == "I" or a[0] == "!":
        start = time.perf_counter()
        p = iddfs(a[1], 80)
        end = time.perf_counter()
        print(str(p) + " ID-DFS " + str(end - start))
    if a[0] == "2" or a[0] == "!":
        print("Bidirectional BFS was not implemented")
    if a[0] == "A" or a[0] == "!":
        start = time.perf_counter()
        p = a_star(a[1])
        end = time.perf_counter()
        print(str(p) + " A* " + str(end - start))
    if a[0] == "7" or a[0] == "!":
        for b in range(0, 3):
            start = time.perf_counter()
            p = a_star_multiplier(a[1], .7)
            end = time.perf_counter()
            print(str(p) + " A* Estimate " + str(end - start))
