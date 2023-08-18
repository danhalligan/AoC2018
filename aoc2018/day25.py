def md(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


# this is horribly inefficient!
def find_set(x):
    s = [x[0]]
    x = x[1:]
    dists = [min(md(a, b) for b in s) for a in x]
    while any(x <= 3 for x in dists):
        s += [x[i] for i in range(len(dists)) if dists[i] <= 3]
        x = [x[i] for i in range(len(dists)) if dists[i] > 3]
        dists = [min(md(a, b) for b in s) for a in x]
    return s, x


def part1():
    lines = open("inputs/day25.txt").read().splitlines()
    dat = [list(map(int, line.split(","))) for line in lines]
    count = 0
    while len(dat):
        count += 1
        s, dat = find_set(dat)
    return count
