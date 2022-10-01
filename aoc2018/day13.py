import numpy as np

class Car:
    def __init__(self, pos, shape):
        self.pos = pos
        self.shape = shape
        self.dir = 'L'
    
    def move(self):
        s = self.shape
        p = self.pos
        if   s == '>': p = (p[0],   p[1]+1)
        elif s == 'v': p = (p[0]+1, p[1])
        elif s == '<': p = (p[0],   p[1]-1)
        elif s == '^': p = (p[0]-1, p[1])
        self.pos = p
    
    def turn(self, track):
        p = self.pos
        s = self.shape
        d = self.dir
        # turn
        turn = {
            'L': {'>':'^', '^':'<', '<':'v', 'v':'>'},
            'R': {'>':'v', '^':'>', '<':'^', 'v':'<'}
        }
        if track[p] == '\\':
            if s == '>' or s == '<':
                s = turn['R'][s]
            else:
                s = turn['L'][s]
        elif track[p] == '/':
            if s == '^' or s == 'v':
                s = turn['R'][s]
            else:
                s = turn['L'][s]
        elif track[p] == '+':
            if not d == 'S': 
                s = turn[d][s]
            self.dir = {'L':'S', 'S':'R', 'R':'L'}[d]
        self.shape = s
        self.pos = p
    
    def update(self, track):
        self.move()
        self.turn(track)


def data():
    x = np.array([list(x) for x in open("inputs/day13.txt").read().splitlines()])
    cars = []
    for r,c in np.ndindex(x.shape):
        if x[r,c] in ['>', '^', '<', 'v']:
            cars.append(Car((r,c), x[r,c]))
            x[r,c] = {'>':'-', '^':'|', '<':'-', 'v':'|'}[x[r,c]]
    return x, cars


def update(cars, track):
    cars = sorted(cars, key=lambda x: x.pos)
    crash = None
    todrop = []
    for i, c in enumerate(cars):
        c.update(track)
        if sum(c.pos == c2.pos for c2 in cars) > 1:
            crash = c.pos
            todrop += [i for i, c2 in enumerate(cars) if c2.pos == c.pos]
    if crash:
        cars = [c for i, c in enumerate(cars) if not i in todrop]
    return cars, crash


def print_map(x, cars):
    x = x.copy()
    for c in cars:
        x[c['p']] = c['s']
    for line in x:
        print(''.join(line))
    

def part1():
    track, cars = data()
    crash = None
    while not crash:
        cars, crash = update(cars, track)
    print("Part1: " + str(crash[1]) + "," + str(crash[0]))

def part2():
    track, cars = data()
    crash = None
    while len(cars) >= 2:
        cars, crash = update(cars, track)
    print("Part2: " + str(cars[0].pos[1]) + "," + str(cars[0].pos[0]))

