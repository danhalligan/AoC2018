from itertools import accumulate, cycle


def data():
    dat = open("inputs/day01.txt", "r").read().splitlines()
    return [int(x) for x in dat]


def part1():
    return sum(data())


def part2():
    seen = set()
    for f in accumulate(cycle(data())):
        if f in seen:
            return f
        seen.add(f)
