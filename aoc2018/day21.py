import re
from collections import defaultdict
from aoc2018.day16 import functions
from aoc2018.day19 import parse_program


# part 1.
# instruction 28 "eqrr 5 0 3" compares reg 5 to reg 0 (and sets reg 3 to 1/0 for true /false)
# this is the ONLY time reg 0 is used (which is the value we can manipulate)
# if we set reg 0 to the number that first appears in reg 5, then reg 3 will become 0
# we then execute "addr 3 4 4" (which adds reg 3 (value = 1) to reg 4 and stores in reg 4
# since reg 4 is out instruction pointer, adding 1 ends the program.
#
# Thus we need to find the first value in reg 5 to end the program fastest.
def part1():
    program, ip, reg = parse_program("inputs/day21.txt")
    fns = functions()
    while reg[ip] < len(program):
        inst = program[reg[ip]]
        if reg[ip] == 28:
            return reg[5]
        reg[inst["c"]] = fns[inst["fn"]](reg, inst["a"], inst["b"])
        reg[ip] += 1


# part 2
# the longest time will be found when the numbers cycle will be the value
# just before the values at reg 5 cycle around.
# Take quite a long time!
def part2():
    program, ip, reg = parse_program("inputs/day21.txt")
    fns = functions()
    vals = defaultdict(int)
    trail = 0
    while reg[ip] < len(program):
        inst = program[reg[ip]]
        if reg[ip] == 28:
            vals[reg[5]] += 1
            if max(vals.values()) == 2:
                return trail
            trail = reg[5]
        reg[inst["c"]] = fns[inst["fn"]](reg, inst["a"], inst["b"])
        reg[ip] += 1
