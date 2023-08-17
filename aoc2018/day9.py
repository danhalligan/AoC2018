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


# marbles(10, 1618) == 8317
# marbles(13, 7999) == 146373
# marbles(17, 1104) == 2764
# marbles(21, 6111) == 54718
# marbles(30, 5807) == 37305


def part1():
    return marbles(411, 71170)


def part2():
    return marbles(411, 7117000)


if __name__ == "__main__":
    print("Part1:", part1())
    print("Part2:", part2())
