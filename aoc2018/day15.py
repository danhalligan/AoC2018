import aoc2018.goblins


def part1():
    cave = aoc2018.goblins.Cave("inputs/day15.txt")
    done = False
    while not done:
        done = cave.round(verbose=False)
    return str(cave.score())


def part2():
    cave = aoc2018.goblins.Cave("inputs/day15.txt", elf_attack=13)
    done = False
    while not done:
        done = cave.round2(verbose=False)
    return str(cave.score())
