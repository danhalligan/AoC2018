from collections import deque, defaultdict


def marbles(players, last_marble):
    marble = 0
    player = 0
    circle = deque()
    scores = defaultdict(int)
    while True:
        if marble > 0 and marble % 23 == 0:
            scores[player] += marble
            circle.rotate(7)
            scores[player] += circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
        if marble == last_marble:
            break
        marble += 1
        player = (player + 1) % players
    return max(scores.values())


def part1():
    return marbles(411, 71170)


def part2():
    return marbles(411, 7117000)
