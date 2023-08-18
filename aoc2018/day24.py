import aoc2018.immune
import importlib

def part1():
    b = aoc2018.immune.Board("inputs/day24.txt")
    return b.play()["score"]


# I found the value manually.
# Slightly less than "43" boost leads to an untrapped stalemate (play continues
# to run indefinitely), making optimisation tough (without trapping this case)
def part2():
    for i in range(100):
        b = aoc2018.immune.Board("inputs/day24.txt")
        b.add_boost(i)
        res = b.play()
        if res["winner"] == "immune":
            return res["score"]
