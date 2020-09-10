from collections import deque
import time
size = 4
goal = "0ABCDEFGHIJKLMNO"


class Node:
    def __init__(self, state, path_length):
        self.path_length = path_length
        self.state = state

    def get_path_length(self):
        return self.path_length

    def get_state(self):
        # returns the string that represents the puzzle state
        return self.state


class KNode:
    def __init__(self, state):
        self.state = state
        self.depth = 0
        self.ancestors = set()


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


def path(state):
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


file = open("ext.txt", "r")
for line in file:
    a = line.split()
    print(a[0])
    try:
        start = time.process_time()
        length = path(a[0])
        end = time.process_time()
        print("BFS    " + str(length) + " " + str(end - start))
    except MemoryError as error:
        print("BFS Memory Error")
    start2 = time.process_time()
    length2 = iddfs(a[0], 80)
    end2 = time.process_time()
    print("ID-DFS " + str(length2) + " " + str(end2-start2))
