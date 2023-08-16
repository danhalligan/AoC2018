import re

def md(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


lines = open("inputs/day23.txt").read().splitlines()
dat = [list(map(int, re.findall("-*\\d+", line))) for line in lines]

sizes = [x[3] for x in dat]
largest = sizes.index(max(sizes))
sum(md(dat[largest][0:3], x[0:3]) <= max(sizes) for x in dat)

