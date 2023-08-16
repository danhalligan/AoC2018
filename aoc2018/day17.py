import numpy as np


def build_map(file):
    dat = open(file).read().splitlines()
    ranges = {"x": [100000, 0], "y": [100000, 0]}
    for vein in dat:
        a, b = vein.split(", ")
        c1, v = a.split("=")
        ranges[c1][0] = min(ranges[c1][0], int(v))
        ranges[c1][1] = max(ranges[c1][1], int(v))
        c2, r = b.split("=")
        r = r.split("..")
        ranges[c2][0] = min(ranges[c2][0], int(r[0]))
        ranges[c2][1] = max(ranges[c2][1], int(r[1]))
    ground = np.full([ranges["x"][1] + 2, ranges["y"][1] + 2], ".", dtype=str)
    for vein in dat:
        a, b = vein.split(", ")
        c1, v = a.split("=")
        c2, r = b.split("=")
        r = r.split("..")
        if c1 == "x":
            ground[int(v), int(r[0]) : int(r[1]) + 1] = "#"
        else:
            ground[int(r[0]) : int(r[1]) + 1, int(v)] = "#"
    ground[(500, 0)] = "+"
    return ground


def print_map(g, xmin=0, ymax=100000):
    for col in range(min(g.shape[1], ymax)):
        row = [x for x in g[xmin:, col]]
        print("".join(row))


def move(pos, dir):
    if dir == "v":
        return (pos[0], pos[1] + 1)
    elif dir == ">":
        return (pos[0] + 1, pos[1])
    elif dir == "<":
        return (pos[0] - 1, pos[1])
    elif dir == "^":
        return (pos[0], pos[1] - 1)


def find_end(pos, g, dir):
    while not (g[pos] == "#" or g[move(pos, "v")] in "|."):
        pos = move(pos, dir)
    return pos


def fill_intermediates(left, right, g, x):
    for i in range(left[0] + 1, right[0]):
        g[(i, left[1])] = x


def solve(g):
    # Initiate a source
    queue = [(np.argmax(g[:, 0] == "+"), 0)]
    # Loop until queue empty
    while queue:
        queue = sorted(queue, key=lambda x: x[1])
        pos = queue.pop()
        g[pos] = "|"
        if pos[1] >= g.shape[1] - 1:
            continue
        if g[move(pos, "v")] == ".":
            # if cell down is vacant
            # fill downward with sources until not '.'
            queue.append(pos)
            while move(pos, "v")[1] < g.shape[1] and g[move(pos, "v")] == ".":
                pos = move(pos, "v")
                g[pos] = "|"
                queue.append(pos)
        elif g[move(pos, "v")] in "#~":
            # if cell down is wall or standing water below
            # look left /right for the "end" of the row
            lend = find_end(pos, g, "<")
            rend = find_end(pos, g, ">")
            if g[lend] == "#" and g[rend] == "#":
                fill_intermediates(lend, rend, g, "~")
            else:
                fill_intermediates(lend, rend, g, "|")
                if g[lend] == ".":
                    queue.append(lend)
                if g[rend] == ".":
                    queue.append(rend)
        elif g[move(pos, "v")] in "|" or pos[1] >= g.shape[1] - 1:
            g[pos] = "|"
            continue
    return g


def trim_map(g):
    ind = np.argwhere([np.any(g[:, i] == "#") for i in range(g.shape[1])])
    start = int(ind[0])
    end = int(ind[-1]) + 1
    return g[:, start:end]


def part1():
    g = build_map("inputs/day17.txt")
    g = solve(g)
    g = trim_map(g)
    return sum(sum(g == "|")) + sum(sum(g == "~"))


def part2():
    g = build_map("inputs/day17.txt")
    g = solve(g)
    g = trim_map(g)
    return sum(sum(g == "~"))
