import re
from collections import defaultdict
from math import prod


def time(x):
    return re.findall("\[(.+)\]", x)[0]


def guard(x):
    return int(re.findall("Guard #(\d+)", x)[0])


def minute(x):
    return int(re.findall("(\d+)\]", x)[0])


dat = open("inputs/day04.txt", "r").read().splitlines()
dat = dict([time(x), x] for x in dat)
sleep = defaultdict(int)
mins = defaultdict(lambda: defaultdict(int))
for x in sorted(dat.keys()):
    if "Guard" in dat[x]:
        g = guard(dat[x])
    else:
        if "asleep" in dat[x]:
            asleep = minute(dat[x])
        else:
            wake = minute(dat[x])
            for t in range(asleep, wake):
                mins[g][t] += 1
            sleep[g] += wake - asleep


def part1():
    g = max(sleep, key=sleep.get)
    m = max(mins[g], key=mins[g].get)
    return g * m


def maxminute(t, mins):
    m = dict([g, mins[g][t]] for g in mins)
    return {"g": max(m, key=m.get), "t": max(m.values()), "m": t}


def part2():
    r = [maxminute(t, mins) for t in range(60)]
    r = max(r, key=lambda x: x["t"])
    return r["g"] * r["m"]


if __name__ == "__main__":
    print("Part1:", part1())
    print("Part2:", part2())
