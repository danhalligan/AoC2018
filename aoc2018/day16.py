import re


def functions():
    return {
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


def ints(x):
    return list(map(int, re.findall("\\d+", x)))


def testfn(fn, sample):
    fns = functions()
    sample = [ints(x) for x in sample]
    reg = sample[0]
    reg[sample[1][3]] = fns[fn](reg, sample[1][1], sample[1][2])
    return reg == sample[2]


def behaves_as(sample, poss=functions().keys()):
    return [fn for fn in poss if testfn(fn, sample)]


def parse_input(file):
    dat = open(file).read()
    samples, program = dat.split("\n\n\n\n")
    program = program.split("\n")
    samples = [x.split("\n") for x in samples.split("\n\n")]
    return samples, program


def part1():
    samples, _ = parse_input("inputs/day16.txt")
    return sum(len(behaves_as(x)) >= 3 for x in samples)


def part2():
    samples, program = parse_input("inputs/day16.txt")
    fns = functions()

    # gather evidence
    poss = {k: list(fns.keys()) for k in range(len(fns))}
    for sample in samples:
        fni = ints(sample[1])[0]
        opt = behaves_as(sample, poss[fni])
        poss[fni] = list(set(poss[fni]) & set(opt))

    # prune
    while max(len(x) for x in poss.values()) > 1:
        for fni in range(16):
            if len(poss[fni]) == 1:
                for i in range(16):
                    if i != fni and poss[fni][0] in poss[i]:
                        poss[i].remove(poss[fni][0])

    # run program
    reg = [0] * 4
    for line in program:
        line = ints(line)
        reg[line[3]] = fns[poss[line[0]][0]](reg, line[1], line[2])

    return reg[0]
