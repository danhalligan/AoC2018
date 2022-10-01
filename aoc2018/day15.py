from heapq import *

# store position as (column, row)
class Unit:
    def __init__(self, position):
        self.hit_points = 200
        self.attack_power = 3
        self.position = position
    
    def neighbours(self, cave):
        i, j = self.position
        coords = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        return [(i, j) for i, j in coords if cave[i,j] == '.']
    
    def move(self, grid):
        # from open squares - which is closest (avoiding walls)
        # find ALL shortest paths
        # if paths -- pick path
            # move 1 step
        return None
    
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

class Goblin(Unit):
    pass

class Elf(Unit):
    pass


class Cave:
    def __init__(self, array):
        self.units = []
        self.map = {}
        for r in range(len(array)):
            for c in range(len(array[r])):
                if array[r][c] == 'G':
                    self.units.append(Goblin((r,c)))
                    self.map[(r,c)] = '.'
                elif array[r][c] == 'E':
                    self.units.append(Elf((r,c)))
                    self.map[(r,c)] = '.'
                else:
                    self.map[(r,c)] = array[r][c]
    
    def neighbours(self, pos, taken):
        i, j = pos
        coords = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        return [(i, j) for i, j in coords if self.map[i,j] == '.' and (i,j) not in taken]
    
    # return shortest distance to a position
    def distance(self, pos, taken):
        scores = {pos: 0}
        queue = [(0, pos)]
        while len(queue) > 0:
            score, pos = heappop(queue)
            for nb in self.neighbours(pos, taken):
                new = score + 1
                if new < scores.get(nb, 100000):
                    scores[nb] = new
                    heappush(queue, (new, nb))
        return scores
    
    # return all shortest paths to a position
    def shortest_paths(self, pos, taken):
        pass
    
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
    
    def in_range(self, unit):
        pass
    
    def print():
        for r in range(len(cave)):
            s = ''
            for c in range(len(cave[r])):
                if (r,c) in x: s += str(x[r,c])
                else: s += cave[r][c]
            print(s)



x = [list(x) for x in open("tests/inputs/day15.txt").read().splitlines()]
x = Cave(x)
unit = x.units[0]
x.destination(unit)


others = [u for u in x.units if unit != u]
taken = [u.position for u in others]
avail = [x.neighbours(u.position, taken) for u in others]
avail = sum(avail, [])
dist = [x.distance(p, taken).get(unit.position, 1000) for p in avail]
pos = [a for d, a in zip(dist, avail) if d == min(dist)]
dest = sorted(pos)[0]


for u in x.units:
    if unit != u:
        breakpoint()
        x.distance(u.position, taken)[unit.position]

x.distance(x.units[1].position, taken)[unit.position]


def round()
    for unit in sort(units, key = lambda x: x.pos):
