# https://adventofcode.com/2022/day/12

# read and split
with open('input.txt','r') as f:
    data = f.read().strip().split('\n')

# this dic and func maps any input to an integer
capitals = {'S':1, 'E':27}
def map_letters(x):
    return capitals.get(x, ord(x)-96)

# make height map of integers
hmap = [[map_letters(x) for x in row] for row in data]
len(hmap), len(hmap[0])

# function to translate input into the graph we need
def make_adjacency_map(hmap):
    adj_map = {} # to store which nodes and adjacent to each other
    ni = len(hmap) # n_rows
    nj = len(hmap[0]) # n_cols

    # these to store for later
    key_points = {'start': None, 'end': None, 'lowest': []}

    for i in range(ni): # for each row
        for j in range(nj): # each point in that row
            adjs = [] # make list of adjacents
            # note we are making our map in reverse
            # so we are mapping distance from E to S
            # (so we can easily do part 2)
            # hence why the adjacency allows you 
            # to "go up" as many as you like but down only 1
            if i > 0:
                if hmap[i][j] - hmap[i-1][j] <= 1:
                    adjs.append((i-1,j))
            if j > 0:
                if hmap[i][j] - hmap[i][j-1] <= 1:
                    adjs.append((i,j-1))
            if i < ni-1:
                if hmap[i][j] - hmap[i+1][j] <= 1:
                    adjs.append((i+1,j))
            if j < nj-1:
                if hmap[i][j] - hmap[i][j+1] <= 1:
                    adjs.append((i,j+1))
            adj_map[(i,j)] = adjs # add adjacencies

            # keep a record of the key points on the map
            if data[i][j] == 'S':
                key_points['start'] = (i,j)
            if data[i][j] == 'E':
                key_points['end'] = (i,j)
            if data[i][j] =='a':
                key_points['lowest'].append((i,j))
        
    return adj_map, key_points


# classic bit of dijkstra 
def dijkstra_algorithm(graph, start_node):

    unvisited_nodes = list(graph.keys()) # initialise everything we haven't visited
    previous_nodes = {} # maps nodes to the node to visit 1 step before
 
    # initialise shortest distance to be very high for all nodes
    shortest_path = {node: 1e24 for node in unvisited_nodes}
    shortest_path[start_node] = 0 # except start node is zero
    
    while unvisited_nodes: # loops until all visited 
        current_min_node = None # get node with lowest distance
        for node in unvisited_nodes: # for each unvisited
            if current_min_node == None: # if our best is still None... 
                current_min_node = node # replace with the new unvisited
            # else check if it is lower and if it is replace
            elif shortest_path[node] < shortest_path[current_min_node]:  
                current_min_node = node
                
        neighbors = graph[current_min_node] # get all neighbours of current node
        for neighbor in neighbors: # for eahc neighbour
            # note in our case all valid edges are length 1, hence we only ever +1
            tentative_value = shortest_path[current_min_node] + 1 
            if tentative_value < shortest_path[neighbor]: # check if it is better
                shortest_path[neighbor] = tentative_value # if yes replace
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node # and update best path
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

# get adjacency map and key points
adj_map, key_points = make_adjacency_map(hmap)

# run shortest path algo
node_routing, min_distance = dijkstra_algorithm(adj_map, key_points['end'])

# part 1 answer
print(min_distance[key_points['start']])

# find shortest distance to any of the lowest points
min_dist = 1e19
for s in key_points['lowest']:
    if min_distance[s] < min_dist:
        min_dist = min_distance[s]
        new_start = s

# part 2 answer
print(min_dist)

# bonus retrieve best route:
route = [new_start]
next = node_routing[route[-1]]
while next != key_points['end']:
    route.append(next)
    next = node_routing[route[-1]]