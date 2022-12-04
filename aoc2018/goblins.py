from heapq import *

# store position as (column, row)
class Unit:
    def __init__(self, position):
        self.hit_points = 200
        self.attack_power = 3
        self.position = position

    def neighbours(self, cave):
        """Find valid positions (ignoring location of any units)"""
        i, j = self.position
        coords = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return [(i, j) for i, j in coords if cave.map[i, j] == "."]

    def open(self, cave):
        """Find open neighbouring positions (avoids units)"""
        return [p for p in self.neighbours(cave) if p not in cave.positions()]

    def targets(self, cave):
        """Find all targets"""
        return [u for u in cave.units if type(u) != type(self)]

    def target_open(self, cave):
        """Find open locations adjacent to all targets"""
        return sum([u.open(cave) for u in self.targets(cave)], [])

    def any_targets(self, cave):
        """Any targets left?"""
        return len(self.targets(cave) > 0)

    def in_range(self, cave):
        """Are we in range of a target?"""
        return any(self.position in u.neighbours(cave) for u in self.targets(cave))

    def destination(self, cave):
        """Choose open target to move to"""
        dists = cave.distance(self.position)
        dests = self.target_open(cave)
        dists = {k: v for k, v in dists.items() if k in dests}
        min_dist = min(dists.values())
        return sorted([k for k, v in dists.items() if v == min_dist])[0]

    def move(self, cave):
        """Move unit closer to nearest target along shortest path"""
        dest = self.destination(cave)
        paths = cave.shortest_paths(self.position, dest)
        moves = [x[0] for x in paths]
        u.position = sorted(moves)[0]

    def attack(self):
        # find all targets in range
        # find target with fewest hit points
        # deal damage
        return None

    def play(self):
        # identify targets
        # identify open squares adjacent to each target
        # if not in range and no open square in range: end
        # if in range -- attack
        # else -- move
        return None

    def code(self):
        return type(self).__name__[0]

    def __repr__(self):
        return f"{self.code()}{self.position}"


class Goblin(Unit):
    pass


class Elf(Unit):
    pass


class Cave:
    def __init__(self, array):
        """Create a new cave from input as an array"""
        self.units = []
        self.map = {}
        self.rows = len(array)
        self.cols = len(array[0])
        for r in range(len(array)):
            for c in range(len(array[r])):
                if array[r][c] == "G":
                    self.units.append(Goblin((r, c)))
                    self.map[(r, c)] = "."
                elif array[r][c] == "E":
                    self.units.append(Elf((r, c)))
                    self.map[(r, c)] = "."
                else:
                    self.map[(r, c)] = array[r][c]

    def open_positions(self):
        """All open positions in cave"""
        return [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if self.map[r, c] == "." and (r, c) not in self.positions()
        ]

    def neighbours(self, pos):
        """Open neighbours in cave"""
        i, j = pos
        coords = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return list(set(coords) & set(self.open_positions()))

    def dij(self, start):
        """Find all distance to every open position, retaining parent cells"""
        paths = {start: {"s": 0, "p": []}}
        queue = [(0, start)]
        while len(queue):
            score, pos = heappop(queue)
            for nb in self.neighbours(pos):
                new = score + 1
                scores = {p: x["s"] for p, x in paths.items()}
                if new < scores.get(nb, 100000):
                    paths[nb] = {"s": new, "p": [pos]}
                    heappush(queue, (new, nb))
                elif new == scores[nb]:
                    paths[nb] = {"s": new, "p": paths[nb]["p"] + [pos]}
        return paths

    def distance(self, pos):
        """Find shortest distance to every open position"""
        paths = self.dij(pos)
        return {p: x["s"] for p, x in paths.items()}

    def shortest_paths(self, start, end):
        """Find all shortest paths between two positions"""

        def recurse(path, pos):
            if len(paths[pos]["p"]):
                for prev in paths[pos]["p"]:
                    yield from recurse([pos] + path, prev)
            else:
                yield path

        paths = self.dij(start)
        return list(recurse([], end))

    # Find the destination target.
    # Targets defined as being a neighbouring square of an enemy unit
    # We find the target with the minimum distance
    # ties are broken by reading order
    def destination(self, unit):
        others = [u for u in self.units if unit != u]
        taken = [u.position for u in others]
        targets = [
            self.neighbours(u.position, taken)
            for u in others
            if type(others) != type(unit)
        ]
        targets = sum(targets, [])
        dist = [self.distance(p, taken).get(unit.position, 1000) for p in targets]
        pos = [a for d, a in zip(dist, targets) if d == min(dist)]
        return sorted(pos)[0]

    def positions(self):
        return [u.position for u in self.units]

    def in_range(self, unit):
        pass

    def print(self):
        for r in range(self.rows):
            s = ""
            for c in range(self.cols):
                if (r, c) in self.positions():
                    u = self.units[self.positions().index((r, c))]
                    s += u.code()
                else:
                    s += self.map[r, c]
            print(s)
