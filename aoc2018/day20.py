from collections import defaultdict
from heapq import *


def new_node(d, p=None):
    return {"d": d, "p": p, "c": []}


def move(pos, dir):
    if dir == "S":
        return (pos[0], pos[1] + 1)
    elif dir == "E":
        return (pos[0] + 1, pos[1])
    elif dir == "W":
        return (pos[0] - 1, pos[1])
    elif dir == "N":
        return (pos[0], pos[1] - 1)


def build_graph(regex):
    regex = regex[1:-1]
    pos = (0, 0)
    graph = defaultdict(list)
    stack = [pos]

    for v in regex:
        if v == "(":
            stack += [pos]
        elif v == ")":
            pos = stack.pop()
        elif v == "|":
            pos = stack[-1]
        else:
            graph[pos] += [move(pos, v)]
            graph[move(pos, v)] += [pos]
            pos = move(pos, v)

    return graph


def print_rooms(graph):
    xs = [x[0] for x in graph.keys()]
    ys = [x[1] for x in graph.keys()]

    # Between rooms
    print("#", end="")
    for x in range(min(xs), max(xs) + 1):
        print("##", end="")
    print("")

    for y in range(min(ys), max(ys) + 1):
        print("#", end="")
        # Rooms
        for x in range(min(xs), max(xs)):
            v = "." if (x, y) in graph.keys() else "#"
            if x == 0 and y == 0:
                v = "X"
            print(v, end="")
            s = "|" if move((x, y), "E") in graph[(x, y)] else "#"
            print(s, end="")
        v = "." if (max(xs), y) in graph.keys() else "#"
        print(v, end="")
        print("#")

        # Between rooms
        print("#", end="")
        for x in range(min(xs), max(xs) + 1):
            v = "-" if move((x, y), "S") in graph[(x, y)] else "#"
            print(v, end="")
            print("#", end="")
        print("")


def dij(graph):
    scores = {(0, 0): 0}
    queue = [(0, (0, 0))]
    best = 100000
    while len(queue):
        score, pos = heappop(queue)
        for nb in graph[pos]:
            new = score + 1
            if new > best:
                break
            if new < scores.get(nb, 100000):
                scores[nb] = new
                heappush(queue, (new, nb))
    return scores


regex = open("inputs/day20.txt").read().splitlines()[0]
graph = build_graph(regex)
scores = dij(graph)


def part1():
    return max(scores.values())


def part2():
    return len([x for x in scores.values() if x >= 1000])
