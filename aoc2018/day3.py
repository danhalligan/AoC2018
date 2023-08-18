from collections import defaultdict
import re


def data():
    dat = open("inputs/day03.txt", "r").read().splitlines()
    return [[int(y) for y in re.findall("\d+", x)] for x in dat]


def coverage():
    count = defaultdict(int)
    for d in data():
        for x1 in range(d[1], d[3] + d[1]):
            for y1 in range(d[2], d[2] + d[4]):
                count[x1, y1] += 1
    return count


def part1():
    return len([k for k, v in coverage().items() if v >= 2])


def overlap(d, overlaps):
    return sum(
        overlaps[x1, y1] >= 2
        for x1 in range(d[1], d[3] + d[1])
        for y1 in range(d[2], d[2] + d[4])
    )


def part2():
    ol = coverage()
    return [d for d in data() if overlap(d, ol) == 0][0][0]
