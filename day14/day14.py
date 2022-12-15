# https://adventofcode.com/2022/day/14

# read and split
with open('input.txt','r') as f:
    data = f.read().strip().split('\n')
rows = [[eval(i) for i in row.split(' -> ')] for row in data]

# convert rows into list of rock positions
rock_list = []
for row in rows:
    for (x1,y1), (x2,y2) in zip(row[:-1], row[1:]):
        if x1==x2:
            rock_list.extend([(y,x1) for y in range(min(y1,y2), max(y1,y2)+1)])
        else:
            rock_list.extend([(y1,x) for x in range(min(x1,x2), max(x1,x2)+1)])

# this function determines where the next piece of sand lands
def sand_fall(y,x, ext=False):
    # we can go down 1
    if cave.get((y+1,x), 1) == 0: 
        return sand_fall(y+1, x)
    # we can't go down
    elif (y == y_max) & (not ext):
        return (0,500)
    # we can go diagonal left 1
    elif cave.get((y+1,x-1), 1) == 0: 
        return sand_fall(y+1, x-1)
    elif (x == x_min) & (not ext): # end early, we are at left edge
        return (0,500)
    # we can go diagonal right 1
    elif cave.get((y+1,x+1), 1) == 0: 
        return sand_fall(y+1, x+1)
    elif (x == x_max) & (not ext): # end early, we are at right edge
        return (0,500)
    # nowhere to go
    return y,x

# get boundaries of the cave
def get_bounds(rock_list, pad_x=0, pad_y=0):
    x_min = min([r[1] for r in rock_list]) - pad_x
    x_max = max([r[1] for r in rock_list]) + pad_x
    y_min = 0
    y_max = max([r[0] for r in rock_list]) + pad_y
    return x_min, x_max, y_min, y_max

# create cave for part 1
x_min, x_max, y_min, y_max = get_bounds(rock_list, pad_x=0, pad_y=0)
cave = {(y,x):0 for x in range(x_min, x_max+1) for y in range(y_min, y_max+1)}
for y,x in rock_list: cave[(y,x)] = 1

# fill with sand (use ext=False as we have left/right bounds)
room = True
while room:
    y,x = sand_fall(0,500, ext=False)
    if (y,x) == (0,500): room = False
    else: cave[(y,x)] = 2

# part 1 answer
print(sum([v==2 for v in cave.values()]))

# create cave for part 2
x_min, x_max, y_min, y_max = get_bounds(rock_list, pad_x=1000, pad_y=1)
cave = {(y,x):0 for x in range(x_min, x_max) for y in range(y_min, y_max)}
for y,x in rock_list: cave[(y,x)] = 1

# fill with sand (use ext=True as we have infinite floor)
room = True
while room:
    y,x = sand_fall(0,500, ext=True)
    if (y,x) == (0,500): 
        cave[(0,500)] = 2
        room = False
    else: cave[(y,x)] = 2

# part 2 answer
print(sum([v==2 for v in cave.values()]))