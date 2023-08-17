from collections import defaultdict

dat = open("inputs/day06.txt", "r").read().splitlines()
dat = [list(map(int, x.split(", "))) for x in dat]

x0 = min(x for x, y in dat)
x1 = max(x for x, y in dat)
y0 = min(y for x, y in dat)
y1 = max(y for x, y in dat)


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def closest(pad=0):
    r = defaultdict(int)
    for x in range(x0 - pad, x1 + pad):
        for y in range(y0 - pad, y1 + pad):
            d = [dist([x, y], p) for p in dat]
            m = min(d)
            if d.count(m) == 1:
                i = d.index(min(d))
                r[i] += 1
    return r


def part1():
    a = closest()
    b = closest(1)
    stable = [k for k in a.keys() if a[k] == b[k]]
    return max(a[k] for k in stable)


def part2():
    count = 0
    for x in range(x0, x1):
        for y in range(y0, y1):
            if sum(dist([x, y], p) for p in dat) < 10000:
                count += 1
    return count


if __name__ == "__main__":
    print("Part1:", part1())
    print("Part2:", part2())
