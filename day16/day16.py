# https://adventofcode.com/2022/day/16

# read n split
with open('input.txt', 'r') as f:
    data = f.read().strip().split('\n')


def parse_input(row):
    # parse input
    id = row[6:8]
    pressure = int(row.split(';')[0].split('=')[-1])
    routes = set(row[row.find(',')-2:].strip().split(', '))
    return (id, pressure, routes)


def dijkstra_algorithm(graph, start_node):

    # classic bit of dijkstra to work out shorted route between active valvces
    # initialise everything we haven't visited
    unvisited_nodes = list(graph.keys())
    previous_nodes = {}  # maps nodes to the node to visit 1 step before

    # initialise shortest distance to be very high for all nodes
    shortest_path = {node: 1e24 for node in unvisited_nodes}
    shortest_path[start_node] = 0  # except start node is zero

    while unvisited_nodes:  # loops until all visited
        current_min_node = None  # get node with lowest distance
        for node in unvisited_nodes:  # for each unvisited
            if current_min_node == None:  # if our best is still None...
                current_min_node = node  # replace with the new unvisited
            # else check if it is lower and if it is replace
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # get all neighbours of current node
        neighbors = graph[current_min_node]
        for neighbor in neighbors:  # for eahc neighbour
            # note in our case all valid edges are length 1, hence we only ever +1
            tentative_value = shortest_path[current_min_node] + 1
            # check if it is better
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value  # if yes replace
                # We also update the best path to the current node
                # and update best path
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path


# parse input
parsed = [parse_input(row)for row in data]
pressure_map = {id: p for id, p, _ in parsed}
route_map = {id: rout for id, _, rout in parsed}

# use dijk to get shorted path
adj_dict = {node: dijkstra_algorithm(route_map, node)[1] for node in route_map}
# need to add +1 to each travel time to account for turning on valves
adj_dict = {node: {k: v+1 for k, v in subdict.items()}
            for node, subdict in adj_dict.items()}

# we only care about working valves, remove any with zero values
valid = [k for k, v in pressure_map.items() if (v > 0) or (k == 'AA')]
adj_dict = {k: v for k, v in adj_dict.items() if
            k in [k for k, v in pressure_map.items() if (v > 0) or (k == 'AA')]}
adj_dict = {i: {k: v for k, v in adj_dict[i].items() if
                (k in valid) and (k != i)} for i in valid}


def eval_solution(current, visited, unvisited, minutes, score):
    # main recursive function to eval routes

    if (current, visited, unvisited, minutes) in states:  # recall prev res
        score = states[(current, visited, unvisited, minutes)]
        return (current, visited, unvisited, minutes, score)

    # record this state
    states[(current, visited, unvisited, minutes)] = score

    if minutes <= 1:  #  no point proceeding
        states[(current, visited, unvisited, minutes)] = score
        return (current, visited, unvisited, minutes, score)

    # try to get best possible score
    new_scores = [score]
    new_currents = [current]
    new_visiteds = [visited]
    new_unvisiteds = [unvisited]
    new_minutes = [minutes]

    for node in unvisited:
        travel = adj_dict[current][node]  # travel time
        mins_left = (minutes - travel)
        if mins_left > 0:  # only proceed if we have enough time
            # extra score we get
            add_score = mins_left * pressure_map[node]
            # remove node from unvisited
            unvisited_new = tuple([x for x in unvisited if x != node])
            visited_new = list(visited)
            visited_new.append(node)
            # call this function for remaining nodes
            (current_new, visited_new, unvisited_new, minutes_new, score_new
             ) = eval_solution(node,
                               visited=tuple(visited_new),
                               unvisited=unvisited_new,
                               minutes=mins_left,
                               score=score+add_score)

            new_scores.append(score_new)
            new_currents.append(current_new)
            new_visiteds.append(visited_new)
            new_unvisiteds.append(unvisited_new)
            new_minutes.append(minutes_new)

    # get best score
    best_idx = 0
    score = 0
    for idx, val in enumerate(new_scores):
        if val > score:
            score = val
            best_idx = idx

    current = new_currents[best_idx]
    visited = new_visiteds[best_idx]
    unvisited = new_unvisiteds[best_idx]
    minutes = new_minutes[best_idx]

    states[(current, visited, unvisited, minutes)] = score
    return current, visited, unvisited, minutes, score


def initiate():
    unvisited = tuple([x for x in adj_dict if x != 'AA'])
    visited = tuple([])
    states = {}
    return unvisited, visited, states


# part 1 answer
unvisited, visited, states = initiate()
print(eval_solution('AA', visited, unvisited, 30, 0)[-1])


# part 2 re-initiate
print(eval_solution('AA', visited, unvisited, 30, 0)[-1])
eval_solution('AA', visited, unvisited, 26, 0)[-1]

# sort and filter answers > 0
valid_states = [(k[1], v) for k, v in states.items() if v > 0]
valid_states = sorted(valid_states, key=lambda x: x[1])[::-1]

# arbitray threshold to consider our best paid needs to have one in top 5% of routes
idx_thr = int(len(valid_states)*0.05)

# brute force comparison of pairs :'(
# not the best way but only ~40s at least
best_score = 0
# we assume one of the routes must be in top % of routes
for i, (route_i, score_i) in enumerate(valid_states[:idx_thr]):
    # then check against all other routes
    for j, (route_j, score_j) in enumerate(valid_states[i+1:]):
        if len(set(route_j).intersection(route_i)) == 0:
            if score_i + score_j > best_score:
                best_score = score_i + score_j

# answer to part 2
print(best_score)
