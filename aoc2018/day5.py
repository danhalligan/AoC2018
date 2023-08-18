import re
from string import ascii_lowercase as lc
from string import ascii_uppercase as uc

polymer = open("inputs/day05.txt", "r").read().rstrip()


def react(polymer):
    pairs = list(zip(lc, uc)) + list(zip(uc, lc))
    patterns = ["".join(x) for x in pairs]
    l2 = len(polymer)
    l1 = l2 + 1
    while l1 != l2:
        l1 = l2
        for p in patterns:
            polymer = re.sub(p, "", polymer)
        l2 = len(polymer)
    return polymer


def part1():
    return len(react(polymer))


def fix_and_react(polymer, l):
    fixed = re.sub(l, "", polymer, flags=re.IGNORECASE)
    return react(fixed)


def part2():
    return min(len(fix_and_react(polymer, l)) for l in lc)
