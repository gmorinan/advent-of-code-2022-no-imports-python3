# https://adventofcode.com/2022/day/17

# read n split
with open('input.txt', 'r') as f:
    data = f.read().strip().split('\n')


def find_connected_subgraphs(symmetric_graph):
    """Populate list of connected subgraphs"""
    # record connected subgraphs
    # input is a symmetric graph in dict form
    connected_subgraphs = []
    to_visit = set(symmetric_graph)  # remaining nodes
    while to_visit:  # while we have unvisited
        subgraph_i = {}  # start subgraph
        nextup = {to_visit.pop()}  # populate next places to visit
        while nextup:  # visit nest
            current = nextup.pop()  # grab next
            to_visit.discard(current)  # dont need to visit it
            seen = symmetric_graph[current]  # add all we can see
            subgraph_i[current] = seen  # add to subgraph
            nextup = nextup.union(seen.intersection(
                to_visit))  # add newly seen to nextup
        # once we've added all that can be seen so we finish the graph
        connected_subgraphs.append(subgraph_i)
    connected_subgraphs = sorted([set(sub) for sub in connected_subgraphs])
    return connected_subgraphs


# extract coords
cubes = set([tuple([int(i) for i in row.split(',')]) for row in data])

# adjacent coordinates
adjs = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]


def make_adjs(cube):
    # get adjacents spaces
    x, y, z = cube
    return set([(x+xd, y+yd, z+zd) for xd, yd, zd in adjs])


def solve(cubes):
    # exposed are those which aren't in the main cubes set
    return sum([len(make_adjs(cube).difference(cubes)) for cube in cubes])


# part 1 answer
print(solve(cubes))

# make full grid
full_grid = [(x, y, z) for x in range(-1, 21)
             for y in range(-1, 21) for z in range(-1, 21)]
# get all the air spaces
air_space = set(full_grid).difference(set([tuple(x) for x in cubes]))

# construct symmetric graph as a dict, i.e. which air connects to other air
air_map = {air: make_adjs(air).intersection(air_space) for air in air_space}

# get connected subgraphs
connnected_subgraphs = find_connected_subgraphs(air_map)

# the largest connected subgraph is the exterior air
max_graph_size = max([len(g) for g in connnected_subgraphs])

# any subgraph smaller than the largest is an airpocked
air_pockets = [subg for subg in connnected_subgraphs if len(
    subg) < max_graph_size]

# add air pockets to cubes
cubes_filled = cubes.copy()
for air_pocket in air_pockets:
    cubes_filled = cubes_filled.union(air_pocket)

# part 2 answer
print(solve(cubes_filled))
