from itertools import product


def power(p, serial):
    x, y = p
    rack_id = x + 10
    power = str((rack_id * y + serial) * rack_id)
    return int(power[-3]) - 5


# power((3,5), 8)
# power((122,79), 57)
# power((217,196), 39)
# power((101,153), 71)


def calc_grid(serial):
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[x, y] = power((x, y), serial)
    return grid


def max_power(grid, size=3):
    best = -10000
    end = 300 - size + 2
    for x in range(1, end):
        for y in range(1, end):
            pos = list(product(range(x, x + size), range(y, y + size)))
            tot = sum(grid[p] for p in pos)
            if tot > best:
                best = tot
                position = (x, y)
    return best, position


def part1():
    grid = calc_grid(6878)
    power, coord = max_power(grid)
    return str(coord[0]) + "," + str(coord[1])


def part2(stop=20):
    grid = calc_grid(6878)
    best = -10000
    for size in range(1, stop):
        tot, coord = max_power(grid, size)
        if tot > best:
            best = tot
            result = str(coord[0]) + "," + str(coord[1]) + "," + str(size)
            # print(tot, result)
    return result


if __name__ == "__main__":
    print("Part1:", part1())
    print("Part2:", part2(20))
