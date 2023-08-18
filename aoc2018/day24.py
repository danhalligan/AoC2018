import aoc2018.immune
import importlib

importlib.reload(aoc2018.immune)


def part1():
    b = aoc2018.immune.Board("inputs/day24.txt")
    return b.play()["score"]


# I found the value manually.
# Slightly less than "43" boost leads to an untrapped stalemate (play continues
# to run indefinitely), making optimisation tough (without trapping this case)
def part2():
    b = aoc2018.immune.Board("inputs/day24.txt")
    b.add_boost(43)
    b.play()["score"]
