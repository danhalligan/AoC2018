dat = open("inputs/day08.txt", "r").read().rstrip().split()
dat = list(map(int, dat))

# dat = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]


def parse_data(i):
    nc, nm = dat[i : i + 2]
    i += 2
    children = list()
    for _ in range(nc):
        res, i = parse_data(i)
        children += [res]
    return [{"m": dat[i : i + nm], "c": children}, i + nm]


x, i = parse_data(0)


def sum_metadata(x):
    return sum(x["m"]) + sum(sum_metadata(x) for x in x["c"])


def sum_metadata2(x):
    if len(x["c"]) == 0:
        return sum(x["m"])
    else:
        ind = [i - 1 for i in x["m"] if (i > 0 and i <= len(x["c"]))]
        return sum(sum_metadata2(x["c"][i]) for i in ind)


def part1():
    return sum_metadata(x)


def part2():
    return sum_metadata2(x)


if __name__ == "__main__":
    print("Part1:", part1())
    print("Part2:", part2())
