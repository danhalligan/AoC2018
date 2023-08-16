import re
from functools import cache



@cache
def geologic_index(x, y, t1, t2, depth):
    if x == 0 and y == 0:
        return 0
    if x == t1 and y == t2:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    a = erosion_level(x - 1, y, t1, t2, depth)
    b = erosion_level(x, y - 1, t1, t2, depth)
    return a * b


def erosion_level(x, y, t1, t2, depth):
    return (geologic_index(x, y, t1, t2, depth) + depth) % 20183


def shape(x):
    if x == 0:
        return "."
    elif x == 1:
        return "="
    else:
        return "|"


lines = open("inputs/day22.txt").read().splitlines()
depth = int(re.findall("\d+", lines[0])[0])
target = [int(x) for x in re.findall("\d+", lines[1])]

# size = [16, 16]
# cave = {}
# for x in range(size[0]):
#     for y in range(size[1]):
#         cave[x, y] = erosion_level(x, y, target[0], target[1], depth)

# for y in range(size[0]):
#     print("".join(shape(cave[x, y] % 3) for x in range(size[1])))

sum(
    erosion_level(x, y, target[0], target[1], depth) % 3 
    for x in range(target[0] + 1) 
    for y in range(target[1] + 1)
)
