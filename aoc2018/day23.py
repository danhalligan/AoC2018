import re
from itertools import product
from math import ceil


def md(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


def shrink(x, by):
    return [p // by for p in x[0:3]] + [ceil(x[3] / by)]


lines = open("inputs/day23.txt").read().splitlines()
dat = [list(map(int, re.findall("-*\\d+", line))) for line in lines]


def part1():
    sizes = [x[3] for x in dat]
    largest = sizes.index(max(sizes))
    return sum(md(dat[largest][0:3], x[0:3]) <= max(sizes) for x in dat)


# This works by shrinking down the boxes, and finding the best point
# and gradually shrinking by less and less, honing in on the best point
# I'm sure this is not guaranteed to work in all cases (and is sensitive
# to the size of area around our best point).
# I think the best is when there are 976 overlapping bots
def part2():
    best = [0, 0, 0]
    for power in range(25, -1, -1):
        fac = 2**power
        dats = [shrink(x, fac) for x in dat]
        points = [list(range(best[i] - 5, best[i] + 5, 1)) for i in range(3)]
        grid = list(product(*points))
        inrange = [sum(md(point, x[0:3]) <= x[3] for x in dats) for point in grid]
        mx = max(inrange)
        best = grid[inrange.index(mx)]
        # print(power, mx, best)
        if power == 0.0:
            return md((0, 0, 0), best)
        best = [x * 2 for x in best]
