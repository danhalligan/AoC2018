from collections import Counter


def data():
    return open("inputs/day02.txt", "r").read().splitlines()


def part1():
    two, three = 0, 0
    for x in data():
        c = Counter(x)
        if 2 in c.values():
            two += 1
        if 3 in c.values():
            three += 1
    return two * three


def find_diff(dat):
    for s1 in data():
        for s2 in data():
            d = sum(x != y for x, y in zip(s1, s2))
            if d == 1:
                return s1, s2


def part2():
    for s1 in data():
        z = find_diff(data())
        return "".join(x for x, y in zip(*z) if x == y)
