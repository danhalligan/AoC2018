from heapq import *
from termcolor import colored


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
        return [p for p in self.neighbours(cave) if p not in cave.positions_alive()]

    def targets(self, cave):
        """Find all targets"""
        return [u for u in cave.units if type(u) != type(self) and u.alive()]

    def target_open(self, cave):
        """Find open locations adjacent to all targets"""
        return sum([u.open(cave) for u in self.targets(cave)], [])

    def any_targets(self, cave):
        """Any targets left?"""
        return len(self.targets(cave)) > 0

    def in_range(self, cave):
        """List of in range targets"""
        return [u for u in self.targets(cave) if self.position in u.neighbours(cave)]

    def alive(self):
        return self.hit_points > 0

    def move(self, cave, verbose=False):
        """Move unit closer to nearest target along shortest path"""
        dests = self.target_open(cave)
        paths = cave.dij(self.position, dests)
        dists = {p: x["s"] for p, x in paths.items()}
        dists = {k: v for k, v in dists.items() if k in dests}
        if not len(dists):
            return None
        min_dist = min(dists.values())
        dest = sorted([k for k, v in dists.items() if v == min_dist])[0]

        paths = cave.shortest_paths(self.position, dest, paths)
        moves = [x[0] for x in paths]
        if verbose:
            print(f"Moving {self} to {sorted(moves)[0]}")
        self.position = sorted(moves)[0]

    def attack(self, cave):
        # find all targets in range
        avail = self.in_range(cave)

        # find target with fewest hit points (breaking ties as required)
        hp = min(x.hit_points for x in avail)
        avail = [x for x in avail if x.hit_points == hp]
        target = sorted(avail, key=lambda x: x.position)[0]

        # deal damage
        target.hit_points -= self.attack_power

    def play(self, cave, verbose=False):
        if verbose:
            print(f"Targets: {self.targets(cave)}")
        if not self.any_targets(cave):
            return False
        if verbose:
            print(f"In range: {self.in_range(cave)}")
        if not len(self.in_range(cave)):
            self.move(cave, verbose=verbose)
        if len(self.in_range(cave)):
            self.attack(cave)
        return True

    def __repr__(self):
        return f"{self.code()}{self.position}:{self.hit_points}"


class Goblin(Unit):
    def code(self):
        return colored("G", "green")

    pass


class Elf(Unit):
    def __init__(self, position, attack_power=3):
        self.hit_points = 200
        self.attack_power = attack_power
        self.position = position

    def code(self):
        return colored("E", "red")

    pass


class Cave:
    def __init__(self, file, elf_attack=3):
        array = [list(x) for x in open(file).read().splitlines()]
        """Create a new cave from input as an array"""
        self.units = []
        self.map = {}
        self.rows = len(array)
        self.cols = len(array[0])
        self.round_count = 0
        for r in range(len(array)):
            for c in range(len(array[r])):
                if array[r][c] == "G":
                    self.units.append(Goblin((r, c)))
                    self.map[(r, c)] = "."
                elif array[r][c] == "E":
                    self.units.append(Elf((r, c), attack_power=elf_attack))
                    self.map[(r, c)] = "."
                else:
                    self.map[(r, c)] = array[r][c]

    def positions(self):
        return [u.position for u in self.units]

    def positions_alive(self):
        return [u.position for u in self.units if u.alive()]

    def positions_open(self):
        """All open positions in cave"""
        return [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if self.map[r, c] == "." and (r, c) not in self.positions_alive()
        ]

    def neighbours(self, pos):
        """Open neighbours in cave"""
        i, j = pos
        coords = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return list(set(coords) & set(self.positions_open()))

    def dij(self, start, dests):
        """Find all distance to every open position, retaining parent cells"""
        paths = {start: {"s": 0, "p": []}}
        queue = [(0, start)]
        best = 100000
        while len(queue):
            score, pos = heappop(queue)
            for nb in self.neighbours(pos):
                new = score + 1
                if new > best:
                    break
                scores = {p: x["s"] for p, x in paths.items()}
                if new < scores.get(nb, 100000):
                    paths[nb] = {"s": new, "p": [pos]}
                    heappush(queue, (new, nb))
                elif new == scores[nb]:
                    paths[nb] = {"s": new, "p": paths[nb]["p"] + [pos]}
                if nb in dests:
                    best = min(best, new)
        return paths

    def shortest_paths(self, start, end, paths):
        """Find all shortest paths between two positions"""

        def recurse(path, pos):
            if len(paths[pos]["p"]):
                for prev in paths[pos]["p"]:
                    yield from recurse([pos] + path, prev)
            else:
                yield path

        return list(recurse([], end))

    def print(self):
        for r in range(self.rows):
            s = ""
            for c in range(self.cols):
                if (r, c) in self.positions():
                    u = self.units[self.positions().index((r, c))]
                    if u.alive():
                        s += u.code()
                    else:
                        s += self.map[r, c]
                else:
                    s += self.map[r, c]
            print(s)

    def score(self):
        return sum(x.hit_points for x in self.units if x.alive()) * self.round_count

    def round(self, verbose=False):
        for u in self.units:
            if u.alive():
                success = u.play(self)
                if not success:
                    return True
        self.units = [x for x in self.units if x.alive()]
        self.units = sorted(self.units, key=lambda x: x.position)
        if verbose:
            self.print()
            print(self.units)
            print()
        self.round_count += 1
        return False

    def round2(self, verbose=False):
        for u in self.units:
            if u.alive():
                success = u.play(self)
                if not success:
                    return True
            else:
                if type(u).__name__ == "Elf":
                    print("Elf died!")
                    return True
        self.units = [x for x in self.units if x.alive()]
        self.units = sorted(self.units, key=lambda x: x.position)
        if verbose:
            self.print()
            print(self.units)
            print()
        self.round_count += 1
        return False
