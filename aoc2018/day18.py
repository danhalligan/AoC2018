from collections import defaultdict


def neighbours(i, j):
    return [
        (i - 1, j - 1),
        (i, j - 1),
        (i + 1, j - 1),
        (i - 1, j),
        (i + 1, j),
        (i - 1, j + 1),
        (i, j + 1),
        (i + 1, j + 1),
    ]


def print_board(b, r, c):
    for i in range(r):
        print(*[b[i, j] for j in range(c)], sep="")


def update(board):
    new_board = defaultdict(lambda: ".")
    for pos in list(board.keys()):
        new_board[pos] = board[pos]
        vals = [board[x] for x in neighbours(*pos)]
        if board[pos] == ".":
            if vals.count("|") >= 3:
                new_board[pos] = "|"
        if board[pos] == "|":
            if vals.count("#") >= 3:
                new_board[pos] = "#"
            else:
                new_board[pos] = "|"
        if board[pos] == "#":
            if vals.count("#") >= 1 and vals.count("|") >= 1:
                new_board[pos] = "#"
            else:
                new_board[pos] = "."
    return new_board


def dat():
    dat = open("inputs/day18.txt").read().splitlines()
    board = defaultdict(lambda: ".")
    for i in range(len(dat)):
        line = list(dat[i])
        for j in range(len(line)):
            board[i, j] = line[j]
    return board


def part1():
    board = dat()
    for i in range(10):
        board = update(board)

    vals = list(board.values())
    return vals.count("#") * vals.count("|")


def part2():
    values = list()
    board = dat()
    for i in range(1000):
        board = update(board)
        vals = list(board.values())
        values.append(vals.count("#") * vals.count("|"))
    # There is a burn in of 470, then repeating sections 471:526 inclusive
    # Therefore after n the value will be the same as (n-470) % 56 + 470
    # e.g.
    # n = 890
    # values[(n - 470) % 56 + 470] == values[n]
    n = 1000000000 - 1
    values[(n - 470) % 56 + 470]
