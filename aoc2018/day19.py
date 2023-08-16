import re


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


def part1():
    program = open("inputs/day19.txt").read().splitlines()
    ip = program[0]
    program = program[1:]

    # run program
    ip = ints(ip)[0]
    reg = [0] * 6

    while reg[ip] < len(program):
        line = program[reg[ip]]
        # print(f"ip={reg[ip]}, {reg}", end=" ")
        # print(line, end=" ")
        fn, *codes = line.split(" ")
        codes = list(map(int, codes))
        reg[codes[2]] = fns[fn](reg, codes[0], codes[1])
        # print(f"{reg}")
        reg[ip] += 1
    return reg[0]


def part2():
    ip = ints(ip)[0]
    reg = [0] * 6
    reg[0] = 1

    while reg[ip] < len(program):
        line = program[reg[ip]]
        # print(f"ip={reg[ip]}, {reg}", end=" ")
        # print(line, end=" ")
        fn, *codes = line.split(" ")
        codes = list(map(int, codes))
        reg[codes[2]] = fns[fn](reg, codes[0], codes[1])
        # print(f"{reg}")
        reg[ip] += 1
        if reg[ip] == 1:
            break

    # inspecting the code, it seems that this calculates the sum of the factors
    # of the big number in address 4!
    return sum(i for i in range(1, reg[4] + 1) if reg[4] % i == 0)
