# https://adventofcode.com/2022/day/17

with open('input.txt', 'r') as f:
    data = f.read().strip()


def create_rock():
    # grab from start, put to end
    new_rock = rocks.pop(0)
    rocks.append(new_rock)
    # offset to starting position
    height = max([y for _, y in fallen])
    new_rock = {(x+2, y+height+4) for x, y in new_rock}
    return new_rock


def check_walls(rock):
    return all([(x >= 0) & (x <= 6) for x, y in rock])


def check_existing(rock):
    return len(rock.intersection(fallen)) == 0


def rock_fall(new_rock, debug=False):
    # cycle moves
    next_move = moves.pop(0)
    global move_counter
    move_counter += 1
    moves.append(next_move)

    # try to shift horizontal
    move_rock = {(x+next_move, y) for x, y in new_rock}
    if check_walls(move_rock) & check_existing(move_rock):
        if debug:
            print('can push x', move_rock)
        new_rock = move_rock

    # shift down
    move_rock = {(x, y-1) for x, y in new_rock}
    if check_existing(move_rock):
        # space to fall
        if debug:
            print('can fall', move_rock)
        rock_fall(move_rock)
    else:
        if debug:
            print('cannot fall', new_rock)
        # no space to fall so revert to move_rock
        for r in new_rock:
            fallen.add(r)


rocks = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)},
    {(0, 0), (1, 0), (2, 2), (2, 1), (2, 0)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (0, 1), (1, 0), (1, 1)},
]


def starting_state():
    width = 7
    xmap = {'>': 1, '<': -1}
    global move_counter
    move_counter = 0
    fallen = {(x, 0) for x in range(width)}
    height = tuple([max([y for x, y in fallen if x == col])
                   for col in range(7)])
    rocks = [
        {(0, 0), (1, 0), (2, 0), (3, 0)},
        {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)},
        {(0, 0), (1, 0), (2, 2), (2, 1), (2, 0)},
        {(0, 0), (0, 1), (0, 2), (0, 3)},
        {(0, 0), (0, 1), (1, 0), (1, 1)},
    ]
    moves = [xmap[char] for char in data]

    return rocks, moves, fallen, move_counter


def solve(
        start_idx,  # when the cycle starts
        repeat_idx,  # when the cycle ends
        height_record,  # height at each timestep
        duration,  # how long we run for
):

    # time in each cycle
    cycle_len = repeat_idx - start_idx

    # height added in each cycle
    added_each_cycle = height_record[repeat_idx] - height_record[start_idx]

    # height we get to before cycles begin
    added_before_first_cycle = height_record[start_idx]

    # how many cycles we can fit into the time
    n_cycles = (duration - start_idx) // cycle_len
    # how many time steps occur after the cycles end
    time_after_cycles = (duration - start_idx) % cycle_len

    # total height added during all the cycles
    total_added_during_cycles = n_cycles * added_each_cycle

    # height added after the cycles finish
    added_after_cycles = height_record[start_idx +
                                       time_after_cycles] - height_record[start_idx]

    # anwert
    return (total_added_during_cycles
            + added_after_cycles
            + added_before_first_cycle - 1)


def fall_and_solve(duration):
    n_moves, n_rocks = len(moves), len(rocks)
    memory = 100
    states = {}
    height_record = []
    global fallen

    for i in range(duration):
        rock_fall(create_rock())

        # record top of ys
        height = tuple([max([y for x, y in fallen if x == col])
                       for col in range(7)])
        # prune fallen
        fallen = {(x, y) for x, y in fallen if y > max(height) - memory}

        # get relative shape
        rel_height = tuple([y-min(height) for y in height])
        height_record.append(max(height))

        # record state
        state = (rel_height, i % n_rocks, move_counter % n_moves)
        if state in states:
            repeat_idx = i
            start_idx = states[state]
            break
        else:
            states[state] = i

    return solve(
        start_idx,  # when the cycle starts
        repeat_idx,  # when the cycle ends
        height_record,  # height at each timestep
        duration,  # how long we run for
    )


# part 1 answer
rocks, moves, fallen, move_counter = starting_state()
print(fall_and_solve(2022))

# part 2 answer
rocks, moves, fallen, move_counter = starting_state()
print(fall_and_solve(1000000000000))
