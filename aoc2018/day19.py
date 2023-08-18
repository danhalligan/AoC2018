from aoc2018.day16 import functions, ints


def parse_line(line):
    fn, *codes = line.split(" ")
    codes = list(map(int, codes))
    return {"fn": fn, "a": codes[0], "b": codes[1], "c": codes[2]}


def parse_program(file):
    program = open(file).read().splitlines()
    ip = program[0]
    program = program[1:]
    program = [parse_line(line) for line in program]
    ip = ints(ip)[0]
    reg = [0] * 6
    return program, ip, reg


def part1():
    program, ip, reg = parse_program("inputs/day19.txt")
    fns = functions()
    while reg[ip] < len(program):
        inst = program[reg[ip]]
        reg[inst["c"]] = fns[inst["fn"]](reg, inst["a"], inst["b"])
        reg[ip] += 1
    return reg[0]


def part2():
    program, ip, reg = parse_program("inputs/day19.txt")
    fns = functions()
    reg[0] = 1

    while reg[ip] < len(program):
        inst = program[reg[ip]]
        # print(f"ip={reg[ip]}, {reg}", end=" ")
        # print(line, end=" ")
        reg[inst["c"]] = fns[inst["fn"]](reg, inst["a"], inst["b"])
        # print(f"{reg}")
        reg[ip] += 1
        if reg[ip] == 1:
            break

    # inspecting the code, it seems that this calculates the sum of the factors
    # of the big number in address 4!
    return sum(i for i in range(1, reg[4] + 1) if reg[4] % i == 0)
