import aoc2018.goblins
import importlib
importlib.reload(aoc2018.goblins)

x = [list(x) for x in open("tests/inputs/day15.txt").read().splitlines()]
cave = aoc2018.goblins.Cave(x)
# cave.print()
u = cave.units[0]
u.targets(cave)
u.target_open(cave)
u.destination(cave)
u.position = u.move(cave)

# cave.shortest_paths((1,1), (3,3))

paths = cave.dij((1,1))
end = (3,3)



list(recurse([], (2,3)))


for p in target_open(cave):
    
unit = x.units[0]
x.destination(unit)

cave.distance((1,1))

others = [u for u in x.units if unit != u]
taken = [u.position for u in others]
avail = [x.neighbours(u.position, taken) for u in others]
avail = sum(avail, [])
dist = [x.distance(p, taken).get(unit.position, 1000) for p in avail]
pos = [a for d, a in zip(dist, avail) if d == min(dist)]
dest = sorted(pos)[0]


for u in x.units:
    if unit != u:
        breakpoint()
        x.distance(u.position, taken)[unit.position]

x.distance(x.units[1].position, taken)[unit.position]


def round()
    for unit in sort(units, key = lambda x: x.pos):
