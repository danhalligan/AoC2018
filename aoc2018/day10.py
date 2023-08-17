import re


def space2text(space):
    rs = [x["c"][1] for x in space]
    cs = [x["c"][0] for x in space]
    rows = []
    for x in range(min(rs), max(rs) + 1):
        row = []
        for y in range(min(cs), max(cs) + 1):
            val = "."
            for p in space:
                if p["c"] == (y, x):
                    val = "#"
                    break
            row += [val]
        rows += ["".join(row)]
    return "\n".join(rows)


def span(space):
    rs = [x["c"][1] for x in space]
    cs = [x["c"][0] for x in space]
    return max(rs) - min(rs)


def update(space):
    new = []
    for x in space:
        new += [{"c": (x["c"][0] + x["v"][0], x["c"][1] + x["v"][1]), "v": x["v"]}]
    return new


data = open("inputs/day10.txt").read().splitlines()
data = [list(map(int, re.findall(r"-*\d+", line))) for line in data]

space = [{"c": (x[0], x[1]), "v": (x[2], x[3])} for x in data]


def find_message(space):
    count = 0
    while True:
        old = span(space)
        updated = update(space)
        new = span(updated)
        if new > old:
            txt = space2text(space)
            break
        space = updated
        count += 1
    return txt, count


txt, count = find_message(space)


def part1():
    print(txt)


def part2():
    return count
