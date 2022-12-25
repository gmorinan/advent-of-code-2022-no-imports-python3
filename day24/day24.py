# https://adventofcode.com/2022/day/24

with open('input.txt', 'r') as f:
    data = f.read().strip().split('\n')


def lowest_common_multiple(x, y):
    # to compute how long it takes for the blizzards to loop
    big = x if x > y else y
    while True:
        if ((big % x == 0) and (big % y == 0)):
            return big
        big += 1


# map input characters to directions
dmap = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}

# compute how long it takes blizzards to cycle
height, width = len(data), len(data[0])
loop = lowest_common_multiple(width-2, height-2)

# to let blizzards wrap around
wrap_map = {'y': {height-1: 1, 0: height-2}, 'x': {width-1: 1, 0: width-2}}

# simple function to get neighbours (or same place)
possible_adjs = [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0]]


def get_adjs(coord):  # get possible adjacent positions
    x, y = coord
    return set([(x+xd, y+yd) for xd, yd in possible_adjs])


# walking space, entire grid and walls
space = set([(0, 1), (height-1, width-2)] + [(y, x)
            for y in range(1, height-1) for x in range(1, width-1)])
all_grid = set([(y, x) for y in range(height) for x in range(width)])
walling = all_grid.difference(space)

# first need to track where blizzards are at any time
# the x,y,z coordinates of blizzards[0] will be identical to blizzards[600] (we are on 600 time cycle)
blizzards = {0: [((y, x), data[y][x]) for y, x in space if data[y][x] != '.']}
for t in range(1, loop):
    blizzards[t] = []
    # print(len(set([(y,x,d) for (y,x,z) , d in blizzards[t-1]])))
    for (y, x), direction in blizzards[t-1]:
        yd, xd = dmap[direction]
        new_y, new_x = y+yd, x+xd
        new_coord = (
            wrap_map['y'].get(new_y, new_y),
            wrap_map['x'].get(new_x, new_x)
        )
        blizzards[t].append((new_coord, direction))

# just what we need
blizzards_minimal = {k: [(y, x) for (y, x), d in v]
                     for k, v in blizzards.items()}

# next we need to create map of all possible locations
space_x_time = {k: space.difference(v) for k, v in blizzards_minimal.items()}


def walk_time(start_node, target_node, time):
    # main path finding function
    currents = {start_node}
    # continue until we see the target_node...
    while target_node not in currents:
        time += 1
        # find all possible spaces at this time
        possible = space_x_time[time % loop]
        # find all places adjacent to where we could reach at t-1
        all_adj = []
        [all_adj.extend(get_adjs(yx)) for yx in currents]
        # new places are intersection
        currents = set(all_adj).intersection(possible)
    return time


start_node = (0, 1)
target_node = (height-1, width-2)

# part 1 answer
walk1_time = walk_time(start_node, target_node, 0)
print(walk1_time)

# part 2 answer
walk2_time = walk_time(target_node, start_node, walk1_time)
walk3_time = walk_time(start_node, target_node, walk2_time)
print(walk3_time)
