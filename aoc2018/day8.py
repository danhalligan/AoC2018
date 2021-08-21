dat = open("inputs/day08.txt", "r").read().rstrip().split()
dat = list(map(int, dat))

d = dict()

children = dat.pop(0)
metadata = dat.pop(0)
