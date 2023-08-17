import re
from collections import defaultdict


def ints(x):
    return list(map(int, re.findall("\\d+", x)))


fns = {
    "addr": (lambda reg, a, b: reg[a] + reg[b]),
    "addi": (lambda reg, a, b: reg[a] + b),
    "mulr": (lambda reg, a, b: reg[a] * reg[b]),
    "muli": (lambda reg, a, b: reg[a] * b),
    "banr": (lambda reg, a, b: reg[a] & reg[b]),
    "bani": (lambda reg, a, b: reg[a] & b),
    "borr": (lambda reg, a, b: reg[a] | reg[b]),
    "bori": (lambda reg, a, b: reg[a] | b),
    "setr": (lambda reg, a, b: reg[a]),
    "seti": (lambda reg, a, b: a),
    "gtir": (lambda reg, a, b: 1 if a > reg[b] else 0),
    "gtri": (lambda reg, a, b: 1 if reg[a] > b else 0),
    "gtrr": (lambda reg, a, b: 1 if reg[a] > reg[b] else 0),
    "eqir": (lambda reg, a, b: 1 if a == reg[b] else 0),
    "eqri": (lambda reg, a, b: 1 if reg[a] == b else 0),
    "eqrr": (lambda reg, a, b: 1 if reg[a] == reg[b] else 0),
}


def parse_line(line):
    fn, *codes = line.split(" ")
    codes = list(map(int, codes))
    return {"fn": fn, "a": codes[0], "b": codes[1], "c": codes[2]}


program = open("inputs/day21.txt").read().splitlines()
ip = program[0]
program = program[1:]
program = [parse_line(line) for line in program]


# part 1.
# instruction 28 "eqrr 5 0 3" compares reg 5 to reg 0 (and sets reg 3 to 1/0 for true /false)
# this is the ONLY time reg 0 is used (which is the value we can manipulate)
# if we set reg 0 to the number that first appears in reg 5, then reg 3 will become 0
# we then execute "addr 3 4 4" (which adds reg 3 (value = 1) to reg 4 and stores in reg 4
# since reg 4 is out instruction pointer, adding 1 ends the program.
#
# Thus we need to find the first value in reg 5 to end the program fastest.
def part1():
    ip = ints(ip)[0]
    reg = [0] * 6
    while reg[ip] < len(program):
        inst = program[reg[ip]]
        if reg[ip] == 28:
            return reg[5]
        reg[inst["c"]] = fns[inst["fn"]](reg, inst["a"], inst["b"])
        reg[ip] += 1


# part 2
# the longest time will be found when the numbers cycle will be the value
# just before the values at reg 5 cycle around.
def part2():
    ip = ints(ip)[0]
    reg = [0] * 6
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
