import re
import sys

from functools import cache
from heapq import *


sys.setrecursionlimit(10000)


@cache
def geologic_index(x, y, t1, t2, depth):
    if x == 0 and y == 0:
        return 0
    if x == t1 and y == t2:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    a = erosion_level(x - 1, y, t1, t2, depth)
    b = erosion_level(x, y - 1, t1, t2, depth)
    return a * b


@cache
def erosion_level(x, y, t1, t2, depth):
    return (geologic_index(x, y, t1, t2, depth) + depth) % 20183


@cache
def terrain(pos):
    return erosion_level(pos[0], pos[1], target[0], target[1], depth) % 3


def moves(pos):
    out = [
        (pos[0], pos[1] + 1),
        (pos[0], pos[1] - 1),
        (pos[0] + 1, pos[1]),
        (pos[0] - 1, pos[1]),
    ]
    return [x for x in out if x[0] >= 0 and x[1] >= 0]


lines = open("inputs/day22.txt").read().splitlines()
depth = int(re.findall("\d+", lines[0])[0])
target = tuple([int(x) for x in re.findall("\d+", lines[1])])

# size = [16, 16]
# cave = {}
# for x in range(size[0]):
#     for y in range(size[1]):
#         cave[x, y] = erosion_level(x, y, target[0], target[1], depth)

# for y in range(size[0]):
#     print("".join([".", "=", "|"][cave[x, y] % 3] for x in range(size[1])))


def part1():
    return sum(
        terrain((x, y)) for x in range(target[0] + 1) for y in range(target[1] + 1)
    )


# Moving to an adjacent region takes one minute
# You can change if your new equipment would be valid for your current region
# Switching to using the climbing gear, torch, or neither always takes seven minutes
# Once you reach the target, you need the torch equipped


def part2():
    # tool options
    options = [set(["C", "T"]), set(["C", "-"]), set(["T", "-"])]

    start = (0, 0)
    queue = []  # queue items are (time, position, equipment)
    heappush(queue, (0, start, "T"))
    seen = {}
    best = 5000

    while queue:
        time, pos, eq = heappop(queue)
        if pos == target and eq == "T" and time < best:
            best = time
        if time > best or ((pos, eq) in seen and time >= seen[(pos, eq)]):
            continue
        seen[(pos, eq)] = time
        tc = terrain(pos)

        # We can move position (if tool is valid)
        for npos in moves(pos):
            if eq in options[terrain(npos)]:
                heappush(queue, (time + 1, npos, eq))

        # Or we can change tool if valid in our current terrain
        for neq in options[tc].difference(eq):
            heappush(queue, (time + 7, pos, neq))

    return best
