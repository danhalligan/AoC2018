from collections import defaultdict

initial, notes = open("inputs/day12.txt").read().split("\n\n")
initial = initial[15:]
notes = [x.split(" => ") for x in notes.split("\n")]

pots = defaultdict(lambda: '.', [i for i in enumerate(initial)])

for c in range(20):
    print(len([x for x in pots.items() if x[1] == '#']))
    new = defaultdict(lambda: '.')
    v = list(pots.keys())
    for i in range(min(v)-5, max(v) + 5):
        curr = ''.join([pots[i] for i in range(i-2, i+3)])
        for note in notes:
            if note[0] == curr: new[i] = note[1]
    pots = new

sum(x[0] for x in pots.items() if x[1] == '#')



pots = defaultdict(lambda: '.', [i for i in enumerate(initial)])

count = []
for c in range(200):
    new = defaultdict(lambda: '.')
    v = list(pots.keys())
    for i in range(min(v)-5, max(v) + 5):
        curr = ''.join([pots[i] for i in range(i-2, i+3)])
        for note in notes:
            if note[0] == curr: new[i] = note[1]
    pots = new
    count += [sum(x[0] for x in pots.items() if x[1] == '#')]

# growth is by 36 each iteration
[count[i+1]-count[i] for i in range(len(count)-1)]

# value is 6658 after 200
count[-1]

# after 50000000000, should be:
(50000000000-200)*36 + count[-1]

