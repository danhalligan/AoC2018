from itertools import accumulate, cycle

dat = open("inputs/day01.txt", "r").read().splitlines()
dat = [int(x) for x in dat]

def part1():
    return sum(dat)

def part2():
    seen = set()
    for f in accumulate(cycle(dat)):
        if f in seen: return f
        seen.add(f)

if __name__ == "__main__":
    print("Part1:", part1())
    print("Part2:", part2())
