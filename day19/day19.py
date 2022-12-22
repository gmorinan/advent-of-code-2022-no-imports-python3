# https://adventofcode.com/2022/day/19

# read it
with open('input.txt', 'r') as f:
    data = f.read().strip().split('\n')


def parse_input_str(mystr):
    # extract numbers from the string
    idx, vals = mystr.split(':')
    idx = int(idx.split(' ')[-1])
    sents = [s.split(' ') for s in vals.split('.')]
    or1 = int(sents[0][-2])
    cl1 = int(sents[1][-2])
    ob1 = int(sents[2][-5])
    ob2 = int(sents[2][-2])
    ge1 = int(sents[3][-5])
    ge3 = int(sents[3][-2])
    # each line is ore/clay/obsidian build costs
    build_costs = ((or1, 0, 0),  # ore robot cost
                   (cl1, 0, 0),  # clay robot cost
                   (ob1, ob2, 0),  # obsidan robot cost
                   (ge1, 0, ge3))  # geode robot cost

    return idx, build_costs


def attempt_route(
    n_resource=(0, 0, 0),  #  resources we have at this time
    n_robot=(1, 0, 0),  # robots we have at this time
    minutes=24,  # how many minutes left
    start=24  # what the clock started at
):
    """main recursive function"""

    if minutes == start:
        global states
        states = {}

    # if we already saw this stage, return it
    if (n_resource, n_robot, minutes) in states:
        return states[(n_resource, n_robot, minutes)]

    if minutes <= 1:  # no point building anytihng new if we have only 1 minute
        states[(n_resource, n_robot, minutes)] = 0
        return 0

    # checks if there is any point building a robot (idx=0 is ore etc)
    def is_build_worthwhile(idx):
        # compute the max spend possible for a given resource
        max_spend = max([cost[idx] for cost in build_costs]) * minutes
        # subtract our resources (now + future added)
        max_delta = max_spend - n_resource[idx] - (n_robot[idx] * minutes)
        # only worth considering a new robot if this is >0
        return max_delta > 0

    # checks if its possible to build a given robot (idx=0 is ore, etc.)
    def is_build_possible(idx):
        return all([n >= c for n, c in zip(n_resource, build_costs[idx])])

    # call this to update robots
    def update_robot(n_robot, idx=None):
        # no need to change if we are building nothing or geode
        if (idx is None):
            return n_robot
        if (idx == 3):
            return n_robot
        n_robots_new = list(n_robot)
        n_robots_new[idx] += 1
        return tuple(n_robots_new)

    # updates our resources for this timestep, given how many robots we have and build idx
    def add_resource(n_resource, n_robot, build_idx=None):
        robot_cost = build_costs[build_idx] if build_idx is not None else [
            0, 0, 0]
        return tuple([n+r-c for n, r, c in zip(n_resource, n_robot, robot_cost)])

    # return new route attempt assuming we choose to build robot build_idx
    def new_route(n_resource, n_robot, minutes, build_idx):
        return attempt_route(
            n_resource=add_resource(n_resource, n_robot, build_idx),
            n_robot=update_robot(n_robot, build_idx),
            minutes=minutes-1)

    # always prioritise building geode if its possible
    if is_build_possible(3):
        # from next minute we mine extr geodes, so score gets (minutes-1) extra
        score = (minutes - 1) + new_route(n_resource, n_robot, minutes, 3)

    # if we can't do a geode, next we always want to try a obsidean if its possible and worthwhile
    elif is_build_possible(2) & is_build_worthwhile(2):
        score = new_route(n_resource, n_robot, minutes, 2)

    else:  # here we have to consider up to 3 options, build ore, build clay, build nothing
        score = 0
        # Option 1: build ore
        if is_build_possible(0) & is_build_worthwhile(0):
            score = new_route(n_resource, n_robot, minutes, 0)
        # Option 2: build clay
        # note if its not worth building obsi then no point clay either...
        if is_build_possible(1) & is_build_worthwhile(1) & is_build_worthwhile(2):
            score = max(score, new_route(n_resource, n_robot, minutes, 1))
        # Option 3: build nothing
        score = max(score, new_route(n_resource, n_robot, minutes, None))

    # record so we don't need to recompute if we see this state again
    states[(n_resource, n_robot, minutes)] = score
    return score


# parse blueprints
blueprints = {idx: build_costs for idx, build_costs
              in [parse_input_str(mystr) for mystr in data]}

# solve part 1 (note build_costs is used as global so not passed to function)
final_scores = {}
for idx, build_costs in blueprints.items():
    final_scores[idx] = attempt_route(minutes=24, start=24)
# part 1 answer
print(sum([k*v for k, v in final_scores.items()]))

# solve part 2 (we just need to call build_cost)
scr123 = []
for blueprint_id in [1, 2, 3]:
    build_costs = blueprints[blueprint_id]
    scr123.append(attempt_route(minutes=32, start=32))
# part 2 answer
print(scr123[0] * scr123[1] * scr123[2])
