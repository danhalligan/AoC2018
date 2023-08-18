def parse_data(dat, i):
    nc, nm = dat[i : i + 2]
    i += 2
    children = list()
    for _ in range(nc):
        res, i = parse_data(dat, i)
        children += [res]
    return [{"m": dat[i : i + nm], "c": children}, i + nm]


def sum_metadata(x):
    return sum(x["m"]) + sum(sum_metadata(x) for x in x["c"])


def sum_metadata2(x):
    if len(x["c"]) == 0:
        return sum(x["m"])
    else:
        ind = [i - 1 for i in x["m"] if (i > 0 and i <= len(x["c"]))]
        return sum(sum_metadata2(x["c"][i]) for i in ind)


def parse_file(file):
    dat = open(file, "r").read().rstrip().split()
    dat = list(map(int, dat))
    x, _ = parse_data(dat, 0)
    return x


def part1():
    return sum_metadata(parse_file("inputs/day08.txt"))


def part2():
    return sum_metadata2(parse_file("inputs/day08.txt"))
