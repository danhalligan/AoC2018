from collections import defaultdict
from string import ascii_uppercase

dat = open("inputs/day07.txt", "r").read().splitlines()
dat = [[x.split()[i] for i in [1, 7]] for x in dat]

fmap = defaultdict(list)
rmap = defaultdict(list)
for x in dat:
    fmap[x[0]] += [x[1]]
    rmap[x[1]] += [x[0]]


def part1():
    done = list()
    available = sorted(x for x in fmap.keys() if len(rmap[x]) == 0)
    while len(available) > 0:
        done += available.pop(0)
        available += [x for x in fmap[done[-1]] if set(rmap[x]).issubset(done)]
        available = sorted(available)
    return "".join(done)


def part2():
    times = dict(zip(ascii_uppercase, range(1, 27)))
    paused = list()
    done = list()
    tottime = 0
    working = sorted(x for x in fmap.keys() if len(rmap[x]) == 0)
    working = dict([x, times[x] + 60] for x in working)

    while len(working) > 0:
        done += min(working, key=working.get)
        time = working.pop(done[-1])
        tottime += time
        for x in working:
            working[x] -= time
        paused += [x for x in fmap[done[-1]] if set(rmap[x]).issubset(done)]
        paused = sorted(paused)
        toadd = paused[: min(5 - len(working), len(paused))]
        paused = sorted(set(paused) - set(toadd))
        for x in toadd:
            working[x] = times[x] + 60

    return tottime
