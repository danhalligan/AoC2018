def update(recipes, pos):
    new = map(int, list(str(recipes[pos[0]] + recipes[pos[1]])))
    recipes += list(new)
    pos = [
        (pos[0] + recipes[pos[0]] + 1) % len(recipes),
        (pos[1] + recipes[pos[1]] + 1) % len(recipes),
    ]
    return recipes, pos


# part 1
recipes = [3, 7]
pos = [0, 1]
while len(recipes) < 509671 + 10:
    recipes, pos = update(recipes, pos)

print("".join(map(str, recipes[509671 : 509671 + 10])))

# part 2
# Note that the search term is not necessarily the last digits after an update!
recipes = [3, 7]
pos = [0, 1]
search = "509671"
while search not in "".join(map(str, recipes[-10:])):
    recipes, pos = update(recipes, pos)

print(re.search(search, "".join(map(str, recipes))).span()[0])
